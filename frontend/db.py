"""Backward-compatible application repository backed by FastAPI.

The UI can retain its existing function names while all persistence crosses
the REST boundary. No PostgreSQL driver or database credential belongs in the
Streamlit process anymore.
"""

from __future__ import annotations

import requests

from api_client import get, login, post, register, create_reset_token as api_create_reset_token
from api_client import error_detail
from api_client import reset_password as api_reset_password


def add_user(username, email, password):
    try:
        register(username, email, password)
        return True, "Account created successfully. Please login."
    except requests.HTTPError as exc:
        return False, error_detail(exc, "Signup failed.")


def check_login(email, password):
    try:
        user = login(email, password)
        return (user["id"], user["username"], user["email"], user["is_admin"])
    except requests.HTTPError:
        return None


def get_user_by_email(email):
    try:
        return get("/auth/user", params={"email": email})
    except requests.HTTPError:
        return None


def create_reset_token(user_id):
    # Legacy signature receives user_id; the API is email-based. The auth UI
    # already knows the email and uses this result only for the reset email.
    raise RuntimeError("Use create_reset_token_for_email(email) from the API client")


def create_reset_token_for_email(email):
    return api_create_reset_token(email)


def reset_password_with_code(email, reset_code, new_password):
    return api_reset_password(email, reset_code, new_password)


def create_conversation(user_id, title="New Chat"):
    return post("/conversations", json={"title": title})["id"]


def get_conversations(user_id):
    rows = get("/conversations")
    return [(r["id"], r["title"], r["created_at"]) for r in rows]


def rename_conversation(conversation_id, new_title):
    post(f"/conversations/{conversation_id}/rename", json={"title": new_title})
    return True


def delete_conversation(conversation_id):
    from api_client import request
    request("DELETE", f"/conversations/{conversation_id}")
    return True


def get_messages_by_conversation(conversation_id):
    rows = get(f"/conversations/{conversation_id}/messages")
    return [(r["role"], r["content"]) for r in rows]


def add_message(user_id, role, content, conversation_id=None):
    if conversation_id is None:
        conversation_id = create_conversation(user_id)
    post(f"/conversations/{conversation_id}/messages", json={"role": role, "content": content})


def get_all_user_messages(user_id):
    rows = get("/history/messages")
    return [(r["role"], r["content"], r["created_at"], r["conversation_id"]) for r in rows]


def add_mood(user_id, mood):
    post("/mood", json={"mood": mood})


def get_moods(user_id):
    return [row["mood"] for row in get("/mood")]


def add_journal(user_id, entry):
    post("/journal", json={"entry": entry})


def get_journals(user_id):
    return [row["entry"] for row in get("/journal")]


def log_user_activity(user_id, action_type, page_name, details=""):
    post("/activity", json={"action_type": action_type, "page_name": page_name, "details": details})


def get_messages_by_user(user_id):
    return [(r["role"], r["content"], r["created_at"]) for r in get("/admin/messages", params={"user_id": user_id})]


def get_moods_by_user(user_id):
    return [(r["mood"], r["created_at"]) for r in get("/admin/moods", params={"user_id": user_id})]


def get_journals_by_user(user_id):
    return [(r["entry"], r["created_at"]) for r in get("/admin/journals", params={"user_id": user_id})]


def get_all_users():
    return get("/admin/users")


def get_user_activity_log(user_id, limit=50):
    return [(r["action_type"], r["page_name"], r["details"], r["timestamp"]) for r in get("/admin/activity", params={"limit": limit, "user_id": user_id})]


def get_last_activity_with_details(user_id):
    rows = get_user_activity_log(user_id, 1)
    return (rows[0][3], f"{rows[0][0]} on {rows[0][1]}") if rows else (None, "No activity")
