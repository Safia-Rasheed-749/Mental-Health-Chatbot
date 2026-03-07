"""
Enhanced AI engine for mental health chatbot.
- Emotion detection using transformer model (fallback to rule-based)
- Crisis detection with severity levels
- Empathetic, context-aware responses
- Coping strategies based on detected emotion
"""

import random
from textblob import TextBlob

# Optional: Use a proper emotion classifier from HuggingFace
# pip install transformers
try:
    from transformers import pipeline
    emotion_classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
        device=-1  # use CPU
    )
    USE_TRANSFORMER = True
except ImportError:
    USE_TRANSFORMER = False
    # Fallback: simple keyword-based emotion mapping
    emotion_keywords = {
        "anger": ["angry", "frustrated", "annoyed", "mad", "irritated"],
        "fear": ["scared", "afraid", "terrified", "panicked", "anxious"],
        "sadness": ["sad", "depressed", "down", "unhappy", "gloomy"],
        "joy": ["happy", "glad", "joyful", "cheerful", "delighted"],
        "surprise": ["shocked", "surprised", "astonished", "amazed"],
        "disgust": ["disgusted", "repulsed", "grossed out"]
    }

# Crisis phrases by severity
CRISIS_PHRASES = {
    "high": [
        "kill myself", "end my life", "commit suicide", "want to die",
        "going to kill myself", "suicide", "take my own life"
    ],
    "medium": [
        "self harm", "hurt myself", "cut myself", "no reason to live",
        "better off dead", "wish i was dead"
    ],
    "low": [
        "feel hopeless", "want to give up", "can't go on", "worthless",
        "don't want to be here"
    ]
}

# Coping strategies for different emotions
COPING_STRATEGIES = {
    "anger": [
        "When anger arises, try stepping away from the situation for a few minutes. Deep breathing can also help—breathe in for 4 counts, hold for 4, out for 6.",
        "Anger often signals that a boundary has been crossed. Can you identify what triggered this feeling? Writing it down might bring clarity."
    ],
    "fear": [
        "Fear can feel overwhelming. Let's ground ourselves together: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "It's okay to feel scared. Try a slow breath: inhale through your nose for 4, hold for 2, exhale through your mouth for 6."
    ],
    "sadness": [
        "Sadness is a natural emotion. Sometimes a small act of self-care—like making tea or stepping outside—can gently lift the weight.",
        "Would you like to try writing down one thing you're grateful for, even if it's small? Gratitude can shift our focus, even momentarily."
    ],
    "anxiety": [
        "Anxiety often pulls us into the future. Come back to the present with the 5-4-3-2-1 technique: 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "Let's take a slow breath together: breathe in for 4, hold for 4, out for 6. Repeat a few times."
    ],
    "joy": [
        "Joy is a beautiful feeling! What's contributing to this positive emotion? Savouring the moment can amplify it."
    ],
    "surprise": [
        "Surprise can be pleasant or unsettling. Would you like to share what surprised you?"
    ],
    "neutral": [
        "I'm here with you. Could you tell me a bit more about what's on your mind?"
    ]
}

def detect_emotion(text):
    """Return an emotion label for the given text."""
    if USE_TRANSFORMER:
        results = emotion_classifier(text)[0]
        top_emotion = max(results, key=lambda x: x['score'])
        return top_emotion['label']
    else:
        # Simple keyword fallback
        text_lower = text.lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        # Use sentiment polarity as rough guide
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.3:
            return "joy"
        elif polarity < -0.3:
            return "sadness"
        else:
            return "neutral"

def assess_crisis(text):
    """Return crisis severity level (high/medium/low) or None."""
    text_lower = text.lower()
    for level, phrases in CRISIS_PHRASES.items():
        for phrase in phrases:
            if phrase in text_lower:
                return level
    return None

def crisis_response(level):
    """Return an empathetic crisis message with helpline numbers."""
    base = (
        "I'm really concerned about what you're sharing. You are not alone, "
        "and help is available.\n\n"
    )
    if level == "high":
        return base + (
            "**Please reach out immediately to a crisis line:**\n"
            "📞 National Suicide Prevention Lifeline: **988** (US)\n"
            "📱 Crisis Text Line: Text **HOME** to **741741**\n\n"
            "You deserve support right now. Would you like to try a grounding exercise together while you decide?"
        )
    elif level == "medium":
        return base + (
            "It's important to talk to someone who can support you. "
            "You can call a crisis line anytime: **988** (US) or your local emergency number.\n\n"
            "I'm here with you. Would you like to try a breathing exercise to help calm your mind?"
        )
    else:  # low
        return (
            "I hear how heavy this feels for you. You matter, and there is support. "
            "Sometimes just talking about it can help. What's on your mind right now?\n\n"
            "If you ever need immediate help, you can reach out to:\n"
            "📞 **988** Suicide & Crisis Lifeline\n"
            "📱 Text **HOME** to **741741**"
        )

def get_coping_strategy(emotion):
    """Return a random coping strategy for the given emotion."""
    strategies = COPING_STRATEGIES.get(emotion, COPING_STRATEGIES["neutral"])
    return random.choice(strategies)

def generate_response(user_message, context=None):
    """
    Main response generator.
    - context: list of (role, message) tuples for the last few exchanges.
    """
    # 1. Check for crisis
    crisis_level = assess_crisis(user_message)
    if crisis_level:
        return crisis_response(crisis_level)

    # 2. Detect emotion
    emotion = detect_emotion(user_message)

    # 3. Optionally use context to avoid repetition (basic example)
    if context and len(context) > 0:
        # Look at the last bot message to avoid offering the same coping twice
        last_bot_msgs = [msg for role, msg in context if role == "assistant"]
        if last_bot_msgs:
            last_bot = last_bot_msgs[-1]
            # If the last bot message already contained a coping strategy,
            # we might choose a different one or simply reflect.
            # For simplicity, we'll just note it in a variable.
            pass

    # 4. Build response based on emotion
    if emotion == "sadness":
        return f"I hear that you're feeling sad. {get_coping_strategy('sadness')}"
    elif emotion == "anger":
        return f"It sounds like you're feeling angry. {get_coping_strategy('anger')}"
    elif emotion == "fear":
        return f"Feeling afraid can be overwhelming. {get_coping_strategy('fear')}"
    elif emotion == "anxiety":
        return f"I notice some anxiety in your words. {get_coping_strategy('anxiety')}"
    elif emotion == "joy":
        return f"I'm glad to hear you're feeling joyful! {get_coping_strategy('joy')}"
    elif emotion == "surprise":
        return f"That sounds surprising! {get_coping_strategy('surprise')}"
    else:
        # Neutral or other emotion
        return (
            f"Thank you for sharing. {get_coping_strategy('neutral')} "
            "I'm here to listen."
        )

# Optional: You can also add a function to generate a more personalized response
# if you store user mood history (from the database).