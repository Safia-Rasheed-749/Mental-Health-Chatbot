# -*- coding: utf-8 -*-
"""
=========================================================
Reddit Mental Health Topic Prediction
Project : AI Mental Health Chatbot (FYP)

Purpose:
    Load the fine-tuned RoBERTa model trained on Reddit
    mental-health data and predict the most likely
    mental-health topic for the user's current text.

Labels (5-class):
    0 → ADHD
    1 → OCD
    2 → aspergers
    3 → depression
    4 → ptsd
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

MODEL_PATH           = BASE_DIR / "models" / "reddit_mental_health"
LABEL_MAPPING_PATH   = MODEL_PATH / "label_mapping.json"


# =====================================================
# Load Tokenizer
# =====================================================

print("Loading Reddit Mental Health Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)


# =====================================================
# Load Model
# =====================================================

print("Loading Reddit Mental Health RoBERTa Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
)

model.eval()


# =====================================================
# Load Label Mapping
# =====================================================

print("Loading Reddit Mental Health Label Mapping...")

with open(LABEL_MAPPING_PATH, "r", encoding="utf-8") as f:
    _raw_mapping = json.load(f)

# JSON keys are strings — convert to integers
LABEL_MAPPING: dict[int, str] = {
    int(k): v for k, v in _raw_mapping.items()
}
# {0: "ADHD", 1: "OCD", 2: "aspergers", 3: "depression", 4: "ptsd"}


# =====================================================
# Prediction Function
# =====================================================

def predict_mental_health_topic(text: str) -> dict:
    """
    Predict the most likely mental-health topic from input text.

    The model was trained on Reddit mental-health community posts.
    It classifies text into one of five categories:
        ADHD | OCD | aspergers | depression | ptsd

    This signal is intended as an *auxiliary* context hint for the
    LLM prompt — it does NOT constitute a diagnosis.

    Args:
        text: Raw user message string.

    Returns:
        {
            "mental_health_topic":      str,    # e.g. "depression"
            "label":                    int,    # 0–4
            "confidence":               float,  # percentage, rounded to 2 dp
            "all_scores":               dict,   # {label_name: confidence_%}
        }

    Raises:
        TypeError:  if text is not a string.
        ValueError: if text is empty after stripping.
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
    # Inference
    # -------------------------------------------------

    with torch.no_grad():
        outputs       = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)

    label            = prediction.item()
    confidence_value = round(confidence.item() * 100, 2)
    topic            = LABEL_MAPPING.get(label, f"unknown ({label})")

    # Build a full score breakdown — useful for the LLM mental_state prompt
    all_scores: dict[str, float] = {
        LABEL_MAPPING[i]: round(probabilities[0][i].item() * 100, 2)
        for i in range(len(LABEL_MAPPING))
    }

    return {
        "mental_health_topic": topic,
        "label":               label,
        "confidence":          confidence_value,
        "all_scores":          all_scores,
    }


# =====================================================
# Interactive Testing
# =====================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Reddit Mental Health Topic Prediction")
    print("=" * 60)

    test_inputs = [
        "I can't focus on anything. My mind is always jumping to the next thing.",
        "I keep checking if I locked the door. I've done it 10 times already.",
        "I find social cues really confusing. People say things they don't mean.",
        "I feel empty and hopeless. Nothing brings me joy anymore.",
        "I keep having nightmares about what happened. I can't stop reliving it.",
    ]

    for text in test_inputs:
        result = predict_mental_health_topic(text)
        print(f"\nInput     : {text}")
        print(f"Topic     : {result['mental_health_topic']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"All scores: {result['all_scores']}")
