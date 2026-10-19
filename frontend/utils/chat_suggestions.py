# -*- coding: utf-8 -*-
"""Current-message wellness suggestions and localized classifier labels."""


def wellness_suggestion(message: str, language: str, variation: int = 0) -> dict:
    text = message.lower()
    if any(term in text for term in ("study", "studies", "exam", "school", "college", "parhai", "mustaqbil", "imtihan", "پڑھائی", "مستقبل", "امتحان")):
        category = "academic"
    elif any(term in text for term in ("sad", "unmotivated", "enjoy", "interest", "udaas", "dil nahi", "دل نہیں", "دلچسپی", "اداس", "خوشی")):
        category = "sadness"
    elif any(term in text for term in ("anxious", "anxiety", "worry", "fikr", "pareshan", "bechain", "بے چینی", "بےچینی", "فکر", "پریشان")):
        category = "anxiety"
    else:
        category = "stress"

    suggestions = {
        "english": {
            "academic": ["Pick one small study task for today, work on it for 15 minutes, then take a short break.", "Write down your top two study priorities for today; leave longer-term planning for a set time later."],
            "sadness": ["Choose one gentle activity you used to enjoy, even for five minutes, or send a quick message to someone you trust.", "Write a few lines about how today feels, then consider sharing them with someone supportive."],
            "anxiety": ["Try a grounding pause: name five things you see, four you feel, and three you hear.", "Breathe out slowly for a little longer than you breathe in, for five comfortable rounds."],
            "stress": ["Pause for five comfortable breaths, then choose just one next step.", "Relax your shoulders, take a short screen-free break, and return to one manageable task."],
        },
        "roman_urdu": {
            "academic": ["Aaj parhai ka aik chhota kaam chunein, 15 minute us par kaam karein, phir chhota waqfa lein.", "Aaj ke liye parhai ke do zaroori kaam likhein; mustaqbil ki planning ke liye baad mein alag waqt rakhein."],
            "sadness": ["Koi pasandeeda kaam sirf paanch minute karein, ya kisi bharosemand shakhs ko chhota sa paigham bhejein.", "Aaj ki kaifiyat ke bare mein chand jumle likhein aur chahein to kisi apne se share karein."],
            "anxiety": ["Zehan ko haal mein lane ke liye aas paas ki paanch cheezein dekhein, chaar cheezein mehsoos karein, aur teen awaazein sunein.", "Paanch martaba aaram se saans andar lein aur us se zara dheere bahar chhorein."],
            "stress": ["Paanch aaram-deh saansein lein, phir sirf agla aik chhota qadam chunein.", "Kandhe dheele chhorein, mobile se chhota waqfa lein, phir aik asaan kaam par lautain."],
        },
        "urdu": {
            "academic": ["آج پڑھائی کا ایک چھوٹا کام چنیں، پندرہ منٹ اس پر توجہ دیں، پھر مختصر وقفہ لیں۔", "آج کے دو ضروری تعلیمی کام لکھیں؛ مستقبل کی منصوبہ بندی کے لیے بعد میں الگ وقت رکھیں۔"],
            "sadness": ["کوئی پسندیدہ کام صرف پانچ منٹ کریں، یا کسی قابلِ اعتماد شخص کو مختصر پیغام بھیجیں۔", "آج کی کیفیت کے بارے میں چند سطریں لکھیں اور چاہیں تو کسی اپنے سے بات کریں۔"],
            "anxiety": ["ذہن کو حال میں لانے کے لیے پانچ دیکھی ہوئی چیزیں، چار چھوئی ہوئی چیزیں اور تین سنی ہوئی آوازیں نوٹ کریں۔", "پانچ بار آرام سے سانس اندر لیں اور اس سے قدرے آہستہ باہر چھوڑیں۔"],
            "stress": ["آرام سے پانچ سانسیں لیں، پھر اگلا صرف ایک چھوٹا قدم چنیں۔", "کندھے ڈھیلے چھوڑیں، اسکرین سے مختصر وقفہ لیں، پھر ایک آسان کام شروع کریں۔"],
        },
    }
    language = language if language in suggestions else "english"
    options = suggestions[language][category]
    return {"category": category, "text": options[variation % len(options)]}


LABELS = {
    "english": {
        "heading": "Current-message model estimates",
        "emotion": "Emotion signal",
        "stress": "Estimated stress signal",
        "depression": "Estimated depression signal",
        "confidence": "Model confidence",
        "disclaimer": "These are uncertain model estimates, not medical diagnoses. The emotion model’s Fear label is not an anxiety diagnosis.",
        "fear_note": "Fear is an emotion label, not an anxiety diagnosis.",
        "wellness": "A gentle reset may help",
        "exercise": "Explore guided exercises",
    },
    "roman_urdu": {
        "heading": "Is paigham ke model andazay",
        "emotion": "Jazbati signal",
        "stress": "Stress ka andazati signal",
        "depression": "Depression ka andazati signal",
        "confidence": "Model ka aitmaad",
        "disclaimer": "Yeh model ke ghair-yaqeeni andazay hain, medical tashkhees nahi. Emotion model ka Fear label anxiety ki tashkhees nahi hai.",
        "fear_note": "Emotion model ka Fear jazbati label hai, anxiety ki tashkhees nahi.",
        "wellness": "Chhota sa waqfa madadgar ho sakta hai",
        "exercise": "Rehnumai wali mashqein dekhein",
    },
    "urdu": {
        "heading": "اس پیغام کے بارے میں ماڈل کے اندازے",
        "emotion": "جذباتی اشارہ",
        "stress": "ذہنی دباؤ کا اندازہ",
        "depression": "ڈپریشن کا اندازہ",
        "confidence": "ماڈل کا اعتماد",
        "disclaimer": "یہ ماڈل کے غیر یقینی اندازے ہیں، طبی تشخیص نہیں۔ جذباتی ماڈل کا Fear اشارہ اضطراب کی تشخیص نہیں ہے۔",
        "fear_note": "Fear جذباتی ماڈل کا ایک label ہے، اضطراب کی تشخیص نہیں۔",
        "wellness": "ایک مختصر وقفہ مددگار ہو سکتا ہے",
        "exercise": "رہنمائی والی مشقیں دیکھیں",
    },
}


CLASS_LABELS = {
    "roman_urdu": {
        "emotion": {"sadness": "Udaasi", "joy": "Khushi", "love": "Muhabbat", "anger": "Gussa", "fear": "Khauf", "surprise": "Hairani"},
        "stress": {"stress": "Stress", "no stress": "Stress nahi"},
        "depression": {"depression": "Depression signal", "no depression": "Depression signal nahi"},
    },
    "urdu": {
        "emotion": {"sadness": "اداسی", "joy": "خوشی", "love": "محبت", "anger": "غصہ", "fear": "خوف", "surprise": "حیرت"},
        "stress": {"stress": "ذہنی دباؤ کا اشارہ", "no stress": "ذہنی دباؤ کا اشارہ نہیں"},
        "depression": {"depression": "ڈپریشن کا اشارہ", "no depression": "ڈپریشن کا اشارہ نہیں"},
    },
}


def display_classifier_label(kind: str, value: str, language: str) -> str:
    """Localize existing classifier labels without inventing a diagnosis or score."""
    translations = CLASS_LABELS.get(language, {})
    return translations.get(kind, {}).get(value.lower(), value.title())
