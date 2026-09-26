# backend/app/api/chat_routes.py
# MODIFIED: Updated /chat endpoint to pass request.history to
# generate_chat_response() for multi-turn conversation memory.
# MODIFIED (Part 2): Added crisis/severity fields to /chat response.

from fastapi import APIRouter

from app.database.schemas import (
    PredictionRequest,
    PredictionResponse,
    ChatRequest,
    ChatResponse,
)

from app.services.privacy import redact_sensitive_data

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):
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


@router.post("/chat")
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
    )

    if result.get("crisis"):
        # Crisis path: LLM was bypassed; no emotion/stress/depression scores
        return {
            "response":              result["response"],
            "crisis":                True,
            "severity":              result["severity"],
            "emotion":               None,
            "emotion_confidence":    0.0,
            "stress":                None,
            "stress_confidence":     0.0,
            "depression":            None,
            "depression_confidence": 0.0,
        }

    # Normal path: full enriched result
    return {
        "response":              result["response"],
        "crisis":                False,
        "severity":              None,
        "emotion":               result["emotion"],
        "emotion_confidence":    result["emotion_confidence"],
        "stress":                result["stress"],
        "stress_confidence":     result["stress_confidence"],
        "depression":            result["depression"],
        "depression_confidence": result["depression_confidence"],
    }
