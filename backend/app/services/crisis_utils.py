# -*- coding: utf-8 -*-
"""
crisis_utils.py
===============
Thin adapter that bridges the existing crisis_detector + crisis_resources
modules into the single assess_crisis() function expected by rag_chat_service.

rag_chat_service imports:
    from .crisis_utils import assess_crisis

assess_crisis() returns:
    {
        "is_crisis": bool,
        "level":     str | None,   # "HIGH" | "MEDIUM" | "LOW" | None
        "response":  str,          # pre-written template (empty string if not a crisis)
        "language":  str,          # "english" | "roman_urdu" | "urdu"
    }
"""
from app.services.crisis_detector import detect_crisis, log_crisis_event
from app.services.crisis_resources import get_crisis_response


def assess_crisis(text: str, language: str = "english") -> dict:
    """
    Assess whether the user message contains a crisis indicator.

    Uses keyword-based detection (detect_crisis) and, if a crisis is
    found, fetches the appropriate pre-written helpline response
    (get_crisis_response) in the correct language.

    Args:
        text:     Raw user message.
        language: Pre-detected language ("english" / "roman_urdu" / "urdu").
                  Used to select the correct response template.

    Returns:
        dict with keys:
            is_crisis (bool)       — True if any crisis phrase was found.
            level     (str | None) — "HIGH", "MEDIUM", "LOW", or None.
            response  (str)        — Pre-written crisis response, or "" if not a crisis.
            language  (str)        — Detected language passed through.
    """
    result = detect_crisis(text)

    if not result["is_crisis"]:
        return {
            "is_crisis": False,
            "level":     None,
            "response":  "",
            "language":  language,
        }

    severity = result["severity"]

    # Log the event (privacy-safe — matched keywords only, never full message)
    log_crisis_event(
        severity=severity,
        matched_phrases=result["matched_phrases"],
        language=language,
    )

    # Use the language passed in from the main language detector (more
    # accurate than the lightweight internal one in crisis_detector).
    response_text = get_crisis_response(severity=severity, language=language)

    return {
        "is_crisis": True,
        "level":     severity,
        "response":  response_text,
        "language":  language,
    }
