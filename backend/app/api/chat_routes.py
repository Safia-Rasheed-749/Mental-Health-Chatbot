# -*- coding: utf-8 -*-
# backend/app/api/chat_routes.py
# MODIFIED: Updated /chat endpoint to pass request.history to
# generate_chat_response() for multi-turn conversation memory.
# MODIFIED (Part 2): Added crisis/severity fields to /chat response.

from fastapi import APIRouter, Depends

from app.database.schemas import (
    PredictionRequest,
    PredictionResponse,
    ChatRequest,
    ChatResponse,
)

from app.services.privacy import redact_sensitive_data
from app.api.deps import admin_claims

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest, _claims: dict = Depends(admin_claims)):
    from app.services.chat_service import analyze_text
    result = analyze_text(request.text)

    return PredictionResponse(

        emotion=result["emotion"],
        emotion_confidence=result["emotion_confidence"],

        stress=result["stress"],
        stress_confidence=result["stress_confidence"],

        depression=result["depression"],
        depression_confidence=result["depression_confidence"]

    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Load the AI/RAG stack only when chat is requested.  Those modules load
    # large local models during import; importing them at API startup prevents
    # unrelated endpoints such as authentication from starting when model
    # assets are not installed yet.
    from app.services.rag_chat_service import generate_chat_response

    # Pass history (None-safe — format_history handles None/empty gracefully)
    result = generate_chat_response(
        question=request.message,
        history=request.history or [],
        response_language=request.response_language,
        input_language=request.input_language,
        input_mode=request.input_mode,
    )

    if result.get("crisis"):
        # Crisis path: LLM was bypassed; no emotion/stress/depression scores
        return {
            "response":              result["response"],
            "crisis":                True,
            "severity":              result["severity"],
            "language": result.get("language"),
            "speech_text": result.get("speech_text", result["response"]),
            "emotion": None,
            "emotion_confidence": None,
            "stress": None,
            "stress_confidence": None,
            "depression": None,
            "depression_confidence": None,
        }

    # Normal path: full enriched result
    return {
        "response":              result["response"],
        "crisis":                False,
        "severity":              None,
        "language": result.get("language"),
        "speech_text": result.get("speech_text", result["response"]),
        "emotion": result.get("emotion"),
        "emotion_confidence": result.get("emotion_confidence"),
        "stress": result.get("stress"),
        "stress_confidence": result.get("stress_confidence"),
        "depression": result.get("depression"),
        "depression_confidence": result.get("depression_confidence"),
    }
