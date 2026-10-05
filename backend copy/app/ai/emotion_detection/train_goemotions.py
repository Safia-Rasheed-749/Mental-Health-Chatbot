"""
=========================================================
Train RoBERTa GoEmotions Classifier
Project : AI Mental Health Chatbot (FYP)

Dataset
-------
GoEmotions

Model
-----
RoBERTa-base

Classes
-------
28 GoEmotions emotion classes

Features
--------
1. Load GoEmotions train/validation/test datasets
2. Tokenize text
3. Fine-tune RoBERTa-base
4. Evaluate accuracy, precision, recall and F1
5. Save checkpoints
6. Save final model
7. Save evaluation results
=========================================================
"""

import json
from pathlib import Path

import numpy as np
from datasets import load_dataset
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    set_seed,
)

from transformers.trainer_utils import get_last_checkpoint


# =====================================================
# Paths
# =====================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

DATASET_DIR = BACKEND_DIR / "datasets" / "processed"

MODEL_DIR = BACKEND_DIR / "models" / "goemotions_roberta"

LOG_DIR = MODEL_DIR / "logs"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Seed
# =====================================================

set_seed(42)


# =====================================================
# Dataset Paths
# =====================================================

TRAIN_PATH = DATASET_DIR / "clean_train.csv"
VALID_PATH = DATASET_DIR / "clean_dev.csv"
TEST_PATH = DATASET_DIR / "clean_test.csv"


print("=" * 60)
print("RoBERTa GoEmotions Training")
print("=" * 60)

print("\nDataset files:")

print("Train      :", TRAIN_PATH)
print("Validation :", VALID_PATH)
print("Test       :", TEST_PATH)


# =====================================================
# Check Files
# =====================================================

for path in [TRAIN_PATH, VALID_PATH, TEST_PATH]:

    if not path.exists():

        raise FileNotFoundError(
            f"\nDataset file not found:\n{path}"
        )


# =====================================================
# Load Dataset
# =====================================================

print("\nLoading GoEmotions dataset...\n")

dataset = load_dataset(
    "csv",
    data_files={
        "train": str(TRAIN_PATH),
        "validation": str(VALID_PATH),
        "test": str(TEST_PATH),
    },
)

print(dataset)

print("\nDataset Sizes")
print("=" * 60)

print("Training samples   :", len(dataset["train"]))
print("Validation samples :", len(dataset["validation"]))
print("Test samples       :", len(dataset["test"]))


# =====================================================
# Inspect Columns
# =====================================================

print("\nDataset columns:")

print(dataset["train"].column_names)


# =====================================================
# Tokenizer
# =====================================================

print("\nLoading RoBERTa-base tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "roberta-base"
)


# =====================================================
# Tokenization
# =====================================================

MAX_LENGTH = 128


def tokenize_function(batch):

    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=MAX_LENGTH,
    )


print("\nTokenizing datasets...\n")

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
)


# =====================================================
# Rename Label
# =====================================================

tokenized_dataset = tokenized_dataset.rename_column(
    "label",
    "labels"
)


# =====================================================
# Data Collator
# =====================================================

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)


# =====================================================
# Torch Format
# =====================================================

tokenized_dataset.set_format(
    type="torch",
    columns=[
        "input_ids",
        "attention_mask",
        "labels",
    ],
)


# =====================================================
# Model
# =====================================================

print("\nLoading RoBERTa-base model...\n")

model = AutoModelForSequenceClassification.from_pretrained(
    "roberta-base",
    num_labels=28,
)


# =====================================================
# Metrics
# =====================================================

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
            average="weighted",
            zero_division=0,
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
        "f1": f1,
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

    gradient_accumulation_steps=4,

    weight_decay=0.01,

    eval_strategy="steps",

    eval_steps=500,

    save_strategy="steps",

    save_steps=500,

    save_total_limit=3,

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    greater_is_better=True,

    logging_steps=100,

    logging_dir=str(LOG_DIR),

    report_to="none",

    fp16=False,

    bf16=False,

    dataloader_num_workers=0,

    dataloader_pin_memory=False,

    remove_unused_columns=True,

    seed=42,
)


# =====================================================
# Checkpoint Detection
# =====================================================

resume_checkpoint = get_last_checkpoint(
    str(MODEL_DIR)
)


print("\n===================================")

if resume_checkpoint:

    print("Checkpoint Found")
    print(resume_checkpoint)
    print("Training will continue from checkpoint.")

else:

    print("No checkpoint found.")
    print("Training will start from beginning.")

print("===================================\n")


# =====================================================
# Trainer
# =====================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=tokenized_dataset["train"],

    eval_dataset=tokenized_dataset["validation"],

    tokenizer=tokenizer,

    data_collator=data_collator,

    compute_metrics=compute_metrics,
)


# =====================================================
# Training
# =====================================================

print("\n===================================")
print("Training Started")
print("===================================\n")


trainer.train(
    resume_from_checkpoint=resume_checkpoint
)


# =====================================================
# Validation Evaluation
# =====================================================

print("\n===================================")
print("Validation Evaluation")
print("===================================\n")


validation_results = trainer.evaluate(
    tokenized_dataset["validation"]
)


for key, value in validation_results.items():

    print(
        f"{key} : {value}"
    )


# =====================================================
# Test Evaluation
# =====================================================

print("\n===================================")
print("Final Test Evaluation")
print("===================================\n")


test_results = trainer.evaluate(
    tokenized_dataset["test"]
)


for key, value in test_results.items():

    print(
        f"{key} : {value}"
    )


# =====================================================
# Save Model
# =====================================================

print("\n===================================")
print("Saving Final Model")
print("===================================\n")


trainer.save_model(
    str(MODEL_DIR)
)

tokenizer.save_pretrained(
    str(MODEL_DIR)
)


# =====================================================
# Save Evaluation Results
# =====================================================

results_file = MODEL_DIR / "evaluation_results.txt"


with open(
    results_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "GoEmotions RoBERTa Evaluation Results\n"
    )

    f.write("=" * 60 + "\n\n")

    f.write(
        "Model: roberta-base\n"
    )

    f.write(
        "Dataset: GoEmotions\n"
    )

    f.write(
        "Number of classes: 28\n\n"
    )

    f.write(
        "TRAINING SAMPLES: "
        + str(len(dataset["train"]))
        + "\n"
    )

    f.write(
        "VALIDATION SAMPLES: "
        + str(len(dataset["validation"]))
        + "\n"
    )

    f.write(
        "TEST SAMPLES: "
        + str(len(dataset["test"]))
        + "\n\n"
    )

    f.write(
        "VALIDATION RESULTS\n"
    )

    f.write("-" * 40 + "\n")

    for key, value in validation_results.items():

        f.write(
            f"{key} : {value}\n"
        )

    f.write(
        "\nTEST RESULTS\n"
    )

    f.write("-" * 40 + "\n")

    for key, value in test_results.items():

        f.write(
            f"{key} : {value}\n"
        )


# =====================================================
# Final Summary
# =====================================================

print("\n===================================")
print("Training Completed")
print("===================================")

print("\nModel              : RoBERTa-base")
print("Dataset            : GoEmotions")
print("Number of Labels   : 28")
print("Epochs             :", training_args.num_train_epochs)
print("Learning Rate      :", training_args.learning_rate)
print(
    "Batch Size         :",
    training_args.per_device_train_batch_size
)
print(
    "Gradient Accum.    :",
    training_args.gradient_accumulation_steps
)

print("\nModel saved at:")
print(MODEL_DIR)

print("\nEvaluation saved at:")
print(results_file)

print("\nGoEmotions model is ready.")