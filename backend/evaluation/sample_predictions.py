"""
=========================================================
Sample Prediction
Project : AI Mental Health Chatbot

Runs all trained models together.

Author : Shamsa Akram
=========================================================
"""

from app.ai.emotion_detection.predict import predict_emotion
from app.ai.stress_detection.predict import predict_stress

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

# -------------------------------------------------------
# Depression Model
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "depression"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

labels = {
    0: "No Depression",
    1: "Depression"
}

def predict_depression(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)

        confidence, prediction = torch.max(probs, dim=1)

    return {
        "depression": labels[prediction.item()],
        "confidence": round(confidence.item()*100,2)
    }


print("="*60)
print("Mental Health Chatbot Prediction")
print("="*60)

while True:

    text = input("\nEnter your sentence (type exit to quit): ")

    if text.lower()=="exit":
        break

    emotion = predict_emotion(text)

    stress = predict_stress(text)

    depression = predict_depression(text)

    print("\n==============================")
    print("Prediction Results")
    print("==============================")

    print(f"Emotion     : {emotion['emotion']} ({emotion['confidence']}%)")

    print(f"Stress      : {stress['stress']} ({stress['confidence']}%)")

    print(f"Depression  : {depression['depression']} ({depression['confidence']}%)")