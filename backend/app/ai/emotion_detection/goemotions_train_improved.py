"""
=========================================================
Train Improved RoBERTa GoEmotions Multi-Label Classifier
Project : AI Mental Health Chatbot (FYP)

Dataset
-------
GoEmotions

Model
-----
RoBERTa-base

Task
----
Multi-Label Emotion Classification

Classes
-------
28 GoEmotions emotions

IMPORTANT
---------
This is a NEW model.
The original GoEmotions model is NOT overwritten.

Author : Shamsa Akram
=========================================================
"""

import ast
import json
from pathlib import Path

import numpy as np
import torch

from datasets import load_dataset

from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    set_seed,
)


# =========================================================
# Paths
# =========================================================

BACKEND_DIR = Path(
    __file__
).resolve().parents[1]


DATASET_DIR = (
    BACKEND_DIR
    / "datasets"
    / "processed_goemotions_multilabel"
)


MODEL_DIR = (
    BACKEND_DIR
    / "models"
    / "goemotions_roberta_improved"
)


LOG_DIR = (
    MODEL_DIR
    / "logs"
)


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# Seed
# =========================================================

set_seed(42)


# =========================================================
# Dataset Files
# =========================================================

TRAIN_PATH = (
    DATASET_DIR
    / "clean_train.csv"
)

VALID_PATH = (
    DATASET_DIR
    / "clean_dev.csv"
)

TEST_PATH = (
    DATASET_DIR
    / "clean_test.csv"
)


print("=" * 70)
print(
    "Improved RoBERTa GoEmotions Multi-Label Training"
)
print("=" * 70)


print("\nDataset paths:")

print(
    "Train      :",
    TRAIN_PATH
)

print(
    "Validation :",
    VALID_PATH
)

print(
    "Test       :",
    TEST_PATH
)


# =========================================================
# Check Files
# =========================================================

for path in [
    TRAIN_PATH,
    VALID_PATH,
    TEST_PATH
]:

    if not path.exists():

        raise FileNotFoundError(
            f"\nDataset file not found:\n{path}"
        )


# =========================================================
# Load Dataset
# =========================================================

print(
    "\nLoading processed dataset..."
)


dataset = load_dataset(
    "csv",
    data_files={
        "train": str(TRAIN_PATH),
        "validation": str(VALID_PATH),
        "test": str(TEST_PATH),
    },
)


print("\nDataset:")
print(dataset)


print("\nDataset sizes:")

print(
    "Train      :",
    len(dataset["train"])
)

print(
    "Validation :",
    len(dataset["validation"])
)

print(
    "Test       :",
    len(dataset["test"])
)


# =========================================================
# Convert labels from CSV strings to lists
# =========================================================

def parse_labels(example):

    labels = ast.literal_eval(
        example["labels"]
    )

    example["labels"] = [
        float(x)
        for x in labels
    ]

    return example


print(
    "\nConverting labels..."
)


dataset = dataset.map(
    parse_labels
)


# =========================================================
# Tokenizer
# =========================================================

print(
    "\nLoading RoBERTa-base tokenizer..."
)


tokenizer = AutoTokenizer.from_pretrained(
    "roberta-base"
)


# =========================================================
# Tokenization
# =========================================================

MAX_LENGTH = 128


def tokenize_function(batch):

    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=MAX_LENGTH,
    )


print(
    "\nTokenizing dataset..."
)


tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
)


# =========================================================
# Data Collator
# =========================================================

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)


# =========================================================
# Set Torch Format
# =========================================================

tokenized_dataset.set_format(
    type="torch",
    columns=[
        "input_ids",
        "attention_mask",
        "labels",
    ],
)


# =========================================================
# Model
# =========================================================

print(
    "\nLoading RoBERTa-base..."
)


model = AutoModelForSequenceClassification.from_pretrained(

    "roberta-base",

    num_labels=28,

    problem_type="multi_label_classification",

)


# =========================================================
# Metrics
# =========================================================

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    # Convert numpy arrays
    logits = np.asarray(logits)

    labels = np.asarray(labels)

    # Sigmoid
    probabilities = (
        1 /
        (
            1 +
            np.exp(-logits)
        )
    )

    # Initial threshold
    predictions = (
        probabilities >= 0.5
    ).astype(int)


    # Micro metrics
    micro_f1 = f1_score(
        labels,
        predictions,
        average="micro",
        zero_division=0,
    )

    # Macro metrics
    macro_f1 = f1_score(
        labels,
        predictions,
        average="macro",
        zero_division=0,
    )

    weighted_f1 = f1_score(
        labels,
        predictions,
        average="weighted",
        zero_division=0,
    )

    micro_precision = precision_score(
        labels,
        predictions,
        average="micro",
        zero_division=0,
    )

    micro_recall = recall_score(
        labels,
        predictions,
        average="micro",
        zero_division=0,
    )


    return {

        "micro_f1":
            micro_f1,

        "macro_f1":
            macro_f1,

        "weighted_f1":
            weighted_f1,

        "precision":
            micro_precision,

        "recall":
            micro_recall,

    }


# =========================================================
# Training Arguments
# =========================================================

