"""
=========================================================
Train RoBERTa Mental Health Classifier
Project : AI Mental Health Chatbot (FYP)

Dataset
-------
Reddit Mental Health Dataset

Classes
-------
ADHD
OCD
PTSD
Depression
Aspergers

Model
-----
RoBERTa-base

Features
--------
1. Load processed dataset
2. Merge title + body
3. Encode labels
4. Tokenize text
5. Fine-tune RoBERTa
6. Evaluate
7. Save best model
=========================================================
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from datasets import Dataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers.trainer_utils import get_last_checkpoint
from transformers import EarlyStoppingCallback
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    set_seed,
)

# =====================================================
# Paths
# =====================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    BACKEND_DIR
    / "datasets"
    / "reddit_mental_health"
    / "processed"
    / "train_processed.csv"
)

MODEL_DIR = (
    BACKEND_DIR
    / "models"
    / "reddit_mental_health"
)

MODEL_DIR.mkdir(parents=True, exist_ok=True)

set_seed(42)

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

df["text"] = df["title"] + " " + df["body"]

encoder = LabelEncoder()

df["label"] = encoder.fit_transform(df["subreddit"])

mapping = {
    int(i): label
    for i, label in enumerate(encoder.classes_)
}

with open(
    MODEL_DIR / "label_mapping.json",
    "w"
) as f:

    json.dump(mapping, f, indent=4)

train_df, valid_df = train_test_split(

    df,

    test_size=0.10,

    random_state=42,

    stratify=df["label"]

)

train_dataset = Dataset.from_pandas(

    train_df[
        [
            "text",
            "label"
        ]
    ]
)

valid_dataset = Dataset.from_pandas(

    valid_df[
        [
            "text",
            "label"
        ]
    ]
)

print()

print("Training Samples :", len(train_dataset))
print("Validation Samples :", len(valid_dataset))

# =====================================================
# Tokenizer
# =====================================================

print("\nLoading Tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "roberta-base"
)

def tokenize(batch):

    return tokenizer(

        batch["text"],

        truncation=True,

        padding="max_length",

        max_length=128

    )

train_dataset = train_dataset.map(
    tokenize,
    batched=True
)

valid_dataset = valid_dataset.map(
    tokenize,
    batched=True
)

train_dataset = train_dataset.rename_column(
    "label",
    "labels"
)

valid_dataset = valid_dataset.rename_column(
    "label",
    "labels"
)

train_dataset.set_format(

    "torch",

    columns=[
        "input_ids",
        "attention_mask",
        "labels"
    ]

)

valid_dataset.set_format(

    "torch",

    columns=[
        "input_ids",
        "attention_mask",
        "labels"
    ]

)

# =====================================================
# Model
# =====================================================

print("\nLoading RoBERTa...\n")

model = AutoModelForSequenceClassification.from_pretrained(

    "roberta-base",

    num_labels=5

)

# =====================================================
# Metrics
# =====================================================

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(logits, axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(

        labels,

        predictions,

        average="weighted",

        zero_division=0

    )

    accuracy = accuracy_score(

        labels,

        predictions

    )

    return {

        "accuracy": accuracy,

        "precision": precision,

        "recall": recall,

        "f1": f1

    }

# =====================================================
# Training Arguments
# =====================================================

training_args = TrainingArguments(

    output_dir=str(MODEL_DIR),

    overwrite_output_dir=False,

    num_train_epochs=3,

    learning_rate=2e-5,

    per_device_train_batch_size=2,

    per_device_eval_batch_size=2,

    gradient_accumulation_steps=8,

    weight_decay=0.01,

    # -----------------------------
    # Evaluation / Saving
    # -----------------------------

    eval_strategy="steps",

    eval_steps=500,

    save_strategy="steps",  

    save_steps=500,

    save_total_limit=3,

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    greater_is_better=True,

    # -----------------------------
    # Logging
    # -----------------------------

    logging_steps=100,

    logging_dir=str(MODEL_DIR / "logs"),

    report_to="none",

    # -----------------------------
    # CPU configuration
    # -----------------------------

    fp16=False,

    bf16=False,

    dataloader_num_workers=0,

    dataloader_pin_memory=False,

    remove_unused_columns=True,

    save_only_model=False,

    # -----------------------------
    # Reproducibility
    # -----------------------------

    seed=42
)
# =====================================================

resume_checkpoint = get_last_checkpoint(str(MODEL_DIR))

if resume_checkpoint is not None:

    resume_checkpoint = get_last_checkpoint(str(MODEL_DIR))

print("\n===================================")

if resume_checkpoint is not None:

    print("Checkpoint Found")
    print(resume_checkpoint)
    print("Training will continue from checkpoint.")

else:

    print("No checkpoint found.")
    print("Training will start from beginning.")

print("===================================\n")
print("\n===================================")

if resume_checkpoint is not None:

    print("Valid Checkpoint Found")
    print(resume_checkpoint)
    print("Training will continue from checkpoint.")

else:

    print("No valid checkpoint found.")
    print("Training will start from beginning.")

print("===================================\n")
# =====================================================
# Trainer
# =====================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=valid_dataset,

    tokenizer=tokenizer,

    compute_metrics=compute_metrics,

    callbacks=[
    EarlyStoppingCallback(
        early_stopping_patience=3
    )
]
)
# =====================================================
# Train
# =====================================================

print("\nTraining Started\n")

trainer.train(
    resume_from_checkpoint=resume_checkpoint
)
# =====================================================
# Evaluate
# =====================================================

results = trainer.evaluate()

print()

for k, v in results.items():

    print(k, ":", v)

# =====================================================
# Save Model
# =====================================================

trainer.save_model(str(MODEL_DIR))

tokenizer.save_pretrained(str(MODEL_DIR))

print("\nModel Saved Successfully!")

print(MODEL_DIR)