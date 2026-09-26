"""Protected application/data routes used by the Streamlit client."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import admin_claims, current_claims
from app.database.connection import db_cursor
from app.database.schemas import ActivityCreate
from app.services.privacy import redact_sensitive_data

router = APIRouter(tags=["Application"])


def uid(claims):
    return int(claims["sub"])


def permitted_user(target_user_id: int, claims: dict) -> int:
    """Allow self-access or administrator access to another user's records."""
    if uid(claims) != target_user_id and not claims.get("is_admin"):
        raise HTTPException(403, "You cannot access another user's records")
    return target_user_id


@router.get("/auth/user")
def user_by_email(email: str):
    with db_cursor() as cur:
        cur.execute("SELECT id,username,email,is_admin FROM users WHERE LOWER(email)=LOWER(%s)", (email,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "User not found")
    return {"id": row[0], "username": row[1], "email": row[2], "is_admin": bool(row[3])}


@router.post("/conversations")
def create_conversation(body: dict, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("INSERT INTO conversations (user_id,title) VALUES (%s,%s) RETURNING id,title,created_at", (uid(claims), body.get("title", "New Chat")))
        row = cur.fetchone()
    return {"id": row[0], "title": row[1], "created_at": row[2]}


@router.get("/conversations")
def conversations(claims: dict = Depends(current_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT id,title,created_at FROM conversations WHERE user_id=%s ORDER BY created_at DESC", (uid(claims),))
        return [{"id": r[0], "title": r[1], "created_at": r[2]} for r in cur.fetchall()]


@router.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: int, body: dict, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("SELECT id FROM conversations WHERE id=%s AND user_id=%s", (conversation_id, uid(claims)))
        if not cur.fetchone():
            raise HTTPException(404, "Conversation not found")
        cur.execute("INSERT INTO messages (user_id,role,content,conversation_id) VALUES (%s,%s,%s,%s) RETURNING id,created_at", (uid(claims), body["role"], redact_sensitive_data(body["content"]), conversation_id))
        row = cur.fetchone()
    return {"id": row[0], "created_at": row[1]}


@router.get("/conversations/{conversation_id}/messages")
def messages(conversation_id: int, claims: dict = Depends(current_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT m.role,m.content,m.created_at FROM messages m JOIN conversations c ON c.id=m.conversation_id WHERE c.id=%s AND c.user_id=%s ORDER BY m.id", (conversation_id, uid(claims)))
        return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in cur.fetchall()]


@router.get("/history/messages")
def history(claims: dict = Depends(current_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT role,content,created_at,conversation_id FROM messages WHERE user_id=%s ORDER BY id", (uid(claims),))
        return [{"role": r[0], "content": r[1], "created_at": r[2], "conversation_id": r[3]} for r in cur.fetchall()]


@router.post("/conversations/{conversation_id}/rename")
def rename(conversation_id: int, body: dict, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("UPDATE conversations SET title=%s WHERE id=%s AND user_id=%s", (body["title"], conversation_id, uid(claims)))
    return {"message": "Conversation renamed"}


@router.delete("/conversations/{conversation_id}")
def delete(conversation_id: int, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM conversations WHERE id=%s AND user_id=%s", (conversation_id, uid(claims)))
    return {"message": "Conversation deleted"}


@router.post("/activity")
def activity(body: ActivityCreate, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("INSERT INTO user_activity (user_id,action_type,page_name,details) VALUES (%s,%s,%s,%s)", (uid(claims), body.action_type, body.page_name, redact_sensitive_data(body.details)))
    return {"message": "Activity recorded"}


@router.get("/admin/users")
def admin_users(_claims: dict = Depends(admin_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT id,username,email,is_admin,created_at FROM users ORDER BY id")
        return [{"id": r[0], "username": r[1], "email": r[2], "is_admin": r[3], "created_at": r[4]} for r in cur.fetchall()]


@router.get("/admin/messages")
def admin_messages(user_id: int, claims: dict = Depends(current_claims)):
    target_id = permitted_user(user_id, claims)
    with db_cursor() as cur:
        cur.execute("SELECT role,content,created_at FROM messages WHERE user_id=%s ORDER BY id", (target_id,))
        return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in cur.fetchall()]


@router.get("/admin/moods")
def admin_moods(user_id: int, claims: dict = Depends(current_claims)):
    target_id = permitted_user(user_id, claims)
    with db_cursor() as cur:
        cur.execute("SELECT mood,created_at FROM mood WHERE user_id=%s ORDER BY id", (target_id,))
        return [{"mood": r[0], "created_at": r[1]} for r in cur.fetchall()]


@router.get("/admin/journals")
def admin_journals(user_id: int, claims: dict = Depends(current_claims)):
    target_id = permitted_user(user_id, claims)
    with db_cursor() as cur:
        cur.execute("SELECT entry,created_at FROM journal WHERE user_id=%s ORDER BY id DESC", (target_id,))
        return [{"entry": r[0], "created_at": r[1]} for r in cur.fetchall()]


@router.get("/admin/activity")
def admin_activity(user_id: int, limit: int = 50, claims: dict = Depends(current_claims)):
    target_id = permitted_user(user_id, claims)
    with db_cursor() as cur:
        cur.execute("SELECT action_type,page_name,details,timestamp FROM user_activity WHERE user_id=%s ORDER BY timestamp DESC LIMIT %s", (target_id, limit))
        return [{"action_type": r[0], "page_name": r[1], "details": r[2], "timestamp": r[3]} for r in cur.fetchall()]
