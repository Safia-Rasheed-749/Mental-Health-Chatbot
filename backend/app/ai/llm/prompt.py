"""
=========================================================
LLM Prompt Template
Project : AI Mental Health Chatbot (FYP)

Strategy:
    Instead of relying on a small LLM (llama3.2:1b) to
    detect language from a complex prompt, language is
    detected in Python and a language-specific system
    prompt is selected.  The LLM only ever receives ONE
    language instruction — no ambiguity.
=========================================================
"""

import re
from langchain_core.prompts import ChatPromptTemplate


# =====================================================
# Language Detection (Python-side, reliable)
# =====================================================

# Urdu Unicode range: Arabic script block used by Urdu
_URDU_SCRIPT_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

# Common Urdu words written in Roman/Latin letters
_ROMAN_URDU_WORDS = {
    "ma", "mujhe", "mujhy", "meri", "mera", "mere", "aap", "aapko",
    "apna", "apni", "apne", "hai", "hain", "hon", "tha", "thi", "the",
    "ka", "ki", "ke", "ko", "se", "ne", "par", "bhi", "nahi", "nhi",
    "kya", "kyun", "kab", "kahan", "kaisa", "kaisi", "kaise",
    "bohat", "bht", "bahut", "zyada", "thora", "bilkul",
    "udas", "pareshan", "takleef", "dard", "dukh", "khushi",
    "mehsoos", "lagta", "lagti", "raha", "rahi", "rahe",
    "hua", "hui", "hue", "hota", "hoti", "hote",
    "baat", "bata", "batao", "suno", "samjho", "samajh",
    "din", "raat", "aj", "aaj", "kal", "abhi", "phir",
    "ghar", "dil", "zindagi", "waqt", "log",
    "kuch", "sab", "bas", "lekin", "aur", "ya", "jo",
    "kar", "karo", "karna", "jana", "jao",
    "fikr", "tension", "takleef", "mushkil", "masla",
    "theek", "achha", "acha", "bura",
    "ho", "hona", "hun", "hun",
}


def detect_language(text: str) -> str:
    """
    Detect the language of the user message.

    Returns one of:
        "urdu"       — Urdu Unicode script
        "roman_urdu" — Urdu words written in Latin letters
        "english"    — English (default)
    """
    # Urdu script characters → definitive
    if _URDU_SCRIPT_RE.search(text):
        return "urdu"

    # Tokenise into lowercase words and count Roman Urdu hits
    words = re.findall(r"[a-zA-Z]+", text.lower())
    if not words:
        return "english"

    roman_urdu_hits = sum(1 for w in words if w in _ROMAN_URDU_WORDS)
    ratio = roman_urdu_hits / len(words)

    # If ≥25% of words are Roman Urdu vocabulary AND at least 2 hits → Roman Urdu
    if ratio >= 0.25 and roman_urdu_hits >= 2:
        return "roman_urdu"

    return "english"


# =====================================================
# Language-Specific System Prompts
# =====================================================

_ENGLISH_SYSTEM = """You are a warm, supportive mental-health chatbot.

RULES — follow every one:
1. Reply ONLY in English. Do not use any other language.
2. Keep the reply SHORT: 2 to 4 sentences, 40-80 words maximum.
3. Acknowledge the user's feeling first.
4. Show genuine understanding and warmth.
5. End with ONE gentle question about what happened, if appropriate.
6. Do NOT write lists or bullet points.
7. Do NOT diagnose, prescribe, or give medical advice.
8. Do NOT repeat the user's words back verbatim.
9. If the user mentions self-harm, encourage them to contact emergency services or a trusted person.

DETECTED MENTAL STATE (internal — never reveal to user):
{mental_state}

REFERENCE (use only if user asks for mental-health facts):
{context}"""

_ROMAN_URDU_SYSTEM = """Aap ek meherbaan aur supportive mental health chatbot hain.

RULES — sab follow karo:
1. Sirf Roman Urdu mein jawab do. Koi aur language mat use karo. Spanish, French, ya koi aur language bilkul nahi.
2. Jawab chota rakho: 2 se 4 sentences, 40-80 alfaaz maximum.
3. Pehle user ki feeling ko acknowledge karo.
4. Pyar aur samajh ke saath baat karo.
5. Akhir mein EK halka sa sawaal pocho ke kya hua, agar theek lage.
6. Lists ya bullet points mat banao.
7. Koi diagnosis ya medical advice mat do.
8. User ke alfaaz wapis dohraaney mat.
9. Agar user self-harm ka zikar kare, unhe kisi trusted insaan ya emergency services se milne ki targheeb do.

Roman Urdu mein likho — jaise ek Pakistani dost naturally chat karta hai.
Theek alfaaz: aap, mujhe, bohat, udaas, pareshan, mehsoos, fikr, dil, madad, saath, aaj.
Common English words (anxiety, stress, okay, feel) Roman Urdu mein theek hain.

DETECTED MENTAL STATE (internal — user ko mat batao):
{mental_state}

REFERENCE (sirf tab use karo jab user mental health facts pooche):
{context}"""

_URDU_SYSTEM = """آپ ایک مہربان اور سہارا دینے والے ذہنی صحت کے چیٹ بوٹ ہیں۔

اصول — سب پر عمل کریں:
1. صرف اردو رسم الخط میں جواب دیں۔ کوئی اور زبان نہیں۔
2. جواب مختصر رکھیں: 2 سے 4 جملے، زیادہ سے زیادہ 40-80 الفاظ۔
3. پہلے صارف کے احساس کو تسلیم کریں۔
4. محبت اور سمجھ کے ساتھ بات کریں۔
5. آخر میں ایک ہلکا سوال پوچھیں کہ کیا ہوا، اگر مناسب لگے۔
6. کوئی تشخیص یا طبی مشورہ نہ دیں۔
7. خود کو نقصان پہنچانے کا ذکر ہو تو ہنگامی خدمات سے رابطے کی ترغیب دیں۔

DETECTED MENTAL STATE (داخلی — صارف کو نہ بتائیں):
{mental_state}

REFERENCE:
{context}"""


# =====================================================
# Prompt Factory
# =====================================================

def get_prompt(language: str = "english") -> ChatPromptTemplate:
    """
    Return a language-specific ChatPromptTemplate.

    Args:
        language: One of "english", "roman_urdu", "urdu".
                  Defaults to "english".

    Input variables in the returned template:
        context      — retrieved knowledge chunks
        mental_state — classifier detection results
        question     — current user message

    Returns:
        ChatPromptTemplate with the correct system prompt.
    """
    system_map = {
        "english":    _ENGLISH_SYSTEM,
        "roman_urdu": _ROMAN_URDU_SYSTEM,
        "urdu":       _URDU_SYSTEM,
    }
    system = system_map.get(language, _ENGLISH_SYSTEM)

    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    test_cases = [
        ("i am feeling sad today",          "english"),
        ("ma aj bht udas hon",              "roman_urdu"),
        ("mujhe samajh nahi aa raha kya karun", "roman_urdu"),
        ("مجھے بہت دکھ ہے",               "urdu"),
    ]

    print("=" * 60)
    print("Language Detection Test")
    print("=" * 60)

    for text, expected in test_cases:
        detected = detect_language(text)
        status = "OK" if detected == expected else f"FAIL (expected {expected})"
        print(f"  [{status}] '{text}' -> {detected}")
