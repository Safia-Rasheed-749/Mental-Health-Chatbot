"""
=========================================================
Stress Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load trained DistilRoBERTa Stress model
2. Predict Stress / No Stress
=========================================================
"""

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

MODEL_PATH = BASE_DIR / "models" / "stress"

# -----------------------------------------------------
# Load Tokenizer
# -----------------------------------------------------

print("Loading Stress Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# -----------------------------------------------------
# Load Model
# -----------------------------------------------------

print("Loading Stress Model...")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# -----------------------------------------------------
# Label Mapping
# -----------------------------------------------------

label_mapping = {
    0: "No Stress",
    1: "Stress"
}

# -----------------------------------------------------
# Prediction Function
# -----------------------------------------------------

def predict_stress(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():

        outputs = model(**inputs)

        prediction = torch.argmax(outputs.logits, dim=1).item()

        confidence = torch.softmax(outputs.logits, dim=1)[0][prediction].item()

    return {
        "stress": label_mapping[prediction],
        "label": prediction,
        "confidence": round(confidence * 100, 2)
    }

# -----------------------------------------------------
# Interactive Testing
# -----------------------------------------------------

if __name__ == "__main__":

    print("\n==============================")
    print("Stress Prediction")
    print("==============================")

    while True:

        text = input("\nEnter Text (or type exit): ")

        if text.lower() == "exit":
            break

        result = predict_stress(text)

        print("\nPrediction")
        print("-------------------------")
        print("Stress     :", result["stress"])
        print("Label      :", result["label"])
        print("Confidence :", result["confidence"], "%")