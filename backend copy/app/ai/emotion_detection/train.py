"""
=========================================================
Train RoBERTa Emotion Classifier
Project : AI Mental Health Chatbot (FYP)

Features
--------
1. Load processed GoEmotions dataset
2. Tokenize text
3. Fine-tune DistilRoBERTa
4. Resume automatically from latest checkpoint
5. Save checkpoints
6. Save best model
7. CPU Friendly
=========================================================
"""

import importlib.util
import os
from pathlib import Path
from transformers import DataCollatorWithPadding


# =====================================================
# Hugging Face Cache (Cross Platform)
# Centralized in app/ai/hf_cache.py
# Loaded by absolute file path so sys.path is never
# modified and installed packages are never shadowed.
# Must run before importing any Hugging Face library.
# =====================================================

HF_CACHE_PATH = Path(__file__).resolve().parents[1] / "hf_cache.py"

_hf_cache_spec = importlib.util.spec_from_file_location(
    "hf_cache", HF_CACHE_PATH
)
_hf_cache_module = importlib.util.module_from_spec(_hf_cache_spec)
_hf_cache_spec.loader.exec_module(_hf_cache_module)

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
    EarlyStoppingCallback,
    set_seed,
)

from transformers.trainer_utils import get_last_checkpoint

# =====================================================
# Startup Verification
# =====================================================
print("=" * 60)
print("RoBERTa Emotion Training Started")
print("=" * 60)

# =====================================================
# Project Paths
# =====================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

GOEMOTION_PATH = BACKEND_DIR / "datasets" / "processed"

MERGED_PATH = BACKEND_DIR / "datasets" / "final_emotion"

MODEL_SAVE_PATH = BACKEND_DIR / "models" / "emotion_roberta"
LOG_DIR = MODEL_SAVE_PATH / "logs"

MODEL_SAVE_PATH.mkdir(parents=True, exist_ok=True)

LOG_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Random Seed
# =====================================================

set_seed(42)

# =====================================================
# Load Dataset
# =====================================================

print("\nLoading Processed Dataset...\n")

dataset = load_dataset(
    "csv",
    data_files={
        "train": str(MERGED_PATH / "merged_train.csv"),
        "validation": str(GOEMOTION_PATH / "clean_dev.csv"),
    },
)


print(dataset)
print("\nDataset Information")
print("=" * 60)

print("Training Samples   :", len(dataset["train"]))
print("Validation Samples :", len(dataset["validation"]))

print("\nTraining Columns")
print(dataset["train"].column_names)

print("=" * 60)
# =====================================================
# Load Tokenizer
# =====================================================

print("\nLoading roberta-baseTokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "roberta-base"
)


# =====================================================
# Tokenization
# =====================================================

MAX_LENGTH = 64

def tokenize_function(example):

    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH
    )
data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)

print("\nTokenizing Dataset...\n")

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True
)

tokenized_dataset = tokenized_dataset.rename_column(
    "label",
    "labels"
)

tokenized_dataset.set_format(
    type="torch",
    columns=[
        "input_ids",
        "attention_mask",
        "labels"
    ]
)

# =====================================================
# Load Model (always from base, Trainer will restore checkpoint)
# =====================================================

print("\nLoading roberta-base Model...\n")

model = AutoModelForSequenceClassification.from_pretrained(
    "roberta-base",
    num_labels=28
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

    output_dir=str(MODEL_SAVE_PATH),

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

    dataloader_pin_memory=False,

    dataloader_num_workers=0,

    fp16=False,

    bf16=False,

    remove_unused_columns=False,

    seed=42,
)
resume_checkpoint = get_last_checkpoint(str(MODEL_SAVE_PATH))

print("\n===================================")

if resume_checkpoint is not None:

    print("Checkpoint Found")
    print(resume_checkpoint)
    print("Training will continue from checkpoint.")

else:

    print("No checkpoint found.")
    print("Training will start from beginning.")

print("===================================\n")

# -------------------------------------------------------
# Create Trainer
# -------------------------------------------------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=2
        )
    ]
)
# -------------------------------------------------------
# Train Model
# -------------------------------------------------------

print("\n===================================")
print("Training Started")
print("===================================\n")

trainer.train(
    resume_from_checkpoint=resume_checkpoint
)

# -------------------------------------------------------
# Evaluate Model
# -------------------------------------------------------

print("\n========================================")
print("Evaluating Model")
print("========================================\n")

results = trainer.evaluate()

print("\nEvaluation Results\n")

for key, value in results.items():

    print(f"{key} : {value}")

# -------------------------------------------------------
# Save Final Model
# -------------------------------------------------------

print("\n========================================")
print("Saving Final Model")
print("========================================\n")

trainer.save_model(str(MODEL_SAVE_PATH))

tokenizer.save_pretrained(str(MODEL_SAVE_PATH))

print("\nModel Saved Successfully!")

print(f"\nLocation : {MODEL_SAVE_PATH}")

# -------------------------------------------------------
# Save Evaluation Results
# -------------------------------------------------------

metrics_file = MODEL_SAVE_PATH / "evaluation_results.txt"

with open(metrics_file, "w") as f:

    f.write("RoBERTa Emotion Model Evaluation\n")
    f.write("=" * 50 + "\n\n")

    for key, value in results.items():
        f.write(f"{key} : {value}\n")

print("\nEvaluation report saved.")

print(metrics_file)

# -------------------------------------------------------
# Training Summary
# -------------------------------------------------------

print("\n========================================")
print("Training Completed Successfully")
print("========================================")

print("\nSummary")

print("----------------------------------------")

print("Model              : RoBERTa-base")
print("Number of Labels   : 28")
print(f"Epochs             : {training_args.num_train_epochs}")
print(f"Learning Rate      : {training_args.learning_rate}")
print(f"Batch Size         : {training_args.per_device_train_batch_size}")
print(f"Gradient Accum.    : {training_args.gradient_accumulation_steps}")
print(f"Output Directory   : {MODEL_SAVE_PATH}")
print(f"Logs Directory     : {LOG_DIR}")

print("----------------------------------------")

print("\nYour emotion detection model is now ready for inference.")
print("You can now use it in your chatbot.")