# -*- coding: utf-8 -*-
"""
=========================================================
LLM Prompt Templates
Project : AI Mental Health Chatbot (FYP)

Strategy:
    Language is detected in Python (not by the LLM).
    Each language gets its own dedicated system prompt.

    Response length is ADAPTIVE — the LLM decides based
    on the user's message type, emotional state, and
    complexity. No fixed word counts.

Language support:
    english    — English only
    roman_urdu — Urdu written in Latin/English letters
    urdu       — Urdu Unicode script
=========================================================
"""

import re
from langchain_core.prompts import ChatPromptTemplate
from app.ai.llm.system_prompts import _ENGLISH_SYSTEM, _ROMAN_URDU_SYSTEM


# =====================================================
# Language Detection  (Python-side — never trust LLM)
# =====================================================

_URDU_SCRIPT_RE = re.compile(
    r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]"
)

_ROMAN_URDU_WORDS = {
    "ma", "mai", "main", "mujhe", "mujhy", "mujhse",
    "meri", "mera", "mere", "aap", "aapko", "aapke",
    "apna", "apni", "apne", "hum", "humko", "hamara",
    "tum", "tumhe", "tumhara",
    "hai", "hain", "hon", "tha", "thi", "the",
    "hona", "hoti", "hota", "hote",
    "hua", "hui", "hue",
    "raha", "rahi", "rahe",
    "kar", "karo", "karna", "karta", "karti",
    "bata", "batao", "batayen",
    "lagta", "lagti", "laga",
    "chahiye", "chahein", "chahta", "chahti",
    "sakta", "sakti", "sakte",
    "ka", "ki", "ke", "ko", "se", "ne", "par",
    "bhi", "nahi", "nhi", "nahin",
    "kya", "kyun", "kab", "kahan", "kaisa", "kaisi", "kaise",
    "lekin", "aur", "ya", "jo", "agar", "toh", "to",
    "kuch", "sab", "bas", "phir", "sirf",
    "udas", "udaas", "pareshan", "takleef", "dard",
    "dukh", "gham", "khushi", "khusi", "fikr",
    "dara", "ghabrana", "akela", "akeli",
    "thaka", "thaki", "mushkil", "masla",
    "mehsoos", "ehsaas",
    "bohat", "bht", "bahut", "zyada", "thora", "thodi",
    "bilkul", "ziada",
    "aaj", "aj", "kal", "abhi",
    "ghar", "yahan", "wahan", "bahar",
    "dil", "baat", "zindagi", "waqt", "log",
    "din", "raat", "saath", "madad", "samajh",
    "theek", "acha", "achha", "thik",
    "haan", "han", "shukriya",
}


def detect_language(text: str) -> str:
    """
    Detect the language of a user message.

    Returns:
        "urdu"       — Urdu Unicode script
        "roman_urdu" — Urdu words in Latin letters
        "english"    — default
    """
    if _URDU_SCRIPT_RE.search(text):
        return "urdu"

    words = re.findall(r"[a-zA-Z]+", text.lower())
    if not words:
        return "english"

    hits  = sum(1 for w in words if w in _ROMAN_URDU_WORDS)
    ratio = hits / len(words)

    if hits >= 2 and ratio >= 0.25:
        return "roman_urdu"

    return "english"


