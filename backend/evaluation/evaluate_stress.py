"""
=========================================================
Evaluate Stress Detection Model
Project : AI Mental Health Chatbot (FYP)

This script:

1. Loads trained Stress Detection model
2. Loads test dataset
3. Predicts labels
4. Calculates metrics
5. Saves classification report
6. Saves confusion matrix
=========================================================
"""

from pathlib import Path

import pandas as pd
import torch

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Project Paths
# =====================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BACKEND_DIR / "models" / "stress"

DATA_PATH = (
    BACKEND_DIR
    / "datasets"
    / "stress"
    / "processed"
    / "clean_test.csv"
)

RESULT_PATH = BACKEND_DIR / "evaluation"

RESULT_PATH.mkdir(exist_ok=True)

# =====================================================
# Device
# =====================================================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("Loading Stress Model...")
print("=" * 60)

# =====================================================
# Load Model
# =====================================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(device)

model.eval()

# =====================================================
# Load Dataset
# =====================================================

print("\nLoading Stress Test Dataset...\n")

df = pd.read_csv(DATA_PATH)

texts = df["text"].tolist()

true_labels = df["label"].tolist()

predictions = []

# =====================================================
# Prediction Loop
# =====================================================

print("Running Predictions...\n")

for text in texts:

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=96
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():

        outputs = model(**inputs)

        pred = torch.argmax(outputs.logits, dim=1).item()

    predictions.append(pred)

# =====================================================
# Metrics
# =====================================================

accuracy = accuracy_score(true_labels, predictions)

precision, recall, f1, _ = precision_recall_fscore_support(
    true_labels,
    predictions,
    average="weighted",
    zero_division=0
)

print("=" * 60)
print("Stress Model Evaluation")
print("=" * 60)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

# =====================================================
# Classification Report
# =====================================================

report = classification_report(
    true_labels,
    predictions,
    zero_division=0
)

report_file = RESULT_PATH / "stress_classification_report.txt"

with open(report_file, "w") as f:
    f.write(report)

print("\nClassification report saved.")

# =====================================================
# Confusion Matrix
# =====================================================

cm = confusion_matrix(
    true_labels,
    predictions
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Stress Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    RESULT_PATH / "stress_confusion_matrix.png"
)

plt.close()

print("Confusion matrix saved.")

# =====================================================
# Save Metrics
# =====================================================

metrics_file = RESULT_PATH / "stress_metrics.txt"

with open(metrics_file, "w") as f:

    f.write(f"Accuracy  : {accuracy}\n")
    f.write(f"Precision : {precision}\n")
    f.write(f"Recall    : {recall}\n")
    f.write(f"F1 Score  : {f1}\n")

print("Metrics saved.")

print("\nEvaluation Completed Successfully!")