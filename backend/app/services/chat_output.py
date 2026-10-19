# -*- coding: utf-8 -*-
"""Guard the user-facing answer boundary against internal prompt leakage."""

import re


_INTERNAL_OUTPUT_RE = re.compile(
    r"(?is)(?:DETECTED MENTAL STATE|\[\s*Chunk\s*\d+\s*\]|RETRIEVED (?:CONTEXT|KNOWLEDGE)|RAG CONTEXT|NO RELEVANT REFERENCE FOUND|NEWEST MESSAGE\s*:|SYSTEM (?:PROMPT|INSTRUCTIONS?)|CLASSIFICATION (?:RESULTS?|INSTRUCTIONS?)|\b(?:Emotion|Stress|Depression|Depression signal|Anxiety)\s*:\s*[^\n()]+\s*\(\s*\d+(?:\.\d+)?%\s*\)|\bconfidence\s*:\s*\d+(?:\.\d+)?%|internal only)"
)

_SAFE_FALLBACKS = {
    "english": "I’m here with you. What feels most important for us to focus on right now?",
    "roman_urdu": "Main aapki baat sun raha hoon. Is waqt aap kis baat par sab se pehle tawajjoh dena chahein ge?",
    "urdu": "میں آپ کی بات سن رہا ہوں۔ اس وقت آپ کس بات پر سب سے پہلے توجہ دینا چاہیں گے؟",
}


def clean_user_response(text: str, language: str, retrieved_context: str = "", question: str = "") -> str:
    """Return validated conversational text or a language-matched safe fallback."""
    cleaned = (text or "").strip()
    echoes_retrieval = False
    if retrieved_context:
        for passage in retrieved_context.split("\n\n"):
            passage = passage.strip()
            if len(passage) >= 80 and passage in cleaned:
                echoes_retrieval = True
                break
    if not cleaned or _INTERNAL_OUTPUT_RE.search(cleaned) or echoes_retrieval:
        if question:
            from app.services.response_generation import concern_fallback
            return concern_fallback(question, language)
        return _SAFE_FALLBACKS.get(language, _SAFE_FALLBACKS["english"])
    return cleaned
