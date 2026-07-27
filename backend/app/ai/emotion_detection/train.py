"""
=========================================================
Train DistilRoBERTa Emotion Classifier
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

import os
from pathlib import Path

# =====================================================
# HuggingFace Cache (D Drive)
# =====================================================

os.environ["HF_HOME"] = r"D:\AI_Cache\huggingface"
os.environ["HF_DATASETS_CACHE"] = r"D:\AI_Cache\datasets"
os.environ["TRANSFORMERS_CACHE"] = r"D:\AI_Cache\transformers"
os.environ["TORCH_HOME"] = r"D:\AI_Cache\torch"

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
print("NEW TRAIN.PY IS RUNNING")
print("=" * 60)

# =====================================================
# Project Paths
# =====================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = BACKEND_DIR / "datasets" / "processed"

MODEL_SAVE_PATH = BACKEND_DIR / "models" / "emotion"

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
        "train": str(DATASET_PATH / "clean_train.csv"),
        "validation": str(DATASET_PATH / "clean_dev.csv"),
    },
)

print(dataset)
# =====================================================
# Load Tokenizer
# =====================================================

print("\nLoading DistilRoBERTa Tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "distilroberta-base"
)

# =====================================================
# Tokenization
# =====================================================

def tokenize_function(example):

    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=96
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

print("\nLoading DistilRoBERTa Model...\n")

model = AutoModelForSequenceClassification.from_pretrained(
    "distilroberta-base",
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

    # ---------------------------------------
    # Output
    # ---------------------------------------

    output_dir=str(MODEL_SAVE_PATH),

    overwrite_output_dir=False,

    # ---------------------------------------
    # Training
    # ---------------------------------------

    num_train_epochs=5,

    learning_rate=2e-5,

    per_device_train_batch_size=1,

    per_device_eval_batch_size=1,

    gradient_accumulation_steps=8,

    weight_decay=0.01,

    # ---------------------------------------
    # Evaluation
    # ---------------------------------------

    eval_strategy="steps",

    eval_steps=500,

    # ---------------------------------------
    # Checkpoints
    # ---------------------------------------

    save_strategy="steps",

    save_steps=500,

    save_total_limit=3,

    save_only_model=False,

    save_safetensors=True,

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    greater_is_better=True,

    # ---------------------------------------
    # Logging
    # ---------------------------------------

    logging_strategy="steps",

    logging_steps=100,

    logging_dir=str(LOG_DIR),

    report_to="none",

    # ---------------------------------------
    # CPU Optimizations
    # ---------------------------------------

    dataloader_pin_memory=False,

    dataloader_num_workers=0,

    fp16=False,

    bf16=False,

    remove_unused_columns=False,

    seed=42
)

# -------------------------------------------------------
# Resume Training Automatically
# -------------------------------------------------------

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

    f.write("GoEmotions Model Evaluation\n")
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

print("Model              : DistilRoBERTa")
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