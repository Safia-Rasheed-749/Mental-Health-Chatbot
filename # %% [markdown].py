# %% [markdown]
# # Emotion Detection using RoBERTa-base
# 
# ## Project
# AI Mental Health Chatbot — Final Year Project
# 
# ## Dataset
# dair-ai/emotion
# 
# ## Task
# Multi-class emotion classification
# 
# ## Number of Classes
# 6
# 
# ## Classes
# 0 — Sadness
# 1 — Joy
# 2 — Love
# 3 — Anger
# 4 — Fear
# 5 — Surprise
# 
# ## Base Model
# RoBERTa-base
# 
# ## Fine-tuned Model
# emotion_dair_ai_roberta

# %%
import os
import json
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import torch

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

print("Environment loaded successfully.")
print("PyTorch version:", torch.__version__)
print("Device:", "cuda" if torch.cuda.is_available() else "cpu")

# %%
from pathlib import Path

BACKEND_DIR = Path.cwd().parent

RAW_DIR = BACKEND_DIR / "datasets" / "emotion_dataset" / "raw"
PROCESSED_DIR = BACKEND_DIR / "datasets" / "emotion_dataset" / "processed"
MODEL_DIR = BACKEND_DIR / "models" / "emotion_dair_ai_roberta"
EVALUATION_DIR = BACKEND_DIR / "evaluation"

print("Backend:", BACKEND_DIR)
print("Raw:", RAW_DIR)
print("Processed:", PROCESSED_DIR)
print("Model:", MODEL_DIR)
print("Evaluation:", EVALUATION_DIR)

# %%
train_raw = pd.read_csv(RAW_DIR / "train.csv")
val_raw = pd.read_csv(RAW_DIR / "validation.csv")
test_raw = pd.read_csv(RAW_DIR / "test.csv")

print("Raw Train:", train_raw.shape)
print("Raw Validation:", val_raw.shape)
print("Raw Test:", test_raw.shape)

# %%
display(train_raw.head())

# %%
print("Columns:", train_raw.columns.tolist())

# %%
print([name for name in globals() if not name.startswith("_")])

# %%
print(train_raw.dtypes)

# %%
print("Train missing values:")
display(train_raw.isnull().sum())

print("Validation missing values:")
display(val_raw.isnull().sum())

print("Test missing values:")
display(test_raw.isnull().sum())

# %%
print("Train duplicate rows:", train_raw.duplicated().sum())
print("Validation duplicate rows:", val_raw.duplicated().sum())
print("Test duplicate rows:", test_raw.duplicated().sum())

# %%
print("Train duplicate rows:", train_raw.duplicated().sum())
print("Validation duplicate rows:", val_raw.duplicated().sum())
print("Test duplicate rows:", test_raw.duplicated().sum())

# %%
def clean(df):
    df = df.drop_duplicates()
    df = df.dropna()

    df["text"] = (
        df["text"]
        .str.lower()
        .str.strip()
    )

    return df

# %%
train = clean(train_raw.copy())
val = clean(val_raw.copy())
test = clean(test_raw.copy())

# %%
print("Processed Train:", train.shape)
print("Processed Validation:", val.shape)
print("Processed Test:", test.shape)

print("Total processed:",
      len(train) + len(val) + len(test))

# %%
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

train.to_csv(
    PROCESSED_DIR / "train_processed.csv",
    index=False
)

val.to_csv(
    PROCESSED_DIR / "validation_processed.csv",
    index=False
)

test.to_csv(
    PROCESSED_DIR / "test_processed.csv",
    index=False
)

print("Processed datasets saved successfully.")

# %%
print("Train label distribution:")
display(train["label"].value_counts().sort_index())

print("Validation label distribution:")
display(val["label"].value_counts().sort_index())

print("Test label distribution:")
display(test["label"].value_counts().sort_index())

# %%
label_counts = train["label"].value_counts().sort_index()

plt.figure(figsize=(7, 4))
plt.bar(label_counts.index.astype(str), label_counts.values)
plt.title("Emotion Class Distribution - Training Set")
plt.xlabel("Emotion Label")
plt.ylabel("Number of Samples")
plt.show()

# %%
label_mapping = {
    0: "Sadness",
    1: "Joy",
    2: "Love",
    3: "Anger",
    4: "Fear",
    5: "Surprise"
}

label_mapping

# %%
for label_id, emotion in label_mapping.items():
    print(f"\n===== {emotion} ({label_id}) =====")

    samples = train[
        train["label"] == label_id
    ]["text"].head(3)

    for i, text in enumerate(samples, 1):
        print(f"{i}. {text}")

# %% [markdown]
# ## Model Configuration
# 
# - Base model: RoBERTa-base
# - Number of classes: 6
# - Maximum sequence length: 128
# - Epochs: 3
# - Learning rate: 2e-5
# - Training batch size: 4
# - Evaluation batch size: 4
# - Gradient accumulation steps: 2
# - Weight decay: 0.01
# - Optimizer: AdamW (`adamw_torch_fused`)
# - Random seed: 42
# - Best model criterion: validation accuracy

