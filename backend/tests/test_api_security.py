from fastapi.testclient import TestClient

from app.main import app


def test_protected_mood_requires_authentication():
    client = TestClient(app)
    response = client.get("/mood")
    assert response.status_code == 401
