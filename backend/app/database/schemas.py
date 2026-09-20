# MODIFIED: Added ChatMessage schema and updated ChatRequest with optional
# history field for multi-turn conversation memory support.
# Backward compatible — history defaults to empty list.

from typing import List, Optional
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
class ChatMessage(BaseModel):
    """A single turn in conversation history."""
    role: str       # "user" or "assistant"
    content: str    # message text


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []  # previous turns; empty = stateless


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