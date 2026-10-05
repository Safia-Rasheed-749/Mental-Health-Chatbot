import os
import json
import time
import numpy as np
import pandas as pd
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "emotion_dair_ai_roberta"
)

TEST_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "emotion_dataset",
    "processed",
    "test_processed.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "evaluation"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# FILE PATHS
# ============================================================

METRICS_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_metrics.txt"
)

REPORT_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_classification_report.txt"
)

CONFUSION_MATRIX_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_confusion_matrix.png"
)

PREDICTIONS_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_predictions.csv"
)

RAW_PREDICTIONS_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_wrong_predictions.csv"
)

LABEL_MAPPING_FILE = os.path.join(
    OUTPUT_DIR,
    "emotion_label_mapping.json"
)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("RoBERTa Emotion Detection Evaluation")
print("=" * 70)

print("\nModel:")
print(MODEL_PATH)

print("\nTest Dataset:")
print(TEST_PATH)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"\nModel not found:\n{MODEL_PATH}"
    )

if not os.path.exists(TEST_PATH):
    raise FileNotFoundError(
        f"\nTest dataset not found:\n{TEST_PATH}"
    )


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 70)
print("Loading Test Dataset")
print("=" * 70)

df = pd.read_csv(TEST_PATH)

print("\nDataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

if "text" not in df.columns:
    raise ValueError(
        "The test dataset does not contain a 'text' column."
    )

if "label" not in df.columns:
    raise ValueError(
        "The test dataset does not contain a 'label' column."
    )


# ============================================================
# CLEAN BASIC VALUES
# ============================================================

df = df.dropna(subset=["text", "label"]).copy()

df["text"] = df["text"].astype(str)

df["label"] = pd.to_numeric(
    df["label"],
    errors="raise"
).astype(int)

print("\nSamples after basic validation:", len(df))


# ============================================================
# DETERMINE LABEL NAMES
# ============================================================

if "emotion" in df.columns:

    label_mapping = (
        df[["label", "emotion"]]
        .drop_duplicates()
        .sort_values("label")
    )

    label_names = {}

    for _, row in label_mapping.iterrows():
        label_names[int(row["label"])] = str(row["emotion"])

else:

    unique_labels = sorted(df["label"].unique())

    label_names = {
        int(label): str(label)
        for label in unique_labels
    }


print("\nLabel Mapping:")

for label_id, label_name in label_names.items():
    print(f"{label_id} -> {label_name}")


with open(LABEL_MAPPING_FILE, "w", encoding="utf-8") as f:
    json.dump(
        label_names,
        f,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("\n" + "=" * 70)
print("Loading Tokenizer")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "=" * 70)
print("Loading Trained Model")
print("=" * 70)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()

print("\nModel loaded successfully.")

print("\nNumber of labels:",
      model.config.num_labels)

print("\nModel label configuration:")

if hasattr(model.config, "id2label"):
    print(model.config.id2label)


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)

print("\nDevice:", device)

if torch.cuda.is_available():
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================================
# PREDICTION
# ============================================================

print("\n" + "=" * 70)
print("Running Test Predictions")
print("=" * 70)

texts = df["text"].tolist()
true_labels = df["label"].tolist()

predicted_labels = []
prediction_confidences = []

batch_size = 16

start_time = time.time()

for start in range(0, len(texts), batch_size):

    batch_texts = texts[
        start:start + batch_size
    ]

    encoded = tokenizer(
        batch_texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

    encoded = {
        key: value.to(device)
        for key, value in encoded.items()
    }

    with torch.no_grad():

        outputs = model(**encoded)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        predictions = torch.argmax(
            probabilities,
            dim=-1
        )

        confidences = torch.max(
            probabilities,
            dim=-1
        ).values

    predicted_labels.extend(
        predictions.cpu().numpy().tolist()
    )

    prediction_confidences.extend(
        confidences.cpu().numpy().tolist()
    )

    processed = min(
        start + batch_size,
        len(texts)
    )

    print(
        f"\rProcessed {processed}/{len(texts)}",
        end=""
    )

evaluation_time = time.time() - start_time

print("\n")
print(
    f"Evaluation time: {evaluation_time:.2f} seconds"
)


# ============================================================
# METRICS
# ============================================================

print("\n" + "=" * 70)
print("Calculating Metrics")
print("=" * 70)

accuracy = accuracy_score(
    true_labels,
    predicted_labels
)

precision, recall, f1, _ = precision_recall_fscore_support(
    true_labels,
    predicted_labels,
    average="weighted",
    zero_division=0
)

macro_precision, macro_recall, macro_f1, _ = \
    precision_recall_fscore_support(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0
    )


# ============================================================
# PRINT RESULTS
# ============================================================

print("\nFinal Test Results")

print("-" * 50)

print(
    f"Accuracy          : {accuracy:.6f} "
    f"({accuracy * 100:.2f}%)"
)

print(
    f"Weighted Precision : {precision:.6f} "
    f"({precision * 100:.2f}%)"
)

print(
    f"Weighted Recall    : {recall:.6f} "
    f"({recall * 100:.2f}%)"
)

print(
    f"Weighted F1       : {f1:.6f} "
    f"({f1 * 100:.2f}%)"
)

print(
    f"Macro Precision   : {macro_precision:.6f}"
)

print(
    f"Macro Recall      : {macro_recall:.6f}"
)

print(
    f"Macro F1          : {macro_f1:.6f}"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

target_labels = sorted(
    set(true_labels) |
    set(predicted_labels)
)

target_names = [
    label_names.get(
        label,
        str(label)
    )
    for label in target_labels
]

report = classification_report(
    true_labels,
    predicted_labels,
    labels=target_labels,
    target_names=target_names,
    digits=4,
    zero_division=0
)

print("\n" + "=" * 70)
print("Classification Report")
print("=" * 70)

print(report)


# ============================================================
# SAVE CLASSIFICATION REPORT
# ============================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "RoBERTa Emotion Detection "
        "Classification Report\n"
    )

    f.write("=" * 70 + "\n\n")

    f.write(
        f"Model: roberta-base / "
        f"emotion_dair_ai_roberta\n"
    )

    f.write(
        f"Dataset: dair-ai/emotion\n"
    )

    f.write(
        f"Test Samples: {len(df)}\n\n"
    )

    f.write(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    true_labels,
    predicted_labels,
    labels=target_labels
)

print("\n" + "=" * 70)
print("Confusion Matrix")
print("=" * 70)

print(cm)


# ============================================================
# PLOT CONFUSION MATRIX
# ============================================================

plt.figure(
    figsize=(9, 7)
)

plt.imshow(cm)

plt.title(
    "Emotion Detection - Confusion Matrix"
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "Actual Label"
)

plt.xticks(
    range(len(target_names)),
    target_names,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(target_names)),
    target_names
)

