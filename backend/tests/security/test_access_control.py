# -*- coding: utf-8 -*-
"""API-level ownership regression tests using two separately authenticated users.

The API is exercised with TestClient and an isolated in-memory DB adapter; this
is deterministic integration coverage, not a replacement for PostgreSQL tests.
"""
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.api import application_routes, journal_routes, mood_routes
from app.main import app
from app.services import auth_service


class MemoryDB:
    def __init__(self):
        self.conversations = {}
        self.messages = []
        self.moods = []
        self.journals = []
        self.next_id = 1

    def cursor(self, commit=False):
        return MemoryCursor(self)


class MemoryCursor:
    def __init__(self, db):
        self.db = db
        self.one = None
        self.all = []

    def execute(self, sql, params=()):
        query = " ".join(sql.lower().split())
        self.one, self.all = None, []
        if query.startswith("insert into conversations"):
            user_id, title = params
            row_id = self.db.next_id; self.db.next_id += 1
            self.db.conversations[row_id] = {"id": row_id, "user_id": user_id, "title": title}
            self.one = (row_id, title, "created")
        elif query.startswith("select id from conversations where id=%s and user_id=%s"):
            record = self.db.conversations.get(params[0])
            self.one = (record["id"],) if record and record["user_id"] == params[1] else None
        elif query.startswith("insert into messages"):
            user_id, role, content, conversation_id = params
            row_id = self.db.next_id; self.db.next_id += 1
            self.db.messages.append({"id": row_id, "user_id": user_id, "conversation_id": conversation_id, "role": role, "content": content})
            self.one = (row_id, "created")
        elif query.startswith("select m.role,m.content,m.created_at from messages m join conversations"):
            conversation_id, user_id = params
            conv = self.db.conversations.get(conversation_id)
            if conv and conv["user_id"] == user_id:
                self.all = [(m["role"], m["content"], "created") for m in self.db.messages if m["conversation_id"] == conversation_id]
        elif query.startswith("select role,content,created_at,conversation_id from messages where user_id=%s"):
            self.all = [(m["role"], m["content"], "created", m["conversation_id"]) for m in self.db.messages if m["user_id"] == params[0]]
        elif query.startswith("update conversations set title=%s where id=%s and user_id=%s"):
            title, conversation_id, user_id = params
            conv = self.db.conversations.get(conversation_id)
            if conv and conv["user_id"] == user_id:
                conv["title"] = title
        elif query.startswith("delete from conversations where id=%s and user_id=%s"):
            conversation_id, user_id = params
            conv = self.db.conversations.get(conversation_id)
            if conv and conv["user_id"] == user_id:
                del self.db.conversations[conversation_id]
                self.db.messages = [m for m in self.db.messages if m["conversation_id"] != conversation_id]
        elif query.startswith("insert into mood"):
            user_id, mood = params
            self.db.moods.append((user_id, mood, "created"))
            self.one = (len(self.db.moods), mood, "created")
        elif query.startswith("select mood,created_at from mood"):
            self.all = [(mood, created) for uid, mood, created in self.db.moods if uid == params[0]]
        elif query.startswith("insert into journal"):
            user_id, entry = params
            self.db.journals.append((user_id, entry, "created"))
            self.one = (len(self.db.journals), entry, "created")
        elif query.startswith("select entry,created_at from journal"):
            self.all = [(entry, created) for uid, entry, created in self.db.journals if uid == params[0]]
        else:
            raise AssertionError(f"Test DB does not implement SQL: {sql}")

    def fetchone(self):
        return self.one

    def fetchall(self):
        return self.all


@pytest.fixture
def two_users(monkeypatch):
    db = MemoryDB()

    @contextmanager
    def db_cursor(commit=False):
        yield db.cursor(commit)

    monkeypatch.setattr(application_routes, "db_cursor", db_cursor)
    monkeypatch.setattr(mood_routes, "db_cursor", db_cursor)
    monkeypatch.setattr(journal_routes, "db_cursor", db_cursor)
    monkeypatch.setattr("app.main.init_pool", lambda: None)
    monkeypatch.setattr("app.main.close_pool", lambda: None)
    users = {"a@example.test": (101, "user-a"), "b@example.test": (202, "user-b")}

    def fake_register(username, email, password):
        uid, email = users[email]
        return {"id": uid, "username": username, "email": email, "is_admin": False}

    def fake_login(email, password):
        uid, username = users[email]
        from app.core.security import create_access_token
        return {"id": uid, "username": username, "email": email, "is_admin": False,
                "access_token": create_access_token(uid, email)}

    monkeypatch.setattr(auth_service, "register", fake_register)
    monkeypatch.setattr(auth_service, "login", fake_login)
    with TestClient(app) as client:
        tokens = {}
        for email in users:
            response = client.post("/auth/register", json={"username": email.split("@")[0], "email": email, "password": "test-password-123"})
            assert response.status_code == 200
            login = client.post("/auth/login", json={"email": email, "password": "test-password-123"})
            assert login.status_code == 200
            tokens[email] = login.json()["access_token"]
        yield client, db, tokens


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_user_cannot_read_or_manipulate_another_users_conversation_or_history(two_users):
    client, db, tokens = two_users
    token_a, token_b = tokens["a@example.test"], tokens["b@example.test"]
    created = client.post("/conversations", json={"title": "B private session"}, headers=_auth(token_b))
    conversation_id = created.json()["id"]
    assert client.post(f"/conversations/{conversation_id}/messages", json={"role": "user", "content": "private B text"}, headers=_auth(token_b)).status_code == 200

    for method, url, kwargs in [
        ("get", f"/conversations/{conversation_id}/messages", {}),
        ("post", f"/conversations/{conversation_id}/messages", {"json": {"role": "user", "content": "attack"}}),
        ("post", f"/conversations/{conversation_id}/rename", {"json": {"title": "hijacked"}}),
        ("delete", f"/conversations/{conversation_id}", {}),
    ]:
        response = getattr(client, method)(url, headers=_auth(token_a), **kwargs)
        assert response.status_code in (403, 404), f"{method.upper()} {url} returned {response.status_code}: {response.text}"

    a_history = client.get("/history/messages", headers=_auth(token_a))
    assert a_history.status_code == 200
    assert "private B text" not in a_history.text
    assert conversation_id in db.conversations  # failed delete did not mutate B's session
    assert db.conversations[conversation_id]["title"] == "B private session"


def test_mood_and_journal_lists_are_scoped_to_authenticated_user(two_users):
    client, _db, tokens = two_users
    token_a, token_b = tokens["a@example.test"], tokens["b@example.test"]
    client.post("/mood", json={"mood": "private-A-mood"}, headers=_auth(token_a))
    client.post("/journal", json={"entry": "private-A-journal"}, headers=_auth(token_a))
    b_moods = client.get("/mood", headers=_auth(token_b))
    b_journals = client.get("/journal", headers=_auth(token_b))
    assert b_moods.status_code == b_journals.status_code == 200
    assert "private-A-mood" not in b_moods.text
    assert "private-A-journal" not in b_journals.text
