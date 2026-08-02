"""
=========================================================
Emotion Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load trained DistilRoBERTa model
2. Load tokenizer
3. Predict emotion
4. Return emotion name
=========================================================
"""

import json
from pathlib import Path

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "models" / "emotion"

# -----------------------------------------------------
# Load Tokenizer
# -----------------------------------------------------

print("Loading Emotion Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# -----------------------------------------------------
# Load Model
# -----------------------------------------------------

print("Loading Emotion Model...")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# -----------------------------------------------------
# Load Label Mapping
# -----------------------------------------------------

label_file = MODEL_PATH / "label_mapping.json"

with open(label_file, "r") as f:
    label_mapping = json.load(f)

# -----------------------------------------------------
# Prediction Function
# -----------------------------------------------------

def predict_emotion(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=96
    )

    with torch.no_grad():

        outputs = model(**inputs)

        prediction = torch.argmax(outputs.logits, dim=1).item()

        confidence = torch.softmax(outputs.logits, dim=1)[0][prediction].item()

    emotion = label_mapping[str(prediction)]

    return {
        "emotion": emotion,
        "label": prediction,
        "confidence": round(confidence * 100, 2)
    }


# -----------------------------------------------------
# Interactive Testing
# -----------------------------------------------------

if __name__ == "__main__":

    print("\n==============================")
    print("Emotion Prediction")
    print("==============================")

    while True:

        text = input("\nEnter Text (or type exit): ")

        if text.lower() == "exit":
            break

        result = predict_emotion(text)

        print("\nPrediction")
        print("---------------------")
        print("Emotion   :", result["emotion"])
        print("Label     :", result["label"])
        print("Confidence:", result["confidence"], "%")