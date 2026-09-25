"""
=========================================================
Response Validator
Project : AI Mental Health Chatbot (FYP)

Purpose:
    After the LLM generates a response, this module checks
    whether the response actually matches the expected
    language and quality rules.

    For Roman Urdu:
        - Must NOT contain Urdu Unicode script
        - Must NOT contain forbidden Hindi/Sanskrit words
        - Must NOT be English-heavy (>70% English words)

    For Urdu script:
        - Must contain Urdu Unicode characters
        - Must NOT be mostly Latin/English

    For English:
        - Must NOT contain Urdu Unicode script

    If validation fails, a correction prompt is built and
    the caller can regenerate once.

Validation result:
    {
        "valid":    bool,
        "reasons":  list[str],   # why it failed (empty if valid)
        "language": str          # language that was expected
    }
=========================================================
"""

import re
from typing import Optional

from app.ai.llm.roman_urdu_style import FORBIDDEN_WORDS, MAX_REGENERATE_ATTEMPTS

# =====================================================
# Script Detection Helpers
# =====================================================

# Urdu Unicode ranges (Arabic script blocks)
_URDU_RE = re.compile(
    r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]"
)


def contains_urdu_script(text: str) -> bool:
    """Return True if text contains any Urdu Unicode characters."""
    return bool(_URDU_RE.search(text))


def urdu_script_ratio(text: str) -> float:
    """Return fraction of characters that are Urdu Unicode."""
    if not text:
        return 0.0
    urdu_chars = len(_URDU_RE.findall(text))
    return urdu_chars / len(text)


def latin_word_ratio(text: str) -> float:
    """Return fraction of whitespace-separated tokens that are Latin words."""
    tokens = text.split()
    if not tokens:
        return 0.0
    latin = sum(1 for t in tokens if re.match(r"^[a-zA-Z]+$", t))
    return latin / len(tokens)


# =====================================================
# Forbidden Word Check
# =====================================================

def find_forbidden_words(text: str) -> list[str]:
    """
    Return list of FORBIDDEN_WORDS found in the response (case-insensitive).

    Two passes:
    1. Exact whole-word match  (e.g. "samasya")
    2. Normalised match — collapse repeated vowels so "aavashyakta"
       and "avashyakta" both match the same normalised form.
       This catches LLM spelling variations like aa→a, oo→o, ee→e.
    """
    text_lower = text.lower()

    # Pre-normalise text: collapse double vowels  aa→a, oo→o, ee→e, ii→i
    def _normalise(s: str) -> str:
        s = re.sub(r"aa+", "a", s)
        s = re.sub(r"oo+", "o", s)
        s = re.sub(r"ee+", "e", s)
        s = re.sub(r"ii+", "i", s)
        return s

    text_normalised = _normalise(text_lower)

    found = []
    seen  = set()   # avoid duplicate entries in result

    for word in FORBIDDEN_WORDS:
        word_lower = word.lower()

        # Pass 1 — exact word boundary match
        pattern_exact = r"\b" + re.escape(word_lower) + r"\b"
        if re.search(pattern_exact, text_lower) and word_lower not in seen:
            found.append(word)
            seen.add(word_lower)
            continue

        # Pass 2 — normalised match (handles aa/a, oo/o variations)
        word_norm = _normalise(word_lower)
        pattern_norm = r"\b" + re.escape(word_norm) + r"\b"
        if re.search(pattern_norm, text_normalised) and word_lower not in seen:
            found.append(word)
            seen.add(word_lower)

    return found


# =====================================================
# Per-Language Validators
# =====================================================

