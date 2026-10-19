# -*- coding: utf-8 -*-
"""LLM response extraction, quality retries, and concern-aware safe fallback."""

from langchain_core.messages import HumanMessage

from app.ai.llm.roman_urdu_style import MAX_REGENERATE_ATTEMPTS
from app.ai.llm.validator import validate_response, build_correction_prompt


def _message_text(result) -> str:
    content = getattr(result, "content", result)
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    return str(content).strip()


def _concern(question: str) -> str:
    text = question.lower()
    if any(term in text for term in ("study", "studies", "exam", "school", "college", "parhai", "mustaqbil", "imtihan", "پڑھائی", "مستقبل", "امتحان")):
        return "academic"
    if any(term in text for term in ("sad", "unmotivated", "enjoy", "interest", "udaas", "dil nahi", "dil nahin", "اداس", "دل نہیں", "دلچسپی", "خوشی")):
        return "sadness"
    if any(term in text for term in ("anxious", "anxiety", "worry", "worrying", "fikr", "pareshan", "bechain", "بے چین", "بےچین", "فکر", "پریشان", "بے چینی")):
        return "anxiety"
    return "stress"


def response_quality_reasons(question: str, response: str, language: str) -> list[str]:
    """Lightweight relevance checks beyond spelling/script validation."""
    concern = _concern(question)
    text = response.lower()
    reasons = []
    signals = {
        "academic": {
            "english": (("study", "school", "exam", "future", "task"), ("plan", "small", "step", "break", "time", "goal")),
            "roman_urdu": (("parhai", "mustaqbil", "imtihan", "kaam"), ("chhota", "qadam", "waqt", "waqfa", "plan", "hissa")),
            "urdu": (("پڑھائی", "مستقبل", "امتحان", "کام"), ("چھوٹا", "قدم", "وقت", "وقفہ", "منصوبہ", "تقسیم")),
        },
        "sadness": {
            "english": (("sad", "interest", "enjoy", "feelings", "low", "joy"), ("trusted", "someone", "professional", "support", "activity", "write", "reach out")),
            "roman_urdu": (("udaas", "dilchaspi", "pasandeeda", "mehsoos", "dil"), ("bharosemand", "shakhs", "professional", "baat", "kaam", "likh", "madad")),
            "urdu": (("اداس", "دلچسپی", "پسندیدہ", "احساس", "خوشی"), ("قابلِ اعتماد", "بھروسہ", "ماہر", "بات", "کام", "لکھ", "مدد")),
        },
        "anxiety": {
            "english": (("worry", "anxious", "anxiety", "settle", "relax"), ("ground", "breath", "breathe", "step", "write", "break")),
            "roman_urdu": (("fikr", "pareshan", "bechain", "sukoon", "anxiety"), ("grounding", "saans", "qadam", "likh", "waqfa", "chhor")),
            "urdu": (("فکر", "پریشان", "بے چین", "بےچین", "سکون"), ("گراؤنڈنگ", "سانس", "قدم", "لکھ", "وقفہ", "چیزیں")),
        },
        "stress": {
            "english": (("stress", "pressure", "overwhelm", "worry"), ("breath", "breathe", "task", "step", "break", "pause")),
            "roman_urdu": (("stress", "dabao", "pareshan", "fikr"), ("saans", "kaam", "qadam", "waqfa", "ruk")),
            "urdu": (("دباؤ", "ذہنی دباؤ", "فکر", "پریشان"), ("سانس", "کام", "قدم", "وقفہ", "رکیں")),
        },
    }
    language = language if language in {"english", "roman_urdu", "urdu"} else "english"
    topic_terms, action_terms = signals[concern][language]
    if not any(term in text for term in topic_terms):
        reasons.append("The response does not address the user's stated concern directly.")
    if not any(term in text for term in action_terms):
        reasons.append("The response needs at least one practical step relevant to the user's concern.")
    if concern == "academic":
        planning_terms = {
            "english": ("task", "step", "plan", "goal", "syllabus", "subject"),
            "roman_urdu": ("kaam", "qadam", "plan", "hiss", "mazmoon", "subject"),
            "urdu": ("کام", "قدم", "منصوبہ", "تقسیم", "سبق", "مضمون"),
        }[language]
        if not any(term in text for term in planning_terms):
            reasons.append("For study/future worries, suggest one manageable study task or a simple plan, not only relaxation.")
    if concern == "sadness":
        support_terms = {
            "english": ("trusted", "professional", "someone", "support", "counselor"),
            "roman_urdu": ("bharosemand", "professional", "shakhs", "kisi apne"),
            "urdu": ("قابلِ اعتماد", "بھروسہ", "ماہر", "کسی اپنے"),
        }[language]
        if not any(term in text for term in support_terms):
            reasons.append("For persistent sadness/loss of interest, include a gentle suggestion to seek trusted or professional support.")
    return reasons


