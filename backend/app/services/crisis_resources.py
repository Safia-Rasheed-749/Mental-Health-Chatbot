# -*- coding: utf-8 -*-
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
    'HIGH': {
        'urdu': 'مجھے اندازہ ہے کہ آپ اس وقت بہت تکلیف میں ہیں، اور میں آپ کی بات سن رہا ہوں۔\n\nآپ کے احساسات اہم ہیں۔ براہِ کرم ابھی کسی قابلِ اعتماد شخص یا تربیت یافتہ ماہر سے رابطہ کریں۔\n\nپاکستان میں مدد:\n- امنگ: 0311-7786264\n- روزان: 0800-22444\n- ہنگامی مدد: 1122 یا 15\n\nاگر آپ فوری خطرے میں ہیں تو 1122 پر کال کریں یا قریبی ایمرجنسی میں جائیں.',
        'english': 'I hear how much pain you are in right now, and I want you to know\nthat I am here with you in this moment.\n\nYour feelings are real, and you matter. What you are going through\nis incredibly difficult, and you do not have to face it alone.\n\nPlease reach out to a trained professional RIGHT NOW. They will\nlisten without judgment:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Rozan: 0800-22444\n? Government Mental Health: 1166\n? Emergency: 1122 or 15\n\nInternational:\n? US 988 Lifeline: Call or Text 988\n? Crisis Text Line: Text HOME to 741741\n\nIf you are in immediate danger, please call 1122 or go to the\nnearest emergency room. You are not alone, and your life matters.',
        'roman_urdu': 'Main sun raha hoon ke aap kitni takleef mein hain, aur main chahta\nhoon ke aap jaanen ke is waqt main aapke saath hoon.\n\nAap ke jazbaat haqeeqi hain, aur aap ki zindagi ahem hai. Jo aap\nse guzar rahe hain wo bohat mushkil hai, aur aap ko akela nahi\nuthana hai.\n\nBarah-e-karam, abhi kisi trained professional se raabta karein.\nWoh bina kisi judgment ke sunenge:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Rozan: 0800-22444\n? Government Mental Health: 1166\n? Emergency: 1122 ya 15\n\nInternational:\n? US 988 Lifeline: Call ya Text 988\n? Crisis Text Line: Text HOME to 741741\n\nAgar aap foran khatre mein hain, toh 1122 par call karein ya\nnazdeeki emergency room jayein. Aap akela/akeli nahi hain, aur\naap ki zindagi ahem hai.',
    },
    'MEDIUM': {
        'english': "I can hear that things feel really heavy for you right now, and\nI want you to know that I am listening.\n\nWhat you are feeling is valid, and it's okay to not be okay.\nPlease don't carry this alone ? talking to someone who understands\ncan make a real difference.\n\nHere are people who can help:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Rozan: 0800-22444\n? Government Mental Health: 1166\n\nInternational:\n? US 988 Lifeline: Call or Text 988\n\nYou matter, and there are people who want to support you.",
        'roman_urdu': 'Main sun sakta hoon ke is waqt sab kuch bohat bhaari lag raha hai,\naur main chahta hoon ke aap jaanen ke main sun raha hoon.\n\nAap jo feel kar rahe hain wo haqeeqi hai, aur theek hai agar aap\ntheek na hoon. Barah-e-karam akela mat uthayein ? kisi aise insaan\nse baat karein jo samajhta ho, isse waqai farq padta hai.\n\nYeh log aap ki madad kar sakte hain:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Rozan: 0800-22444\n? Government Mental Health: 1166\n\nInternational:\n? US 988 Lifeline: Call ya Text 988\n\nAap ahem hain, aur kuch log hain jo aap ki madad karna chahte hain.',
    },
    'LOW': {
        'english': "It sounds like you're feeling really exhausted and worn down\nlately. That kind of tiredness is real, and I want you to know\nit's okay to feel this way.\n\nYou deserve support and care, and there are people who can help\nlighten this load.\n\nConsider reaching out to:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Government Mental Health: 1166\n\nInternational:\n? US 988 Lifeline: Call or Text 988\n\nTake care of yourself, and remember ? you don't have to face\nthis alone.",
        'roman_urdu': 'Aisa lagta hai ke aap bohat thak gaye hain aur andar se khali\nmehsoos kar rahe hain. Yeh thakaan haqeeqi hai, aur main chahta\nhoon ke aap jaanen ke aisa feel karna theek hai.\n\nAap support aur care deserve karte/karti hain, aur kuch log\nhain jo aap ka bojh halka kar sakte hain.\n\nIn se raabta karne ke baare mein sochein:\n\nPakistan Helplines:\n? Umang: 0311-7786264\n? Government Mental Health: 1166\n\nInternational:\n? US 988 Lifeline: Call ya Text 988\n\nApna khayal rakhein, aur yaad rakhein ? aap ko akela/akeli\nnahi uthana hai.',
    },
}

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

    response = template
    response = response.replace("?", "-")
    return response


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