def _validate_roman_urdu(response: str) -> dict:
    """
    Check a Roman Urdu response.

    Fails if:
        - Contains Urdu Unicode script
        - Contains forbidden Hindi vocabulary
        - Is English-heavy (>70 % of tokens are pure Latin words
          AND none of the known Roman Urdu markers are present)
    """
    reasons = []

    # 1. Must not contain Urdu script
    if contains_urdu_script(response):
        reasons.append(
            "Response contains Urdu Unicode script but Roman Urdu (Latin letters) was expected."
        )

    # 2. Must not use forbidden Hindi/Sanskrit words
    bad = find_forbidden_words(response)
    if bad:
        reasons.append(
            f"Response contains formal Hindi/Sanskrit vocabulary that sounds unnatural "
            f"in Pakistani Roman Urdu: {', '.join(bad)}"
        )

    # 3. Must not be purely English (no Roman Urdu markers at all)
    # Important: English words mixed INTO Roman Urdu are ALLOWED.
    # This check only fires when the response has NO Urdu vocabulary
    # whatsoever — meaning the LLM responded fully in English.
    roman_urdu_markers = {
        "aap", "mujhe", "mujhy", "bohat", "bht", "udaas", "udas",
        "pareshan", "mehsoos", "fikr", "yahan", "hoon", "hain",
        "aapko", "takleef", "madad", "dil", "baat", "afsos",
        "hai", "hon", "lekin", "aur", "nahi", "kya", "kyun",
        "lagta", "lagti", "hua", "hui", "raha", "rahi",
        "theek", "achha", "mushkil", "samajh", "sunna",
        "main", "mera", "meri", "ghar", "zindagi",
    }
    words_lower = set(re.findall(r"[a-z]+", response.lower()))
    has_ru_markers = bool(words_lower & roman_urdu_markers)

    # Only flag as English-heavy if there are truly NO Roman Urdu words at all
    if not has_ru_markers:
        reasons.append(
            "Response appears to be fully in English with no Roman Urdu vocabulary detected. "
            "Please respond in Roman Urdu (Urdu words in Latin letters). "
            "English words like stress, anxiety, family, okay are allowed within Roman Urdu."
        )

    return {"valid": len(reasons) == 0, "reasons": reasons, "language": "roman_urdu"}


def _validate_urdu(response: str) -> dict:
    """
    Check a Urdu script response.

    Fails if:
        - Contains fewer than 10 % Urdu Unicode characters
          (meaning the model responded in Latin/English instead)
    """
    reasons = []
    ratio = urdu_script_ratio(response)
    if ratio < 0.10:
        reasons.append(
            f"Response should be in Urdu script but only {ratio:.0%} of characters "
            "are Urdu Unicode. The model may have responded in English or Roman Urdu."
        )
    return {"valid": len(reasons) == 0, "reasons": reasons, "language": "urdu"}


def _validate_english(response: str) -> dict:
    """
    Check an English response.

    Fails if:
        - Contains Urdu Unicode script (wrong language entirely)
    """
    reasons = []
    if contains_urdu_script(response):
        reasons.append(
            "Response contains Urdu Unicode script but an English response was expected."
        )
    return {"valid": len(reasons) == 0, "reasons": reasons, "language": "english"}


# =====================================================
# Public Validation Entry Point
# =====================================================

def validate_response(response: str, language: str) -> dict:
    """
    Validate a generated response against the expected language.

    Args:
        response: The raw LLM-generated text.
        language: One of "english", "roman_urdu", "urdu".

    Returns:
        {
            "valid":    bool,
            "reasons":  list[str],
            "language": str
        }
    """
    if not response or not response.strip():
        return {
            "valid": False,
            "reasons": ["Response is empty."],
            "language": language,
        }

    validators = {
        "roman_urdu": _validate_roman_urdu,
        "urdu":       _validate_urdu,
        "english":    _validate_english,
    }

    validator_fn = validators.get(language, _validate_english)
    return validator_fn(response)


# =====================================================
# Correction Prompt Builder
# =====================================================

