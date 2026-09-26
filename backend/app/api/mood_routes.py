from fastapi import APIRouter, Depends

from app.api.deps import current_claims
from app.database.connection import db_cursor
from app.database.schemas import MoodCreate

router = APIRouter(prefix="/mood", tags=["Mood"])


@router.post("")
def add_mood(request: MoodCreate, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("INSERT INTO mood (user_id,mood) VALUES (%s,%s) RETURNING id,mood,created_at", (int(claims["sub"]), request.mood))
        row = cur.fetchone()
    return {"id": row[0], "mood": row[1], "created_at": row[2]}


@router.get("")
def get_moods(claims: dict = Depends(current_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT mood,created_at FROM mood WHERE user_id=%s ORDER BY id", (int(claims["sub"]),))
        return [{"mood": row[0], "created_at": row[1]} for row in cur.fetchall()]