for i in range(cm.shape[0]):

    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.colorbar()

plt.tight_layout()

plt.savefig(
    CONFUSION_MATRIX_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# SAVE PREDICTIONS
# ============================================================

results_df = df.copy()

results_df["predicted_label"] = predicted_labels

results_df["prediction_confidence"] = \
    prediction_confidences

results_df["actual_emotion"] = (
    results_df["label"]
    .map(label_names)
)

results_df["predicted_emotion"] = (
    results_df["predicted_label"]
    .map(label_names)
)

results_df["correct"] = (
    results_df["label"]
    ==
    results_df["predicted_label"]
)

results_df.to_csv(
    PREDICTIONS_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# SAVE WRONG PREDICTIONS
# ============================================================

wrong_predictions = results_df[
    results_df["correct"] == False
].copy()

wrong_predictions.to_csv(
    RAW_PREDICTIONS_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# SAVE METRICS
# ============================================================

with open(
    METRICS_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EMOTION DETECTION - EVALUATION RESULTS\n"
    )

    f.write("=" * 70 + "\n\n")

    f.write(
        "MODEL INFORMATION\n"
    )

    f.write(
        "Pretrained/Base Model: roberta-base\n"
    )

    f.write(
        "Fine-tuned Model: emotion_dair_ai_roberta\n"
    )

    f.write(
        "Dataset: dair-ai/emotion\n"
    )

    f.write(
        f"Test Samples: {len(df)}\n"
    )

    f.write(
        f"Number of Classes: {len(target_labels)}\n"
    )

    f.write(
        f"Device: {device}\n\n"
    )

    f.write(
        "LABEL MAPPING\n"
    )

    for label_id, label_name in label_names.items():

        f.write(
            f"{label_id} = {label_name}\n"
        )

    f.write("\n")

    f.write(
        "TEST METRICS\n"
    )

    f.write(
        f"Accuracy: {accuracy:.6f} "
        f"({accuracy * 100:.2f}%)\n"
    )

    f.write(
        f"Weighted Precision: {precision:.6f} "
        f"({precision * 100:.2f}%)\n"
    )

    f.write(
        f"Weighted Recall: {recall:.6f} "
        f"({recall * 100:.2f}%)\n"
    )

    f.write(
        f"Weighted F1: {f1:.6f} "
        f"({f1 * 100:.2f}%)\n"
    )

    f.write(
        f"Macro Precision: {macro_precision:.6f}\n"
    )

    f.write(
        f"Macro Recall: {macro_recall:.6f}\n"
    )

    f.write(
        f"Macro F1: {macro_f1:.6f}\n"
    )

    f.write(
        f"Evaluation Time: {evaluation_time:.2f} seconds\n"
    )

    f.write(
        f"Correct Predictions: "
        f"{int(results_df['correct'].sum())}\n"
    )

    f.write(
        f"Wrong Predictions: "
        f"{int((~results_df['correct']).sum())}\n"
    )

    f.write("\n")

    f.write(
        "CONFUSION MATRIX\n"
    )

    f.write(
        np.array2string(cm)
    )

    f.write("\n\n")

    f.write(
        "CLASSIFICATION REPORT\n"
    )

    f.write(report)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated files:")

print(
    "1.",
    METRICS_FILE
)

print(
    "2.",
    REPORT_FILE
)

print(
    "3.",
    CONFUSION_MATRIX_FILE
)

print(
    "4.",
    PREDICTIONS_FILE
)

print(
    "5.",
    RAW_PREDICTIONS_FILE
)

print(
    "6.",
    LABEL_MAPPING_FILE
)

print("\nEvaluation finished.")