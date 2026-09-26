"""Small REST client used by Streamlit instead of direct PostgreSQL access."""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")


class BackendUnavailableError(RuntimeError):
    """Raised when the FastAPI service cannot be reached."""


def error_detail(exc: requests.HTTPError, fallback: str = "Request failed") -> str:
    """Safely extract an API error even when the response is not JSON."""
    response = exc.response
    if response is None:
        return fallback

    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = payload.get("detail") or payload.get("message")
            if detail:
                return str(detail)
    except (ValueError, requests.exceptions.JSONDecodeError):
        pass

    text = (response.text or "").strip()
    return text[:300] if text else f"{fallback} (HTTP {response.status_code})"


def _headers() -> dict[str, str]:
    token = st.session_state.get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def request(method: str, path: str, **kwargs: Any) -> Any:
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            headers=_headers(),
            timeout=30,
            **kwargs,
        )
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise BackendUnavailableError(
            f"The backend is not available at {API_URL}. "
            "Start the FastAPI server and try again."
        ) from exc
    if response.status_code == 401:
        st.session_state.pop("access_token", None)
    response.raise_for_status()
    return response.json() if response.content else None


def login(email: str, password: str) -> dict:
    data = request("POST", "/auth/login", json={"email": email, "password": password})
    st.session_state["access_token"] = data["access_token"]
    return data


def register(username: str, email: str, password: str) -> dict:
    return request("POST", "/auth/register", json={"username": username, "email": email, "password": password})


def create_reset_token(email: str) -> dict:
    data = request("POST", "/auth/forgot-password", json={"email": email})
    return {"reset_code": data["reset_code"]}


def reset_password(email: str, code: str, password: str) -> tuple[bool, str]:
    try:
        data = request("POST", "/auth/reset-password", json={"email": email, "code": code, "new_password": password})
        return True, data.get("message", "Password reset successfully")
    except requests.HTTPError as exc:
        return False, error_detail(exc, "Password reset failed")


def get(path: str, **kwargs: Any) -> Any:
    return request("GET", path, **kwargs)


def post(path: str, **kwargs: Any) -> Any:
    return request("POST", path, **kwargs)