_URDU_SYSTEM = """آپ ایک مہربان اور سہارا دینے والے ذہنی صحت کے ساتھی ہیں — ایک قابلِ اعتماد دوست کی طرح۔

ذاتی سیاق و سباق:
{user_context}

جواب کی لمبائی:
  سادہ پیغام → 1-2 جملے
  جذباتی پیغام → 3-5 جملے
  تفصیلی صورتحال → جتنی ضرورت ہو
  معلوماتی سوال → سیدھا اور واضح جواب

جواب کی ساخت (قدرتی انداز میں):
  1) صارف کی بتائی ہوئی خاص بات پر ہمدردی دکھائیں
  2) احساس کو انسانی ردعمل کے طور پر تسلیم کریں
  3) صرف ضرورت ہو تو ایک عملی مشورہ دیں
  4) ایک گرمجوش سوال پوچھیں
جواب کی لمبائی — لچکدار رکھیں:
  ہر پیغام پڑھ کر خود فیصلہ کریں:

  سادہ یا معمولی پیغام:
    → 1-2 جملے۔

  سادہ جذباتی پیغام:
    → 3-5 جملے۔ احساس تسلیم کریں + سوال پوچھیں۔

  anxiety، stress، دباؤ، اکیلاپن:
    → 4-7 جملے۔ احساس کو تسلیم کریں → فطری بتائیں →
      ایک عملی مشورہ دیں → مزید بات کرنے کی دعوت دیں۔

  تفصیلی پیغام:
    → جتنا ضروری ہو اتنا لکھیں۔ ادھورا نہ چھوڑیں۔

  معلوماتی سوال:
    → واضح اور مددگار جواب دیں۔

جواب کا بہاؤ — قدرتی طریقے سے اپنائیں:
  1. احساس تسلیم کریں — صارف کو محسوس کرائیں کہ آپ سن رہے ہیں۔
  2. فطری بتائیں — یہ احساس انسانی ردعمل ہے، کمزوری نہیں۔
  3. ایک عملی مشورہ دیں — anxiety کے لیے سانس کی مشق وغیرہ۔
  4. مزید بات کی دعوت دیں — ایک گرمجوش سوال سے ختم کریں۔

اصول:
- صرف اردو رسم الخط میں جواب دیں۔
- رومن اردو یا انگریزی بالکل نہیں۔
- فہرستیں یا نکات نہ بنائیں۔
- تشخیص یا طبی مشورہ نہ دیں۔
- خود کو نقصان پہنچانے کا ذکر ہو تو فوری طور پر ہنگامی خدمات یا
  کسی قابلِ اعتماد شخص سے رابطے کی ترغیب دیں۔

انداز: گرمجوش، پُرسکون، دوستانہ۔

مثالیں:

صارف: میں آج بہت اداس ہوں
مددگار: یہ سن کر دل دکھا — اور یہ بالکل فطری بات ہے کہ کبھی کبھی دل بھاری ہو جاتا ہے۔ آپ اکیلے نہیں ہیں، میں آپ کے ساتھ ہوں۔ کچھ دیر کے لیے کوئی پسندیدہ کام کریں یا کسی قریبی سے بات کریں، تھوڑا ہلکا لگے گا۔ کیا آپ مجھے بتا سکتے ہیں کہ آج کیا ہوا؟

صارف: مجھے بہت فکر ہو رہی ہے
مددگار: فکر کا یہ احساس بہت بھاری ہوتا ہے — اور میں سمجھ سکتا ہوں کہ آپ ابھی کتنا محسوس کر رہے ہیں۔ آپ اکیلے نہیں ہیں۔ ایک کام آزمائیں: چار سیکنڈ میں سانس اندر لیں، چار سیکنڈ روکیں، پھر چار سیکنڈ میں باہر چھوڑیں — یہ تھوڑا سکون دیتا ہے۔ کیا کوئی خاص بات ہے جو آپ کو سب سے زیادہ پریشان کر رہی ہے؟

ذہنی حالت کے اشارے کا استعمال:
نیچے دی گئی پیش گوئیاں classifier کے غیر یقینی اشارے ہیں، حقائق نہیں۔
انہیں صرف لہجے کے لیے استعمال کریں، صارف کے بارے میں دعوے کے طور پر نہیں:
  - sadness (زیادہ اعتماد): زیادہ ہمدردی، نرم رفتار، خوش مزاجی سے گریز
  - anger (زیادہ اعتماد): پُرسکون لہجہ، کشیدگی کم کریں، بحث نہ کریں
  - fear (زیادہ اعتماد): grounding، تسلی، مختصر جملے
  - joy (زیادہ اعتماد): مثبت توانائی سے ہم آہنگ ہوں
  - Stress: ایک فوری سکون دینے کی مشق بتائیں
  - Depression: نرم امید اور ماہر سے مدد لینے کا مشورہ
  - کم اعتماد (<60%): اشارے کو نظرانداز کریں، صارف کے الفاظ کو ترجیح دیں
یہ labels صارف کو کبھی نہ بتائیں۔ تشخیص کبھی نہ کریں۔
ہمیشہ classifier کے اشارے سے زیادہ صارف کی کہی ہوئی بات کو ترجیح دیں۔
صارف: میں بہت تھکا ہوا محسوس کر رہا ہوں
مددگار: یہ تھکاوٹ آپ کے لیے بہت مشکل ہوگی — جب اندر سے تھکاوٹ ہو تو سب کچھ بھاری لگتا ہے۔ آج اپنے ساتھ نرمی برتیں — آرام کریں، پانی پیئیں، کوئی ایک پسندیدہ چیز کریں۔ کیا یہ صرف جسمانی تھکاوٹ ہے یا اندر سے بھی کچھ بھاری ہے؟

صارف: مجھے exams کی وجہ سے بہت stress ہو رہا ہے
مددگار: Exams کا دباؤ بہت حقیقی ہوتا ہے — اور جو آپ محسوس کر رہے ہیں وہ بالکل فطری ہے۔ ایک کام کریں: پورا syllabus ایک ساتھ دیکھنے کی بجائے صرف آج کے لیے ایک موضوع چنیں — چھوٹی شروعات بڑی کامیابی ہوتی ہے۔ اگر چاہیں تو ہم مل کر آپ کا مطالعے کا منصوبہ بنا سکتے ہیں۔ کیا کوئی مخصوص مضمون ہے جس کی وجہ سے زیادہ پریشانی ہو رہی ہے؟

DETECTED MENTAL STATE — صرف داخلی استعمال، صارف کو نہ بتائیں:
{mental_state}

حالیہ گفتگو:
{history}

REFERENCE KNOWLEDGE — صرف اس وقت استعمال کریں جب صارف
ذہنی صحت کے بارے میں معلومات مانگے:
{context}"""


