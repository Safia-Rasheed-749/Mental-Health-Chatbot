"""
=========================================================
Depression Detection Prediction
Project : AI Mental Health Chatbot (FYP)
=========================================================
"""

import os
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# -----------------------------------------------------
# Model Path
# -----------------------------------------------------

MODEL_PATH = os.path.join(
    os.getcwd(),
    "models",
    "depression"
)

print("Loading Depression Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading Depression Model...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

labels = {
    0: "No Depression",
    1: "Depression"
}


# =====================================================
# Prediction Function (For FastAPI)
# =====================================================

def predict_depression(text: str):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

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

    return {
    "depression": labels[label],
    "label": label,
    "confidence": round(confidence.item() * 100, 2)
}

# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("\n==============================")
    print("Depression Prediction")
    print("==============================")

    while True:

        text = input("\nEnter Text (or type exit): ")

        if text.lower() == "exit":
            break

        prediction, confidence = predict_depression(text)

        print("\nPrediction")
        print("-------------------------")
        print(f"Depression : {prediction}")
        print(f"Confidence : {confidence} %")