"""Database operations for authentication."""

import secrets
from datetime import datetime, timedelta

from app.core.security import create_access_token, hash_password, verify_password
from app.database.connection import db_cursor


def register(username: str, email: str, password: str) -> dict:
    with db_cursor(commit=True) as cur:
        cur.execute("SELECT id FROM users WHERE LOWER(email)=LOWER(%s)", (email.strip(),))
        if cur.fetchone():
            raise ValueError("This email is already registered.")
        cur.execute("INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s) RETURNING id", (username.strip(), email.strip().lower(), hash_password(password)))
        return {"id": cur.fetchone()[0], "username": username.strip(), "email": email.strip().lower(), "is_admin": False}


def login(email: str, password: str) -> dict | None:
    with db_cursor(commit=True) as cur:
        cur.execute("SELECT id,username,email,password_hash,is_admin FROM users WHERE LOWER(email)=LOWER(%s)", (email.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        valid, needs_rehash = verify_password(password, row[3])
        if not valid:
            return None
        if needs_rehash:
            cur.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hash_password(password), row[0]))
        user = {"id": row[0], "username": row[1], "email": row[2], "is_admin": bool(row[4])}
        user["access_token"] = create_access_token(user["id"], user["email"], user["is_admin"])
        return user


def user_by_email(email: str) -> dict | None:
    with db_cursor() as cur:
        cur.execute("SELECT id,username,email,is_admin FROM users WHERE LOWER(email)=LOWER(%s)", (email.strip(),))
        row = cur.fetchone()
    return {"id": row[0], "username": row[1], "email": row[2], "is_admin": bool(row[3])} if row else None


def create_reset_code(email: str) -> dict | None:
    user = user_by_email(email)
    if not user:
        return None
    code = f"{secrets.randbelow(1_000_000):06d}"
    with db_cursor(commit=True) as cur:
        cur.execute("UPDATE password_reset_tokens SET used=TRUE WHERE user_id=%s AND used=FALSE", (user["id"],))
        cur.execute("INSERT INTO password_reset_tokens (user_id,reset_code,expires_at) VALUES (%s,%s,%s)", (user["id"], code, datetime.utcnow() + timedelta(hours=1)))
    return {"code": code, "username": user["username"], "email": user["email"]}


def reset_password(email: str, code: str, password: str) -> bool:
    with db_cursor(commit=True) as cur:
        cur.execute("SELECT u.id FROM users u JOIN password_reset_tokens t ON t.user_id=u.id WHERE LOWER(u.email)=LOWER(%s) AND t.reset_code=%s AND t.used=FALSE AND t.expires_at>NOW() ORDER BY t.created_at DESC LIMIT 1", (email.strip(), code.strip()))
        row = cur.fetchone()
        if not row:
            return False
        cur.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hash_password(password), row[0]))
        cur.execute("UPDATE password_reset_tokens SET used=TRUE WHERE user_id=%s AND reset_code=%s", (row[0], code.strip()))
        return True
