# -*- coding: utf-8 -*-
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
    response_language: str = "auto"
    input_language: Optional[str] = None
    input_mode: str = "text"


class ChatResponse(BaseModel):
    response: str
    crisis: bool = False
    severity: Optional[str] = None
    language: Optional[str] = None
    speech_text: Optional[str] = None
    # Per-current-message model signals for the separate, caveated UI panel.
    emotion: Optional[str] = None
    emotion_confidence: Optional[float] = None
    stress: Optional[str] = None
    stress_confidence: Optional[float] = None
    depression: Optional[str] = None
    depression_confidence: Optional[float] = None


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ResetRequest(BaseModel):
    email: str
    code: str
    new_password: str


class MoodCreate(BaseModel):
    mood: str


class JournalCreate(BaseModel):
    entry: str


class ActivityCreate(BaseModel):
    action_type: str
    page_name: str
    details: str = ""
