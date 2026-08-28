from fastapi import APIRouter

from app.database.schemas import (
    PredictionRequest,
    PredictionResponse,
    ChatRequest,
    ChatResponse

)

# from app.services.chat_service import analyze_text
from app.services.rag_chat_service import generate_chat_response

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
@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    result = generate_chat_response(request.message)

    return ChatResponse(
        response=result["response"],

        emotion=result["emotion"],
        emotion_confidence=result["emotion_confidence"],

        stress=result["stress"],
        stress_confidence=result["stress_confidence"],

        depression=result["depression"],
        depression_confidence=result["depression_confidence"],
    )