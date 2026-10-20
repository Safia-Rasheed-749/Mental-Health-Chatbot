# -*- coding: utf-8 -*-
"""
=========================================================
Train Stress Detection Model (RoBERTa-base)
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load processed dataset
2. Tokenize text using RoBERTa tokenizer
3. Fine-tune RoBERTa-base
4. Resume from checkpoint automatically
5. Save best model

Author : Shamsa Akram (modified)
=========================================================
"""

import importlib.util
import os
import glob
import random
from pathlib import Path

# =====================================================
# Hugging Face Cache (Cross Platform)
# =====================================================

HF_CACHE_PATH = Path(__file__).resolve().parents[1] / "hf_cache.py"

_hf_cache_spec = importlib.util.spec_from_file_location(
    "hf_cache", HF_CACHE_PATH
)
_hf_cache_module = importlib.util.module_from_spec(_hf_cache_spec)
_hf_cache_spec.loader.exec_module(_hf_cache_module)

import numpy as np

from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    set_seed,
)

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[3]
SEED = 42
DATASET_PATH = BACKEND_DIR / "datasets" / "stress" / "processed"

MODEL_SAVE_PATH = Path(os.getenv("STRESS_MODEL_OUTPUT_DIR", str(BACKEND_DIR / "models" / "stress_roberta")))

os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\nLoading Stress Dataset...\n")

set_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

source_train = load_dataset("csv", data_files={"train": str(DATASET_PATH / "clean_train.csv")})["train"].to_pandas()
train_frame, validation_frame = train_test_split(
    source_train,
    test_size=0.1,
    random_state=SEED,
    stratify=source_train["label"],
)
from datasets import Dataset, DatasetDict
dataset = DatasetDict({
    "train": Dataset.from_pandas(train_frame.reset_index(drop=True), preserve_index=False),
    "validation": Dataset.from_pandas(validation_frame.reset_index(drop=True), preserve_index=False),
})

print(dataset)

# -------------------------------------------------------
# Tokenizer (RoBERTa-base)
# -------------------------------------------------------

print("\nLoading RoBERTa-base Tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "roberta-base"   # changed from distilroberta-base
)

# -------------------------------------------------------
# Tokenization
# -------------------------------------------------------

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

print("\nTokenizing Dataset...\n")

tokenized_dataset = dataset.map(
    tokenize,
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

# -------------------------------------------------------
# Model (RoBERTa-base)
# -------------------------------------------------------

print("\nLoading RoBERTa-base Model...\n")

model = AutoModelForSequenceClassification.from_pretrained(
    "roberta-base",   # changed from distilroberta-base
    num_labels=2
)

# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary",
        zero_division=0
    )
    accuracy = accuracy_score(labels, predictions)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

# -------------------------------------------------------
# Training Arguments
# -------------------------------------------------------

training_args = TrainingArguments(
    output_dir=MODEL_SAVE_PATH,
    num_train_epochs=5,
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="steps",
    logging_steps=50,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    report_to="none",
    seed=SEED,
    data_seed=SEED,
)

# -------------------------------------------------------
# Trainer
# -------------------------------------------------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=2
        )
    ]
)

# -------------------------------------------------------
# Resume From Checkpoint
# -------------------------------------------------------

checkpoint_dirs = sorted(
    glob.glob(
        os.path.join(
            MODEL_SAVE_PATH,
            "checkpoint-*"
        )
    ),
    key=os.path.getmtime
)

resume_checkpoint = None
if len(checkpoint_dirs) > 0:
    resume_checkpoint = checkpoint_dirs[-1]
    print("\n===================================")
    print("Checkpoint Found")
    print("===================================")
    print("\nResuming From:\n")
    print(resume_checkpoint)
else:
    print("\n===================================")
    print("No Previous Checkpoint Found")
    print("Starting Fresh Training")
    print("===================================")

# -------------------------------------------------------
# Start Training
# -------------------------------------------------------

print("\n===================================")
print("Training Started...")
print("===================================\n")

trainer.train(
    resume_from_checkpoint=resume_checkpoint
)

# -------------------------------------------------------
# Evaluation
# -------------------------------------------------------

print("\n===================================")
print("Evaluating Model...")
print("===================================\n")

results = trainer.evaluate()
print(results)

# -------------------------------------------------------
# Save Final Model
# -------------------------------------------------------

print("\n===================================")
print("Saving Final Model...")
print("===================================\n")

trainer.save_model(MODEL_SAVE_PATH)
tokenizer.save_pretrained(MODEL_SAVE_PATH)

# -------------------------------------------------------
# Training Completed
# -------------------------------------------------------

print("\n===================================")
print("Training Completed Successfully")
print("===================================")

print("\nModel Saved At:\n")
print(MODEL_SAVE_PATH)
