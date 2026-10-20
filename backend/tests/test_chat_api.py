# -*- coding: utf-8 -*-
from types import SimpleNamespace
import sys

from fastapi.testclient import TestClient

from app.main import app


def test_chat_api_returns_current_signals_separately_and_not_internal_context(monkeypatch):
    captured = {}

    def generate_chat_response(*, question, history):
        captured.update(question=question, history=history)
        return {
            "response": "Try one small step today.",
            "crisis": False,
            "severity": None,
            "language": "english",
            "speech_text": "",
            "emotion": "fear",
            "emotion_confidence": 81.2,
            "stress": "Stress",
            "stress_confidence": 77.3,
            "depression": "No Depression",
            "depression_confidence": 92.1,
            "context": "PRIVATE RETRIEVED PASSAGE",
            "mental_state": "DETECTED MENTAL STATE — internal only",
        }

    fake_service = SimpleNamespace(generate_chat_response=generate_chat_response)
    monkeypatch.setitem(sys.modules, "app.services.rag_chat_service", fake_service)
    client = TestClient(app)
    response = client.post("/chat", json={
        "message": "I am worried", "response_language": "english",
        "input_language": "english", "input_mode": "text",
        "history": [{"role": "user", "content": "Earlier message"}],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Try one small step today."
    assert data["emotion"] == "fear" and data["emotion_confidence"] == 81.2
    assert data["stress"] == "Stress" and data["stress_confidence"] == 77.3
    assert data["depression"] == "No Depression" and data["depression_confidence"] == 92.1
    assert "context" not in data and "mental_state" not in data
    assert captured["question"] == "I am worried"
    assert [(turn.role, turn.content) for turn in captured["history"]] == [("user", "Earlier message")]


def test_chat_api_keeps_crisis_response_without_fabricated_classifications(monkeypatch):
    fake_service = SimpleNamespace(generate_chat_response=lambda **kwargs: {
        "response": "Please contact emergency support now.", "crisis": True,
        "severity": "HIGH", "language": "english", "speech_text": "",
        "emotion": None, "emotion_confidence": None, "stress": None,
        "stress_confidence": None, "depression": None, "depression_confidence": None,
    })
    monkeypatch.setitem(sys.modules, "app.services.rag_chat_service", fake_service)
    response = TestClient(app).post("/chat", json={"message": "crisis test"})
    assert response.status_code == 200
    assert response.json()["crisis"] is True
    assert response.json()["stress"] is None
