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
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    # LLM-generated reply
    response: str

    # Emotion / stress / depression detection results
    # (included so the frontend can display or act on them)
    emotion: str
    emotion_confidence: float

    stress: str
    stress_confidence: float

    depression: str
    depression_confidence: float