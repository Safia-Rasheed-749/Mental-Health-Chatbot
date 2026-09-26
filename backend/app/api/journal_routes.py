from fastapi import APIRouter, Depends

from app.api.deps import current_claims
from app.database.connection import db_cursor
from app.database.schemas import JournalCreate

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.post("")
def add_journal(request: JournalCreate, claims: dict = Depends(current_claims)):
    with db_cursor(commit=True) as cur:
        cur.execute("INSERT INTO journal (user_id,entry) VALUES (%s,%s) RETURNING id,entry,created_at", (int(claims["sub"]), request.entry))
        row = cur.fetchone()
    return {"id": row[0], "entry": row[1], "created_at": row[2]}


@router.get("")
def get_journals(claims: dict = Depends(current_claims)):
    with db_cursor() as cur:
        cur.execute("SELECT entry,created_at FROM journal WHERE user_id=%s ORDER BY id DESC", (int(claims["sub"]),))
        return [{"entry": row[0], "created_at": row[1]} for row in cur.fetchall()]