# %%
tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_DIR)
)

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_DIR)
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)
model.eval()

print("Model loaded successfully.")
print("Device:", device)
print("Number of classes:", model.config.num_labels)

# %%
test_df = pd.read_csv(
    PROCESSED_DIR / "test_processed.csv"
)

texts = test_df["text"].astype(str).tolist()
true_labels = test_df["label"].astype(int).tolist()

predicted_labels = []
prediction_confidences = []

BATCH_SIZE = 16

start_time = time.time()

for start in range(0, len(texts), BATCH_SIZE):

    batch_texts = texts[start:start + BATCH_SIZE]

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

evaluation_time = time.time() - start_time

print("Evaluation time:", round(evaluation_time, 2), "seconds")

# %%
accuracy = accuracy_score(
    true_labels,
    predicted_labels
)

precision, recall, f1, _ = (
    precision_recall_fscore_support(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0
    )
)

macro_precision, macro_recall, macro_f1, _ = (
    precision_recall_fscore_support(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0
    )
)

print("Accuracy:", accuracy)
print("Weighted Precision:", precision)
print("Weighted Recall:", recall)
print("Weighted F1:", f1)
print("Macro Precision:", macro_precision)
print("Macro Recall:", macro_recall)
print("Macro F1:", macro_f1)

# %%
target_labels = sorted(
    set(true_labels) | set(predicted_labels)
)

target_names = [
    label_mapping[label]
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

print(report)

# %%
target_labels = sorted(
    set(true_labels) | set(predicted_labels)
)

target_names = [
    label_mapping[label]
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

print(report)

# %%
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(
    true_labels,
    predicted_labels
)

print("Confusion Matrix:")
print(cm)

# %%
plt.figure(figsize=(9, 7))

plt.imshow(cm)

plt.title("Emotion Detection - Confusion Matrix")

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

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
plt.show()

# %%
results_df = test_df.copy()

results_df["predicted_label"] = predicted_labels
results_df["prediction_confidence"] = prediction_confidences

results_df["actual_emotion"] = (
    results_df["label"].map(label_mapping)
)

results_df["predicted_emotion"] = (
    results_df["predicted_label"].map(label_mapping)
)

results_df["correct"] = (
    results_df["label"] ==
    results_df["predicted_label"]
)

display(results_df.head(10))

# %%
wrong_predictions = results_df[
    results_df["correct"] == False
]

print("Wrong predictions:", len(wrong_predictions))

display(
    wrong_predictions.head(10)
)

# %%
print("=" * 60)
print("FINAL EMOTION TEST RESULTS")
print("=" * 60)

print(f"Test Samples        : {len(test_df)}")
print(f"Accuracy            : {accuracy * 100:.2f}%")
print(f"Weighted Precision   : {precision * 100:.2f}%")
print(f"Weighted Recall      : {recall * 100:.2f}%")
print(f"Weighted F1          : {f1 * 100:.2f}%")
print(f"Macro Precision      : {macro_precision * 100:.2f}%")
print(f"Macro Recall         : {macro_recall * 100:.2f}%")
print(f"Macro F1             : {macro_f1 * 100:.2f}%")
print(f"Correct Predictions  : {int(results_df['correct'].sum())}")
print(f"Wrong Predictions    : {int((~results_df['correct']).sum())}")
print(f"Evaluation Time      : {evaluation_time:.2f} seconds")

# %%
trainer_state_path = (
    MODEL_DIR /
    "checkpoint-6000" /
    "trainer_state.json"
)

with open(trainer_state_path, "r", encoding="utf-8") as f:
    trainer_state = json.load(f)

history = pd.DataFrame(
    trainer_state["log_history"]
)

history.head()

# %%
train_history = history[
    history["loss"].notna()
]

plt.figure(figsize=(8, 5))
plt.plot(
    train_history["step"],
    train_history["loss"]
)
plt.xlabel("Training Step")
plt.ylabel("Training Loss")
plt.title("Emotion Model Training Loss")
plt.show()

# %% [markdown]
# ## Conclusion
# 
# The RoBERTa-base model was fine-tuned for six-class emotion classification using the dair-ai/emotion dataset. The raw data was cleaned by removing duplicate and missing records and by converting text to lowercase and removing leading/trailing whitespace. The processed dataset contained separate training, validation, and testing subsets.
# 
# The trained model was evaluated on the independent test split. The final evaluation included accuracy, weighted and macro precision, recall, F1-score, classification report, and confusion matrix. Individual predictions and incorrect predictions were also inspected for error analysis.

# %%
eval_history = history[
    history["eval_accuracy"].notna()
]

plt.figure(figsize=(8, 5))
plt.plot(
    eval_history["step"],
    eval_history["eval_accuracy"]
)
plt.xlabel("Training Step")
plt.ylabel("Validation Accuracy")
plt.title("Emotion Model Validation Accuracy")
plt.show()


