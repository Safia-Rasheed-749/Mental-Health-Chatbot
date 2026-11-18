import sys
import types

from fastapi.testclient import TestClient

from app.main import app


def test_demo_chat_is_public_and_uses_shared_response_service(monkeypatch):
    calls = []

    def generate_chat_response(**kwargs):
        calls.append(kwargs)
        return {
            "response": "A thoughtful response from the shared chat service.",
            "crisis": False,
            "crisis_level": "none",
        }

    service = types.ModuleType("app.services.rag_chat_service")
    service.generate_chat_response = generate_chat_response
    monkeypatch.setitem(sys.modules, "app.services.rag_chat_service", service)

    response = TestClient(app).post(
        "/demo/chat",
        json={
            "message": "I am worried about my exams.",
            "history": [
                {"role": "user", "content": "My exams are next week."},
                {"role": "assistant", "content": "Which subject worries you most?"},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "response": "A thoughtful response from the shared chat service.",
        "crisis": False,
        "severity": None,
    }
    assert calls[0]["question"] == "I am worried about my exams."
    assert [
        message.model_dump() for message in calls[0]["history"]
    ] == [
        {"role": "user", "content": "My exams are next week."},
        {"role": "assistant", "content": "Which subject worries you most?"},
    ]
    assert calls[0]["user_id"] is None


def test_regular_chat_route_still_requires_authentication():
    response = TestClient(app).post(
        "/chat",
        json={"message": "I am worried about my exams."},
    )

    assert response.status_code == 401
