from app.ai.emotion_detection.predict import predict_emotion
from app.ai.stress_detection.predict import predict_stress
from app.ai.depression_detection.predict import predict_depression


def analyze_text(text: str):

    emotion_result = predict_emotion(text)

    stress_result = predict_stress(text)

    depression_result = predict_depression(text)

    return {

        "emotion": emotion_result["emotion"],
        "emotion_confidence": emotion_result["confidence"],

        "stress": stress_result["stress"],
        "stress_confidence": stress_result["confidence"],

        "depression": depression_result["depression"],
        "depression_confidence": depression_result["confidence"]

    }