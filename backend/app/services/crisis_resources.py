"""
crisis_resources.py
===================
Part 1 of the Crisis Guardrail system for the AI Mental Health Chatbot FYP.

Responsibilities:
    - Pakistan and international crisis helpline directory
    - Pre-written empathetic response templates (English + Roman Urdu)
      for HIGH / MEDIUM / LOW severity levels
    - get_crisis_response() factory with graceful fallback

Does NOT:
    - Call the LLM
    - Make any network requests
    - Depend on any third-party package (standard library only)
    - Modify any existing service
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Helpline Directory
# ─────────────────────────────────────────────────────────────────────────────

CRISIS_HELPLINES: dict = {
    "pakistan": {
        "Umang Helpline":             "0311-7786264",
        "Rozan Helpline":             "0800-22444",
        "Government Mental Health":   "1166",
        "Emergency Services":         "1122 or 15",
    },
    "international": {
        "US 988 Suicide & Crisis Lifeline":                 "Call or Text 988",
        "Crisis Text Line (US)":                            "Text HOME to 741741",
        "International Association for Suicide Prevention": "https://www.iasp.info/resources/Crisis_Centres/",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Response Templates
# ─────────────────────────────────────────────────────────────────────────────

CRISIS_TEMPLATES: dict = {

    # ── HIGH ─────────────────────────────────────────────────────────────────
    "HIGH": {

        "english": (
            "I hear you, and I'm really glad you reached out.\n"
            "What you're feeling right now is incredibly heavy, and you don't have to carry it alone.\n"
            "Your life matters — deeply.\n\n"
            "This pain feels permanent, but it isn't.\n"
            "With the right support, things can and do get better.\n\n"
            "Please reach out to a trained professional RIGHT NOW. They will listen without judgment:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 or 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call or Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "If you are in immediate danger, please call 1122 or go to the nearest emergency room.\n"
            "You are not alone."
        ),

        "roman_urdu": (
            "Main sun raha/sun rahi hoon, aur mujhe khushi hai ke aap ne apni baat share ki.\n"
            "Jo aap feel kar rahe hain wo bohat bhaari hai — aur aap ko yeh akela nahi uthana hai.\n"
            "Aap ki zindagi bohat ahem hai.\n\n"
            "Yeh takleef hamesha ke liye nahi hai.\n"
            "Sahi support ke saath cheezein behtar ho sakti hain — yeh sach hai.\n\n"
            "Barah-e-karam, abhi kisi trained professional se raabta karein. Woh bina kisi judgement ke sunein ge:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 ya 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call ya Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "Agar aap foran khatre mein hain, toh 1122 par call karein ya nazdeeki emergency room jayein.\n"
            "Aap akela/akeli nahi hain."
        ),
    },

    # ── MEDIUM ───────────────────────────────────────────────────────────────
    "MEDIUM": {

        "english": (
            "I hear you, and I want you to know that what you're feeling is real.\n"
            "Feeling this way is a sign that you need — and deserve — some support right now.\n"
            "You are not alone in this.\n\n"
            "These feelings can get better with the right help.\n"
            "Please don't wait — reaching out today can make a real difference.\n\n"
            "Please contact a trained professional. They are there to help:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 or 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call or Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "If you are in immediate danger, please call 1122 or go to the nearest emergency room.\n"
            "You are not alone."
        ),

        "roman_urdu": (
            "Main sun raha/sun rahi hoon, aur jo aap feel kar rahe hain woh bilkul real hai.\n"
            "Is tarah feel karna is baat ki nishani hai ke aap ko abhi kuch support chahiye — aur aap is ke haqdar hain.\n"
            "Aap is mein akele nahi hain.\n\n"
            "Sahi madad se yeh feelings behtar ho sakti hain.\n"
            "Barah-e-karam deri mat karein — aaj raabta karna farq daal sakta hai.\n\n"
            "Kisi trained professional se rabta karein. Woh madad ke liye hain:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 ya 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call ya Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "Agar aap foran khatre mein hain, toh 1122 par call karein ya nazdeeki emergency room jayein.\n"
            "Aap akela/akeli nahi hain."
        ),
    },

    # ── LOW ──────────────────────────────────────────────────────────────────
    "LOW": {

        "english": (
            "I'm glad you shared that with me, and I want you to know I'm here.\n"
            "Feeling worn down and exhausted is hard, and your feelings are completely valid.\n"
            "You matter, and so does how you're feeling right now.\n\n"
            "You don't have to work through this alone.\n"
            "Talking to someone who is trained to help can make a real difference.\n\n"
            "If you ever feel like things are getting heavier, please reach out:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 or 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call or Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "If you are in immediate danger, please call 1122 or go to the nearest emergency room.\n"
            "You are not alone — would you like to tell me a little more about what's been going on?"
        ),

        "roman_urdu": (
            "Mujhe khushi hai ke aap ne share kiya, aur main yahan hoon.\n"
            "Thaka hua aur ub chuka mehsoos karna mushkil hai — aur aap ki yeh feelings bilkul theek hain.\n"
            "Aap ahem hain, aur jo aap feel kar rahe hain woh bhi ahem hai.\n\n"
            "Aap ko yeh akele nahi karna hai.\n"
            "Kisi trained insaan se baat karna sachchi madad kar sakta hai.\n\n"
            "Agar kabhi lagey ke cheezein ziada bhaari ho rahi hain, toh please raabta karein:\n\n"
            "Pakistan Helplines:\n"
            "  • Umang:                    0311-7786264\n"
            "  • Rozan:                    0800-22444\n"
            "  • Government Mental Health: 1166\n"
            "  • Emergency:                1122 ya 15\n\n"
            "International:\n"
            "  • US 988 Lifeline:    Call ya Text 988\n"
            "  • Crisis Text Line:   Text HOME to 741741\n\n"
            "Agar aap foran khatre mein hain, toh 1122 par call karein ya nazdeeki emergency room jayein.\n"
            "Aap akela/akeli nahi hain — kya aap thoda aur bata sakte hain ke kya ho raha hai?"
        ),
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Response Factory
# ─────────────────────────────────────────────────────────────────────────────

def get_crisis_response(severity: str, language: str) -> str:
    """
    Return the appropriate pre-written crisis response template.

    Falls back to HIGH/english if the requested severity or language
    is not found in CRISIS_TEMPLATES.

    Args:
        severity: "HIGH", "MEDIUM", or "LOW"
        language: "english", "roman_urdu", or "urdu"
                  Note: "urdu" falls back to "english" (no Urdu script templates yet)

    Returns:
        Crisis response string ready to send to the user.
    """
    _FALLBACK_SEVERITY = "HIGH"
    _FALLBACK_LANGUAGE = "english"

    severity_block = CRISIS_TEMPLATES.get(severity)
    if severity_block is None:
        logger.warning(
            "get_crisis_response: unknown severity '%s' — falling back to %s/%s",
            severity, _FALLBACK_SEVERITY, _FALLBACK_LANGUAGE,
        )
        return CRISIS_TEMPLATES[_FALLBACK_SEVERITY][_FALLBACK_LANGUAGE]

    template = severity_block.get(language)
    if template is None:
        logger.warning(
            "get_crisis_response: no template for severity='%s' language='%s' — "
            "falling back to %s",
            severity, language, _FALLBACK_LANGUAGE,
        )
        template = severity_block.get(_FALLBACK_LANGUAGE)

    # Final safety net
    if template is None:
        logger.warning(
            "get_crisis_response: complete fallback to %s/%s",
            _FALLBACK_SEVERITY, _FALLBACK_LANGUAGE,
        )
        return CRISIS_TEMPLATES[_FALLBACK_SEVERITY][_FALLBACK_LANGUAGE]

    return template


# ─────────────────────────────────────────────────────────────────────────────
# Standalone Test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("Crisis Resources — Template Verification")
    print("=" * 65)

    for severity in ("HIGH", "MEDIUM", "LOW"):
        for language in ("english", "roman_urdu"):
            print(f"\n{'─' * 65}")
            print(f"  SEVERITY={severity}  |  LANGUAGE={language}")
            print(f"{'─' * 65}")
            print(get_crisis_response(severity, language))

    print(f"\n{'=' * 65}")
    print("Fallback test (unknown severity → HIGH/english):")
    print(f"{'─' * 65}")
    result = get_crisis_response("UNKNOWN", "english")
    print(result[:120] + "...")

    print(f"\n{'=' * 65}")
    print("Fallback test (urdu → english template):")
    print(f"{'─' * 65}")
    result = get_crisis_response("HIGH", "urdu")
    print(result[:120] + "...")

    print(f"\n{'=' * 65}")
    print("All templates verified successfully.")
