"""
crisis_detector.py
==================
Part 1 of the Crisis Guardrail system for the AI Mental Health Chatbot FYP.

Responsibilities:
    - Keyword-based crisis detection across three severity levels
    - Language detection (English / Roman Urdu / Urdu script)
    - Privacy-safe crisis event logging (matched keywords only, never full message)

Does NOT:
    - Call the LLM
    - Modify any existing service
    - Depend on any third-party package (standard library only)
"""

import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

# __file__ = backend/app/services/crisis_detector.py
# parents[0] = services/   parents[1] = app/   parents[2] = backend/
BASE_DIR = Path(__file__).resolve().parents[2]   # → backend/
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "crisis_events.log"

# ─────────────────────────────────────────────────────────────────────────────
# Keyword Categories
# ─────────────────────────────────────────────────────────────────────────────

HIGH_SEVERITY_PHRASES = [
    # English
    "kill myself",
    "end my life",
    "want to die",
    "commit suicide",
    "end it all",
    "suicide",
    "hang myself",
    "overdose",
    "want to kill myself",
    # Roman Urdu
    "khudkushi",
    "khud kushi",
    "marna chahta",
    "marna chahti",
    "zindagi khatam",
    "jaan dena",
    "jaan de dun",
]

MEDIUM_SEVERITY_PHRASES = [
    # English
    "no reason to live",
    "better off dead",
    "can't go on",
    "cannot go on",
    "no point in living",
    "don't want to be here",
    "do not want to be here",
    # Roman Urdu
    "jeena nahi chahta",
    "jeena nahi chahti",
    "zindagi mein koi faida nahi",
    "khatam kar dun",
]

LOW_SEVERITY_PHRASES = [
    # English
    "tired of living",
    "don't want to wake up",
    "do not want to wake up",
    "wish i could sleep forever",
    "done with life",
    # Roman Urdu
    "zindagi se thak gaya",
    "zindagi se thak gayi",
    "marna behtar hai",
]

# Roman Urdu indicator words used for language detection
_ROMAN_URDU_INDICATORS = {
    "khudkushi", "khud", "kushi", "marna", "chahta", "chahti",
    "jeena", "zindagi", "jaan", "khatam", "dena",
}

# Urdu script Unicode range
_URDU_SCRIPT_RE = re.compile(
    r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]"
)


# ─────────────────────────────────────────────────────────────────────────────
# Language Detection (lightweight, internal use)
# ─────────────────────────────────────────────────────────────────────────────

def _detect_language(text: str) -> str:
    """
    Detect language of the input text.

    Returns:
        "urdu"       — Urdu Unicode script characters found
        "roman_urdu" — Roman Urdu indicator words found
        "english"    — default
    """
    if _URDU_SCRIPT_RE.search(text):
        return "urdu"

    words = set(re.findall(r"[a-zA-Z]+", text.lower()))
    if words & _ROMAN_URDU_INDICATORS:
        return "roman_urdu"

    return "english"


# ─────────────────────────────────────────────────────────────────────────────
# Core Detection
# ─────────────────────────────────────────────────────────────────────────────

def detect_crisis(text: str) -> dict:
    """
    Detect crisis indicators in the user message.

    Checks HIGH → MEDIUM → LOW (in that order).
    Returns the highest severity found.

    Args:
        text: Raw user message.

    Returns:
        dict with keys:
            is_crisis       (bool)              — True if any crisis phrase found
            severity        (str | None)        — "HIGH", "MEDIUM", "LOW", or None
            matched_phrases (list[str])         — all matched phrases
            language        (str)               — "english", "roman_urdu", or "urdu"
    """
    _empty = {
        "is_crisis":       False,
        "severity":        None,
        "matched_phrases": [],
        "language":        "english",
    }

    if not text or not isinstance(text, str):
        return _empty

    normalised = text.lower().strip()
    language   = _detect_language(text)

    matched: list[str] = []
    severity: Optional[str] = None

    # Check HIGH first — stop at first positive level
    for phrase in HIGH_SEVERITY_PHRASES:
        if phrase in normalised:
            matched.append(phrase)
            severity = "HIGH"

    if not matched:
        for phrase in MEDIUM_SEVERITY_PHRASES:
            if phrase in normalised:
                matched.append(phrase)
                severity = "MEDIUM"

    if not matched:
        for phrase in LOW_SEVERITY_PHRASES:
            if phrase in normalised:
                matched.append(phrase)
                severity = "LOW"

    return {
        "is_crisis":       bool(matched),
        "severity":        severity,
        "matched_phrases": matched,
        "language":        language,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Crisis Event Logging
# ─────────────────────────────────────────────────────────────────────────────

def log_crisis_event(
    severity:        str,
    matched_phrases: list,
    language:        str,
) -> None:
    """
    Append a privacy-safe crisis event to the log file.

    PRIVACY: Only matched keywords are logged — the user's full message
    is NEVER written to disk.

    Log format:
        [YYYY-MM-DD HH:MM:SS] SEVERITY=HIGH | MATCHED="phrase1, phrase2" | LANG=english

    Args:
        severity:        "HIGH", "MEDIUM", or "LOW"
        matched_phrases: List of matched keyword phrases
        language:        "english", "roman_urdu", or "urdu"
    """
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        timestamp     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        phrases_str   = ", ".join(matched_phrases)
        log_line      = (
            f"[{timestamp}] SEVERITY={severity} | "
            f'MATCHED="{phrases_str}" | '
            f"LANG={language}\n"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)

    except Exception as exc:
        # Logging must never crash the main service
        print(f"[crisis_detector] Warning: could not write to log — {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Standalone Test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_inputs = [
        # (description, text)
        ("High — English suicidal intent",  "I want to kill myself tonight"),
        ("High — English suicide keyword",  "I have been thinking about suicide all day"),
        ("High — Roman Urdu",               "mujhe khudkushi karna hai, zindagi khatam karni hai"),
        ("Normal — English",                "I am feeling very sad and lonely today"),
        ("Normal — Roman Urdu",             "mujhe bohat bura lag raha hai lekin main theek ho jaunga"),
    ]

    print("=" * 65)
    print("Crisis Detector — Standalone Test")
    print("=" * 65)

    for description, text in test_inputs:
        result = detect_crisis(text)
        print(f"\n[{description}]")
        print(f"  Input    : {text}")
        print(f"  is_crisis: {result['is_crisis']}")
        print(f"  severity : {result['severity']}")
        print(f"  matched  : {result['matched_phrases']}")
        print(f"  language : {result['language']}")

        if result["is_crisis"]:
            log_crisis_event(
                severity=result["severity"],
                matched_phrases=result["matched_phrases"],
                language=result["language"],
            )

    print(f"\n{'=' * 65}")
    print(f"Log file location: {LOG_FILE}")

    if LOG_FILE.exists():
        print("Log file created successfully. Contents:")
        print(LOG_FILE.read_text(encoding="utf-8"))
    else:
        print("No crisis events detected — log file not created.")