# =====================================================
# Prompt Factory
# =====================================================

def get_prompt(language: str = "english") -> ChatPromptTemplate:
    """
    Return the language-specific ChatPromptTemplate.

    Args:
        language: One of "english", "roman_urdu", "urdu".

    Template input variables:
        context      — retrieved RAG knowledge chunks
        mental_state — classifier detection results string
        user_context — recent mood and journal history
        history      — recent conversation turns
        question     — current user message
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
# Standalone Test
# =====================================================

if __name__ == "__main__":

    test_cases = [
        ("i am feeling sad today",                    "english"),
        ("i feel anxious about everything",           "english"),
        ("i need someone to talk to",                 "english"),
        ("ma aj bht udas hon",                        "roman_urdu"),
        ("mujhe samajh nahi aa raha kya karun",       "roman_urdu"),
        ("mujhy anxiety ho rhi ha",                   "roman_urdu"),
        ("aj mera din bht kharab tha",                "roman_urdu"),
        ("mujhe kisi se baat karni hai",              "roman_urdu"),
        ("main bohat pareshan hon ghar ke maslon se", "roman_urdu"),
        ("میں آج بہت اداس ہوں",                      "urdu"),
        ("مجھے بہت فکر ہو رہی ہے",                   "urdu"),
    ]

    print("=" * 60)
    print("Language Detection Test")
    print("=" * 60)

    all_ok = True
    for text, expected in test_cases:
        detected = detect_language(text)
        ok = detected == expected
        if not ok:
            all_ok = False
        status = "OK  " if ok else "FAIL"
        print(f"  [{status}] '{text}' -> {detected}")

    print()
    print("ALL PASSED" if all_ok else "SOME FAILED")

    print()
    print("Prompt input variables:")
    expected_variables = {"context", "mental_state", "user_context", "history", "question"}
    for lang in ("english", "roman_urdu", "urdu"):
        p = get_prompt(lang)
        print(f"  {lang}: {p.input_variables}")
        if set(p.input_variables) != expected_variables:
            raise AssertionError(
                f"{lang} prompt variables should be {sorted(expected_variables)}; "
                f"got {p.input_variables}"
            )