training_args = TrainingArguments(

    output_dir=str(
        MODEL_DIR
    ),

    overwrite_output_dir=False,

    num_train_epochs=5,

    learning_rate=2e-5,

    per_device_train_batch_size=2,

    per_device_eval_batch_size=2,

    gradient_accumulation_steps=8,

    weight_decay=0.01,

    warmup_ratio=0.1,

    lr_scheduler_type="linear",

    eval_strategy="steps",

    eval_steps=500,

    save_strategy="steps",

    save_steps=500,

    save_total_limit=3,

    load_best_model_at_end=True,

    metric_for_best_model="eval_micro_f1",

    greater_is_better=True,

    logging_steps=100,

    logging_dir=str(
        LOG_DIR
    ),

    report_to="none",

    fp16=False,

    bf16=False,

    dataloader_num_workers=0,

    dataloader_pin_memory=False,

    remove_unused_columns=True,

    seed=42,

)


# =========================================================
# Trainer
# =========================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=tokenized_dataset[
        "train"
    ],

    eval_dataset=tokenized_dataset[
        "validation"
    ],

    tokenizer=tokenizer,

    data_collator=data_collator,

    compute_metrics=compute_metrics,

    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=3
        )
    ],
)


# =========================================================
# Training
# =========================================================

print("\n")
print("=" * 70)
print("TRAINING STARTED")
print("=" * 70)
print()


trainer.train()


# =========================================================
# Validation
# =========================================================

print("\n")
print("=" * 70)
print("VALIDATION EVALUATION")
print("=" * 70)
print()


validation_results = trainer.evaluate(
    tokenized_dataset[
        "validation"
    ]
)


for key, value in validation_results.items():

    print(
        f"{key} : {value}"
    )


# =========================================================
# Test
# =========================================================

print("\n")
print("=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)
print()


test_results = trainer.evaluate(
    tokenized_dataset[
        "test"
    ]
)


for key, value in test_results.items():

    print(
        f"{key} : {value}"
    )


# =========================================================
# Save Model
# =========================================================

print("\n")
print("=" * 70)
print("SAVING IMPROVED MODEL")
print("=" * 70)
print()


trainer.save_model(
    str(MODEL_DIR)
)


tokenizer.save_pretrained(
    str(MODEL_DIR)
)


# =========================================================
# Save Label Mapping
# =========================================================

label_mapping = {

    "0": "admiration",
    "1": "amusement",
    "2": "anger",
    "3": "annoyance",
    "4": "approval",
    "5": "caring",
    "6": "confusion",
    "7": "curiosity",
    "8": "desire",
    "9": "disappointment",
    "10": "disapproval",
    "11": "disgust",
    "12": "embarrassment",
    "13": "excitement",
    "14": "fear",
    "15": "gratitude",
    "16": "grief",
    "17": "joy",
    "18": "love",
    "19": "nervousness",
    "20": "optimism",
    "21": "pride",
    "22": "realization",
    "23": "relief",
    "24": "remorse",
    "25": "sadness",
    "26": "surprise",
    "27": "neutral"

}


with open(

    MODEL_DIR
    / "label_mapping.json",

    "w",

    encoding="utf-8"

) as file:

    json.dump(
        label_mapping,
        file,
        indent=4
    )


# =========================================================
# Save Evaluation Results
# =========================================================

results_file = (
    MODEL_DIR
    / "evaluation_results.txt"
)


with open(

    results_file,

    "w",

    encoding="utf-8"

) as file:

    file.write(
        "Improved GoEmotions "
        "RoBERTa Evaluation\n"
    )

    file.write(
        "=" * 70
        + "\n\n"
    )

    file.write(
        "Model: roberta-base\n"
    )

    file.write(
        "Dataset: GoEmotions\n"
    )

    file.write(
        "Task: Multi-Label Classification\n"
    )

    file.write(
        "Classes: 28\n\n"
    )


    file.write(
        "TRAINING SAMPLES: "
        + str(
            len(
                dataset["train"]
            )
        )
        + "\n"
    )

    file.write(
        "VALIDATION SAMPLES: "
        + str(
            len(
                dataset["validation"]
            )
        )
        + "\n"
    )

    file.write(
        "TEST SAMPLES: "
        + str(
            len(
                dataset["test"]
            )
        )
        + "\n\n"
    )


    file.write(
        "VALIDATION RESULTS\n"
    )

    file.write(
        "-" * 50
        + "\n"
    )


    for key, value in validation_results.items():

        file.write(
            f"{key} : {value}\n"
        )


    file.write(
        "\nTEST RESULTS\n"
    )

    file.write(
        "-" * 50
        + "\n"
    )


    for key, value in test_results.items():

        file.write(
            f"{key} : {value}\n"
        )


# =========================================================
# Final Summary
# =========================================================

print("\n")
print("=" * 70)
print("TRAINING COMPLETED")
print("=" * 70)

print(
    "\nModel:"
)

print(
    "RoBERTa-base"
)

print(
    "\nTask:"
)

print(
    "Multi-label emotion classification"
)

print(
    "\nClasses:"
)

print(
    "28"
)

print(
    "\nImproved model saved at:"
)

print(
    MODEL_DIR
)

print(
    "\nEvaluation results saved at:"
)

print(
    results_file
)

print(
    "\nThe original model was NOT overwritten."
)