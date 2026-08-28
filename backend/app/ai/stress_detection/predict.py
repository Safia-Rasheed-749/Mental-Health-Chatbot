"""
=========================================================
Stress Detection Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
1. Load trained RoBERTa Stress model
2. Load tokenizer
3. Predict Stress / No Stress
4. Return prediction for FastAPI
=========================================================
"""

import json
from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[3]

# Best checkpoint according to validation accuracy
MODEL_PATH = BASE_DIR / "models" / "stress_roberta"


# =====================================================
# Load Tokenizer
# =====================================================

print("Loading Stress Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)


# =====================================================
# Load Model
# =====================================================

print("Loading Stress RoBERTa Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)

model.eval()


# =====================================================
# Label Mapping
# =====================================================

label_mapping = {
    0: "No Stress",
    1: "Stress",
}


# =====================================================
# Prediction Function
# =====================================================

def predict_stress(text: str) -> dict:
    """
    Predict whether the given text indicates stress.

    Args:
        text:
            User input text.

    Returns:
        Dictionary containing:
            stress
            label
            confidence
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1,
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1,
        )

    label = prediction.item()

    return {
        "stress": label_mapping[label],
        "label": label,
        "confidence": round(
            confidence.item() * 100,
            2,
        ),
    }


# =====================================================
# Interactive Testing
# =====================================================

if __name__ == "__main__":

    print("\n==============================")
    print("Stress Prediction")
    print("==============================")

    print(f"Model path: {MODEL_PATH}")

    while True:

        text = input(
            "\nEnter Text (or type exit): "
        )

        if text.lower() == "exit":
            break

        try:

            result = predict_stress(text)

            print("\nPrediction")
            print("-------------------------")
            print("Stress     :", result["stress"])
            print("Label      :", result["label"])
            print(
                "Confidence :",
                result["confidence"],
                "%",
            )

        except Exception as e:

            print("\nError:", e)