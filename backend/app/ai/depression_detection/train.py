"""
=========================================================
Train RoBERTa Depression Classifier - V2
Project : AI Mental Health Chatbot (FYP)

Dataset split:
    Train      : 5355
    Validation : 1147
    Test       : 1148

IMPORTANT:
    test.csv is NOT used during training.
    It is reserved exclusively for final evaluation.

Classes:
    0 = No Depression
    1 = Depression

Model:
    roberta-base
=========================================================
"""

import importlib.util
import json
import os
from pathlib import Path

# =========================================================
# Hugging Face Cache
# =========================================================

HF_CACHE_PATH = Path(__file__).resolve().parents[1] / "hf_cache.py"

_hf_cache_spec = importlib.util.spec_from_file_location(
    "hf_cache",
    HF_CACHE_PATH
)

_hf_cache_module = importlib.util.module_from_spec(
    _hf_cache_spec
)

_hf_cache_spec.loader.exec_module(
    _hf_cache_module
)

# =========================================================
# Imports
# =========================================================

import numpy as np

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    set_seed
)

from transformers.trainer_utils import get_last_checkpoint

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

# =========================================================
# Configuration
# =========================================================

MODEL_NAME = "roberta-base"

NUM_LABELS = 2

MAX_LENGTH = 128

SEED = 42

# =========================================================
# Paths - NEW V2 EXPERIMENT
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    BACKEND_DIR
    / "datasets"
    / "depression_v2"
    / "processed"
)

MODEL_SAVE_PATH = (
    BACKEND_DIR
    / "models"
    / "depression_v2"
)

LOG_DIR = MODEL_SAVE_PATH / "logs"

MODEL_SAVE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# Random Seed
# =========================================================

set_seed(SEED)

# =========================================================
# Startup
# =========================================================

print("=" * 70)
print("RoBERTa Depression Training - V2")
print("=" * 70)

print()
print("Model :", MODEL_NAME)
print("Labels:", NUM_LABELS)
print()

# =========================================================
# Dataset Paths
# =========================================================

TRAIN_PATH = DATASET_PATH / "train.csv"

VALIDATION_PATH = DATASET_PATH / "validation.csv"

TEST_PATH = DATASET_PATH / "test.csv"

print("=" * 70)
print("Dataset Paths")
print("=" * 70)

print("Train      :", TRAIN_PATH)
print("Validation :", VALIDATION_PATH)
print("Test       :", TEST_PATH)

# =========================================================
# Check Dataset Files
# =========================================================

if not TRAIN_PATH.exists():
    raise FileNotFoundError(
        f"Training dataset not found:\n{TRAIN_PATH}"
    )

if not VALIDATION_PATH.exists():
    raise FileNotFoundError(
        f"Validation dataset not found:\n{VALIDATION_PATH}"
    )

if not TEST_PATH.exists():
    raise FileNotFoundError(
        f"Test dataset not found:\n{TEST_PATH}"
    )

print()
print("All dataset files found.")

# =========================================================
# Load TRAIN + VALIDATION ONLY
# =========================================================

print()
print("=" * 70)
print("Loading Training and Validation Data")
print("=" * 70)
print()

dataset = load_dataset(
    "csv",
    data_files={
        "train": str(TRAIN_PATH),
        "validation": str(VALIDATION_PATH)
    }
)

print(dataset)

print()
print("=" * 70)
print("Dataset Information")
print("=" * 70)

print(
    "Training Samples   :",
    len(dataset["train"])
)

print(
    "Validation Samples :",
    len(dataset["validation"])
)

print(
    "Test Samples       :",
    1148,
    "(reserved separately; NOT loaded into Trainer)"
)

print(
    "Columns            :",
    dataset["train"].column_names
)

# =========================================================
# Check Labels
# =========================================================

train_labels = sorted(
    set(dataset["train"]["label"])
)

validation_labels = sorted(
    set(dataset["validation"]["label"])
)

print()
print("Training Labels   :", train_labels)
print("Validation Labels :", validation_labels)

if train_labels != [0, 1]:
    raise ValueError(
        f"Unexpected training labels: {train_labels}. "
        "Expected [0, 1]."
    )

