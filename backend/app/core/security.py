"""Password hashing and signed bearer-token helpers."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

from app.core.config import settings

try:
    import bcrypt
except ImportError:  # dependency is declared; startup remains importable for diagnostics
    bcrypt = None


def hash_legacy_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    if bcrypt is None:
        raise RuntimeError("bcrypt is required for creating new passwords")
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=settings.bcrypt_rounds)).decode()


def verify_password(password: str, stored_hash: str) -> tuple[bool, bool]:
    """Return (valid, needs_rehash), supporting existing SHA-256 users."""
    if stored_hash.startswith("$2") and bcrypt is not None:
        return bcrypt.checkpw(password.encode(), stored_hash.encode()), False
    valid = hmac.compare_digest(hash_legacy_password(password), stored_hash)
    return valid, valid and settings.allow_legacy_sha256


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(user_id: int, email: str, is_admin: bool = False) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "email": email, "is_admin": bool(is_admin), "exp": int(time.time()) + settings.token_expire_minutes * 60}
    encoded = f"{_b64(json.dumps(header, separators=(',', ':')).encode())}.{_b64(json.dumps(payload, separators=(',', ':')).encode())}"
    signature = hmac.new(settings.jwt_key().encode(), encoded.encode(), hashlib.sha256).digest()
    return f"{encoded}.{_b64(signature)}"


def decode_access_token(token: str) -> dict:
    try:
        header, payload, signature = token.split(".")
        signed = f"{header}.{payload}"
        expected = hmac.new(settings.jwt_key().encode(), signed.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(_unb64(signature), expected):
            raise ValueError("invalid signature")
        data = json.loads(_unb64(payload))
        if int(data["exp"]) < int(time.time()):
            raise ValueError("token expired")
        return data
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid access token") from exc