def concern_fallback(question: str, language: str) -> str:
    """A modest failure fallback that still addresses the user's expressed concern."""
    concern = _concern(question)
    responses = {
        "english": {
            "academic": "Worry about study and the future can feel like too much at once. Choose one small task for today, set a realistic time for it, and take a short break afterward. What feels most urgent to work on first?",
            "sadness": "Feeling sad and losing interest can be heavy to carry. Try one gentle, manageable activity and tell someone you trust; if this continues or affects daily life, consider speaking with a mental-health professional. How long have you been feeling this way?",
            "anxiety": "It sounds as though worry is making it hard to settle. For the next minute, name five things you see and let your exhale be slow; then choose one worry you can act on today. What has been weighing on you most?",
            "stress": "It sounds like the stress has been building up. Pause for a moment, then choose one small thing you can do next and give yourself a brief break afterward. What is putting the most pressure on you today?",
        },
        "roman_urdu": {
            "academic": "Aapko parhai aur mustaqbil ki fikr aik saath bohat bhaari lag sakti hai. Aaj ka sirf aik chhota kaam chunein, us ke liye munasib waqt rakhein, phir chhota waqfa lein. Is waqt sab se pehle kaunsa kaam karna zaroori lagta hai?",
            "sadness": "Udaasi aur pasandeeda cheezon mein dilchaspi kam hona mushkil lag sakta hai. Aaj koi chhota, narm sa kaam karein aur kisi bharosemand shakhs ko apni kaifiyat batayein; agar yeh silsila jaari rahe to mental-health professional se baat karein. Yeh kab se mehsoos ho raha hai?",
            "anxiety": "Lagta hai fikr ki wajah se aapko sukoon se baithna mushkil ho raha hai. Aik minute ke liye aas paas ki paanch cheezein dekhein aur saans ahista bahar chhorein; phir aaj ke liye aik chhota qadam chunein. Aapko sab se zyada fikr kis baat ki hai?",
            "stress": "Aapko lagta hai stress kuch zyada barh gaya hai. Aik lamha ruk kar agla chhota kaam chunein, phir apne liye thora waqfa rakhein. Aaj sab se zyada dabao kis baat ka hai?",
        },
        "urdu": {
            "academic": "پڑھائی اور مستقبل کی فکر ایک ساتھ بہت بھاری محسوس ہو سکتی ہے۔ آج کے لیے صرف ایک چھوٹا کام چنیں، اسے مکمل کرنے کا مناسب وقت رکھیں، پھر مختصر وقفہ لیں۔ اس وقت سب سے پہلے کون سا کام ضروری لگتا ہے؟",
            "sadness": "اداسی اور پسندیدہ کاموں میں دلچسپی کم ہونا مشکل کیفیت ہے۔ آج کوئی چھوٹا سا ایسا کام کریں جس سے آپ کو پہلے خوشی ملتی تھی، اور کسی قابلِ اعتماد شخص کو اپنے احساسات بتائیں۔ اگر یہ کیفیت برقرار رہے یا روزمرہ زندگی متاثر ہو تو ذہنی صحت کے ماہر سے بات کرنے پر غور کریں۔ یہ کب سے ہو رہا ہے؟",
            "anxiety": "لگتا ہے فکر کی وجہ سے آپ کے لیے پُرسکون رہنا مشکل ہو رہا ہے۔ ایک منٹ کے لیے اپنے آس پاس کی پانچ چیزیں دیکھیں اور سانس آہستہ باہر چھوڑیں؛ پھر آج کے لیے ایک چھوٹا قابلِ عمل قدم چنیں۔ سب سے زیادہ فکر کس بات کی ہے؟",
            "stress": "لگتا ہے ذہنی دباؤ بڑھ گیا ہے۔ ایک لمحہ رک کر اگلا چھوٹا کام چنیں اور اس کے بعد مختصر وقفہ لیں۔ آج سب سے زیادہ دباؤ کس بات کا ہے؟",
        },
    }
    return responses.get(language, responses["english"])[concern]


def generate_validated_response(llm, messages: list, question: str, language: str) -> tuple[str, bool]:
    """Call the configured chat model, retry low-quality/truncated output, then fall back safely."""
    latest_text = ""
    current_messages = list(messages)
    for attempt in range(MAX_REGENERATE_ATTEMPTS + 1):
        try:
            raw = llm.invoke(current_messages)
        except Exception as exc:
            print(f"[chat] LLM invocation failed ({type(exc).__name__}); retrying safely.")
            latest_text = ""
            if attempt < MAX_REGENERATE_ATTEMPTS:
                continue
            break
        latest_text = _message_text(raw)
        result = validate_response(latest_text, language)
        result["reasons"].extend(response_quality_reasons(question, latest_text, language))
        if result["reasons"]:
            result["valid"] = False
        done_reason = getattr(raw, "response_metadata", {}).get("done_reason")
        if done_reason == "length":
            result["valid"] = False
            result["reasons"].append("Model stopped at the output token limit; response may be incomplete.")
        if result["valid"]:
            return latest_text, attempt > 0
        if attempt < MAX_REGENERATE_ATTEMPTS:
            correction = build_correction_prompt(question, latest_text, result)
            current_messages = list(messages) + [HumanMessage(content=correction)]
    return concern_fallback(question, language), True
