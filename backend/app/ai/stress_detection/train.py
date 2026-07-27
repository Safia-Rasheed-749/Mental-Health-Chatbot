"""
=========================================================
Train Stress Detection Model
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load processed dataset
2. Tokenize text
3. Fine-tune DistilRoBERTa
4. Resume from checkpoint automatically
5. Save best model

Author : Shamsa Akram
=========================================================
"""

import os
import glob
import numpy as np

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

DATASET_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "stress",
    "processed"
)

MODEL_SAVE_PATH = os.path.join(
    os.getcwd(),
    "models",
    "stress"
)

os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\nLoading Stress Dataset...\n")

dataset = load_dataset(
    "csv",
    data_files={
        "train": os.path.join(DATASET_PATH, "clean_train.csv"),
        "validation": os.path.join(DATASET_PATH, "clean_test.csv")
    }
)

print(dataset)

# -------------------------------------------------------
# Tokenizer
# -------------------------------------------------------

print("\nLoading DistilRoBERTa Tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "distilroberta-base"
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
# Model
# -------------------------------------------------------

print("\nLoading DistilRoBERTa Model...\n")

model = AutoModelForSequenceClassification.from_pretrained(

    "distilroberta-base",

    num_labels=2

)

# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(

        logits,

        axis=-1

    )

    precision, recall, f1, _ = precision_recall_fscore_support(

        labels,

        predictions,

        average="binary",

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

    report_to="none"

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

trainer.save_model(

    MODEL_SAVE_PATH

)

tokenizer.save_pretrained(

    MODEL_SAVE_PATH

)

# -------------------------------------------------------
# Training Completed
# -------------------------------------------------------

print("\n===================================")
print("Training Completed Successfully")
print("===================================")

print("\nModel Saved At:\n")

print(MODEL_SAVE_PATH)