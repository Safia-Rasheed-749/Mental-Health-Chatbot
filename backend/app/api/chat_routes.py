from fastapi import APIRouter

from app.database.schemas import (
    PredictionRequest,
    PredictionResponse
)

from app.services.chat_service import analyze_text


router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):

    result = analyze_text(request.text)

    return PredictionResponse(

        emotion=result["emotion"],
        emotion_confidence=result["emotion_confidence"],

        stress=result["stress"],
        stress_confidence=result["stress_confidence"],

        depression=result["depression"],
        depression_confidence=result["depression_confidence"]

    )