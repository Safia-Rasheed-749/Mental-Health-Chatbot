"""
=========================================================
Depression Detection Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose:
    Load the trained RoBERTa depression model and
    predict Depression / No Depression.
=========================================================
"""

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

MODEL_PATH = BASE_DIR / "models" / "depression_v2"


# =====================================================
# Load Tokenizer
# =====================================================

print("Loading Depression Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)


# =====================================================
# Load Model
# =====================================================

print("Loading Depression RoBERTa Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)

model.eval()


# =====================================================
# Label Mapping
# =====================================================

LABEL_MAPPING = {
    0: "No Depression",
    1: "Depression",
}


# =====================================================
# Prediction Function
# =====================================================

def predict_depression(text: str) -> dict:
    """
    Predict depression from input text.

    Returns:
        {
            "depression": str,
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
        max_length=128,
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

    depression = LABEL_MAPPING.get(
        label,
        f"Unknown ({label})"
    )

    return {
        "depression": depression,
        "label": label,
        "confidence": round(
            confidence_value,
            2
        ),
    }


# =====================================================
# Interactive Testing
# =====================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Depression Prediction")
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

            result = predict_depression(text)

            print()
            print("Prediction")
            print("-" * 30)
            print(
                "Depression :",
                result["depression"]
            )
            print(
                "Label      :",
                result["label"]
            )
            print(
                "Confidence :",
                result["confidence"],
                "%"
            )

        except Exception as e:

            print()
            print("Prediction error:")
            print(e)