if validation_labels != [0, 1]:
    raise ValueError(
        f"Unexpected validation labels: {validation_labels}. "
        "Expected [0, 1]."
    )

# =========================================================
# Load Tokenizer
# =========================================================

print()
print("=" * 70)
print("Loading RoBERTa-base Tokenizer")
print("=" * 70)
print()

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# =========================================================
# Tokenization
# =========================================================

def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )


print("Tokenizing Training + Validation Dataset...")
print()

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True
)

# =========================================================
# Rename Label Column
# =========================================================

tokenized_dataset = tokenized_dataset.rename_column(
    "label",
    "labels"
)

# =========================================================
# Torch Format
# =========================================================

tokenized_dataset.set_format(
    type="torch",
    columns=[
        "input_ids",
        "attention_mask",
        "labels"
    ]
)

# =========================================================
# Load FRESH RoBERTa Model
# =========================================================

print()
print("=" * 70)
print("Loading FRESH RoBERTa-base Model")
print("=" * 70)
print()

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label={
        0: "No Depression",
        1: "Depression"
    },
    label2id={
        "No Depression": 0,
        "Depression": 1
    }
)

# =========================================================
# Metrics
# =========================================================

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(
        logits,
        axis=-1
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            labels,
            predictions,
            average="binary",
            zero_division=0
        )
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

# =========================================================
# Training Arguments
# =========================================================

training_args = TrainingArguments(

    output_dir=str(
        MODEL_SAVE_PATH
    ),

    overwrite_output_dir=False,

    # -----------------------------
    # Training
    # -----------------------------

    num_train_epochs=4,

    learning_rate=2e-5,

    per_device_train_batch_size=4,

    per_device_eval_batch_size=4,

    gradient_accumulation_steps=1,

    weight_decay=0.01,

    # -----------------------------
    # Evaluation
    # -----------------------------

    eval_strategy="epoch",

    # -----------------------------
    # Checkpoint Saving
    # -----------------------------

    save_strategy="epoch",

    save_total_limit=2,

    save_only_model=True,

    # -----------------------------
    # Best Model
    # -----------------------------

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    greater_is_better=True,

    # -----------------------------
    # Logging
    # -----------------------------

    logging_steps=100,

    logging_dir=str(
        LOG_DIR
    ),

    # -----------------------------
    # Reporting
    # -----------------------------

    report_to="none",

    # -----------------------------
    # CPU-friendly settings
    # -----------------------------

    fp16=False,

    bf16=False,

    dataloader_num_workers=0,

    dataloader_pin_memory=False,

    # -----------------------------
    # Dataset
    # -----------------------------

    remove_unused_columns=True,

    # -----------------------------
    # Reproducibility
    # -----------------------------

    seed=SEED
)

# =========================================================
# Checkpoint Detection
# =========================================================

resume_checkpoint = get_last_checkpoint(
    str(MODEL_SAVE_PATH)
)

print()
print("=" * 70)

if resume_checkpoint is not None:

    print("V2 Checkpoint Found")
    print()
    print("Checkpoint:", resume_checkpoint)
    print()
    print("Training will resume from V2 checkpoint.")

else:

    print("No V2 Checkpoint Found")
    print()
    print("Training will start from roberta-base.")

print("=" * 70)
print()

# =========================================================
# Trainer
# =========================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=tokenized_dataset["train"],

    eval_dataset=tokenized_dataset["validation"],

    tokenizer=tokenizer,

    compute_metrics=compute_metrics
)

# =========================================================
# Training
# =========================================================

print("=" * 70)
print("Training Started")
print("=" * 70)
print()

train_result = trainer.train(
    resume_from_checkpoint=resume_checkpoint
)

# =========================================================
# Training Metrics
# =========================================================

print()
print("=" * 70)
print("Training Completed")
print("=" * 70)
print()

print("Training Metrics:")

for key, value in train_result.metrics.items():
    print(
        f"{key} : {value}"
    )

# =========================================================
# Validation Evaluation
# =========================================================

print()
print("=" * 70)
print("Evaluating Validation Set")
print("=" * 70)
print()

validation_results = trainer.evaluate()

print()
print("Validation Results")
print("=" * 70)

