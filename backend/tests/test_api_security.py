# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.main import app


def test_protected_mood_requires_authentication():
    client = TestClient(app)
    response = client.get("/mood")
    assert response.status_code == 401


def test_classifier_predictions_are_not_available_to_unauthenticated_users():
    client = TestClient(app)
    response = client.post("/predict", json={"text": "I feel stressed"})
    assert response.status_code == 401


def test_access_token_signature_is_stable_within_process():
    token = create_access_token(123, "test@example.invalid")
    assert decode_access_token(token)["sub"] == "123"
    assert settings.jwt_key() == settings.jwt_key()
