"""Privacy-preserving redaction for text sent to models or stored in chat."""

from __future__ import annotations

import re

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?92|0)\s?(?:3\d{2})[-\s]?\d{3}[-\s]?\d{4}(?!\w)|(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)")
CNIC_RE = re.compile(r"(?<!\w)\d{5}[-\s]?\d{7}[-\s]?\d(?!\w)")


def redact_sensitive_data(text: str) -> str:
    """Replace common email, phone, and Pakistani CNIC patterns.

    This is a privacy guard, not a claim of perfect de-identification. The
    original text should never be logged; only the redacted text should be
    passed to model/storage code.
    """
    if not isinstance(text, str):
        return ""
    redacted = EMAIL_RE.sub("[EMAIL REDACTED]", text)
    redacted = CNIC_RE.sub("[CNIC REDACTED]", redacted)
    return PHONE_RE.sub("[PHONE REDACTED]", redacted)
