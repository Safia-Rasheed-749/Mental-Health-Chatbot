"""
=========================================================
Emotion Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose:
    Load the trained RoBERTa emotion model and predict
    the emotion of the user's current text.
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

MODEL_PATH = BASE_DIR / "models" / "emotion_dair_ai_roberta"

LABEL_MAPPING_PATH = MODEL_PATH / "label_mapping.json"


# =====================================================
# Load Tokenizer
# =====================================================

print("Loading Emotion Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)


# =====================================================
# Load Model
# =====================================================

print("Loading Emotion RoBERTa Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)

model.eval()


# =====================================================
# Load Label Mapping
# =====================================================

print("Loading Emotion Label Mapping...")

with open(
    LABEL_MAPPING_PATH,
    "r",
    encoding="utf-8"
) as f:
    label_mapping = json.load(f)


# JSON keys are strings, so convert them to integers
label_mapping = {
    int(key): value
    for key, value in label_mapping.items()
}


# =====================================================
# Prediction Function
# =====================================================

def predict_emotion(text: str) -> dict:
    """
    Predict emotion from input text.

    Returns:
        {
            "emotion": str,
            "label": int,
            "confidence": float
        }
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    # -------------------------------------------------
    # Tokenization
    # -------------------------------------------------

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=96,
    )

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    label = prediction.item()

    confidence_value = confidence.item() * 100

    emotion = label_mapping.get(
        label,
        f"Unknown ({label})"
    )

    return {
        "emotion": emotion,
        "label": label,
        "confidence": round(confidence_value, 2),
    }


# =====================================================
# Interactive Testing
# =====================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Emotion Prediction")
    print("=" * 60)

    while True:

        text = input(
            "\nEnter Text (or type exit): "
        ).strip()

        if text.lower() == "exit":
            print("Exiting...")
            break

        if not text:
            print("Please enter some text.")
            continue

        try:

            result = predict_emotion(text)

            print()
            print("Prediction")
            print("-" * 30)
            print("Emotion    :", result["emotion"])
            print("Label      :", result["label"])
            print(
                "Confidence :",
                result["confidence"],
                "%"
            )

        except Exception as e:

            print()
            print("Prediction error:")
            print(e)