for key, value in validation_results.items():
    print(
        f"{key} : {value}"
    )

# =========================================================
# Save Best Model
# =========================================================

print()
print("=" * 70)
print("Saving Best V2 Model")
print("=" * 70)
print()

trainer.save_model(
    str(MODEL_SAVE_PATH)
)

tokenizer.save_pretrained(
    str(MODEL_SAVE_PATH)
)

# =========================================================
# Save Evaluation Results
# =========================================================

metrics_file = (
    MODEL_SAVE_PATH
    / "validation_results.txt"
)

with open(
    metrics_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "RoBERTa Depression Model V2 - Validation Evaluation\n"
    )

    f.write(
        "=" * 70
        + "\n\n"
    )

    f.write(
        f"Model : {MODEL_NAME}\n"
    )

    f.write(
        "Label Mapping : 0 = No Depression, 1 = Depression\n"
    )

    f.write(
        f"Number of Labels : {NUM_LABELS}\n"
    )

    f.write(
        f"Maximum Sequence Length : {MAX_LENGTH}\n"
    )

    f.write(
        f"Epochs : {training_args.num_train_epochs}\n"
    )

    f.write(
        f"Learning Rate : {training_args.learning_rate}\n"
    )

    f.write(
        f"Train Batch Size : "
        f"{training_args.per_device_train_batch_size}\n"
    )

    f.write(
        f"Training Samples : {len(dataset['train'])}\n"
    )

    f.write(
        f"Validation Samples : {len(dataset['validation'])}\n"
    )

    f.write(
        "Test Samples : 1148 (reserved for final testing)\n"
    )

    f.write(
        "\nTraining Metrics\n"
    )

    f.write(
        "-" * 70
        + "\n"
    )

    for key, value in train_result.metrics.items():
        f.write(
            f"{key} : {value}\n"
        )

    f.write(
        "\nValidation Metrics\n"
    )

    f.write(
        "-" * 70
        + "\n"
    )

    for key, value in validation_results.items():
        f.write(
            f"{key} : {value}\n"
        )

# =========================================================
# Save Training Configuration
# =========================================================

config_file = (
    MODEL_SAVE_PATH
    / "training_config.json"
)

training_config = {

    "model": MODEL_NAME,

    "num_labels": NUM_LABELS,

    "label_mapping": {
        "0": "No Depression",
        "1": "Depression"
    },

    "max_length": MAX_LENGTH,

    "epochs": training_args.num_train_epochs,

    "learning_rate": training_args.learning_rate,

    "train_batch_size":
        training_args.per_device_train_batch_size,

    "eval_batch_size":
        training_args.per_device_eval_batch_size,

    "weight_decay":
        training_args.weight_decay,

    "seed": SEED,

    "dataset_train":
        str(TRAIN_PATH),

    "dataset_validation":
        str(VALIDATION_PATH),

    "dataset_test":
        str(TEST_PATH),

    "training_samples":
        len(dataset["train"]),

    "validation_samples":
        len(dataset["validation"]),

    "test_samples":
        1148
}

with open(
    config_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        training_config,
        f,
        indent=4
    )

# =========================================================
# Final Summary
# =========================================================

print()
print("=" * 70)
print("V2 MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print()
print("Model             :", MODEL_NAME)

print(
    "Training Samples  :",
    len(dataset["train"])
)

print(
    "Validation Samples:",
    len(dataset["validation"])
)

print(
    "Test Samples      :",
    1148,
    "(NOT USED DURING TRAINING)"
)

print(
    "Number of Labels  :",
    NUM_LABELS
)

print(
    "Epochs            :",
    training_args.num_train_epochs
)

print(
    "Learning Rate     :",
    training_args.learning_rate
)

print(
    "Batch Size        :",
    training_args.per_device_train_batch_size
)

print()
print("Model Location:")
print(MODEL_SAVE_PATH)

print()
print("Validation Results:")

for key, value in validation_results.items():
    print(
        f"{key} : {value}"
    )

print()
print("Validation file:")
print(metrics_file)

print()
print("Training configuration:")
print(config_file)

print()
print("=" * 70)
print("V2 Depression Training Finished")
print("=" * 70)