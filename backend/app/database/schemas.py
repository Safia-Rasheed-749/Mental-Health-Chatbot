from pydantic import BaseModel


class PredictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    emotion: str
    emotion_confidence: float

    stress: str
    stress_confidence: float

    depression: str
    depression_confidence: float