def build_correction_prompt(
    original_question: str,
    bad_response: str,
    validation_result: dict,
) -> str:
    """
    Build a correction instruction to send back to the LLM
    when the first response fails validation.

    Args:
        original_question:  The user's original message.
        bad_response:       The LLM's failed response.
        validation_result:  Output of validate_response().

    Returns:
        A plain-text correction prompt string.
    """
    language  = validation_result["language"]
    reasons   = validation_result["reasons"]
    reason_str = "\n".join(f"  - {r}" for r in reasons)

    if language == "roman_urdu":
        return (
            f"The following response has quality issues:\n"
            f"---\n{bad_response}\n---\n\n"
            f"Problems found:\n{reason_str}\n\n"
            f"Please rewrite the response for this user message:\n"
            f"\"{original_question}\"\n\n"
            f"Rules for the rewrite:\n"
            f"1. Write in Roman Urdu — Urdu language using Latin/English letters.\n"
            f"2. Do NOT use Urdu Unicode script (Arabic letters).\n"
            f"3. Do NOT use formal Hindi/Sanskrit words:\n"
            f"   BANNED: samasya, nivaran, peeda, sujhav, vyakti, saksham,\n"
            f"           parivaar, sahayata, samay, prayas, anubhav, vichar.\n"
            f"4. ALLOWED English words inside Roman Urdu (these are fine):\n"
            f"   stress, anxiety, family, member, support, okay, feel,\n"
            f"   comfortable, depression, mood, help, talk.\n"
            f"5. Use natural Pakistani words: aap, mujhe, bohat, udaas,\n"
            f"   pareshan, mehsoos, fikr, madad, dil, baat, ghar waale.\n"
            f"6. Keep it 2 to 4 sentences, warm and conversational.\n"
            f"7. Do NOT write lists or bullet points.\n"
            f"\n"
            f"Example of a GOOD response:\n"
            f"\"Mujhe afsos hai ke aap bohat pareshan hain. Main aapki baat "
            f"sunne ke liye yahan hoon. Agar aap chahein to mujhe bata sakte "
            f"hain ke kya hua?\"\n"
        )

    if language == "urdu":
        return (
            f"The following response has quality issues:\n"
            f"---\n{bad_response}\n---\n\n"
            f"Problems found:\n{reason_str}\n\n"
            f"Please rewrite the response for this user message:\n"
            f"\"{original_question}\"\n\n"
            f"Write ONLY in Urdu Unicode script. "
            f"Keep it 2 to 4 sentences, warm and supportive. "
            f"Do not use English or Roman Urdu.\n"
        )

    # English fallback
    return (
        f"The following response has quality issues:\n"
        f"---\n{bad_response}\n---\n\n"
        f"Problems found:\n{reason_str}\n\n"
        f"Please rewrite the response for this user message:\n"
        f"\"{original_question}\"\n\n"
        f"Write ONLY in English. "
        f"Keep it 2 to 4 sentences, warm and supportive. "
        f"Do not use Urdu or Roman Urdu.\n"
    )


# =====================================================
# Standalone Test
# =====================================================

if __name__ == "__main__":

    test_cases = [
        # (response_text, expected_language, should_pass)
        ("I'm sorry you're feeling sad. I'm here to listen. Can you tell me what happened?",
         "english", True),

        ("Mujhe afsos hai ke aap bohat udaas hain. Main aapki baat sunne ke liye yahan hoon.",
         "roman_urdu", True),

        ("میں سمجھ سکتی ہوں کہ آپ بہت اداس ہیں۔ میں یہاں آپ کی بات سننے کے لیے موجود ہوں۔",
         "urdu", True),

        # Should FAIL — Urdu script in Roman Urdu response
        ("Mujhe afsos hai. میں یہاں ہوں آپ کے لیے۔",
         "roman_urdu", False),

        # Should FAIL — forbidden word in Roman Urdu
        ("Aapki samasya ka nivaran karna zaroori hai.",
         "roman_urdu", False),

        # Should FAIL — English response when Urdu expected
        ("I understand you are feeling very sad today.",
         "urdu", False),
    ]

    print("=" * 60)
    print("Response Validator Test")
    print("=" * 60)

    all_ok = True
    for text, lang, expected_valid in test_cases:
        result = validate_response(text, lang)
        actual = result["valid"]
        match  = actual == expected_valid
        if not match:
            all_ok = False
        status = "OK  " if match else "FAIL"
        print(f"\n  [{status}] language={lang}, expected_valid={expected_valid}, got={actual}")
        print(f"         text: {text[:70]}...")
        if result["reasons"]:
            for r in result["reasons"]:
                print(f"         reason: {r}")

    print()
    print("ALL PASSED" if all_ok else "SOME FAILED")
