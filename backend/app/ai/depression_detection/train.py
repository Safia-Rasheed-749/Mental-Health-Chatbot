"""
=========================================================
Train DistilRoBERTa Depression Classifier
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load processed dataset
2. Tokenize data
3. Fine-tune DistilRoBERTa
4. Resume training automatically
5. Save trained model

Author : Shamsa Akram (FYP)
=========================================================
"""

import os
import numpy as np

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
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
    "depression",
    "processed"
)

MODEL_SAVE_PATH = os.path.join(
    os.getcwd(),
    "models",
    "depression"
)

os.makedirs(
    MODEL_SAVE_PATH,
    exist_ok=True
)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\nLoading Depression Dataset...\n")

dataset = load_dataset(
    "csv",
    data_files={
        "train": os.path.join(
            DATASET_PATH,
            "train.csv"
        ),
        "validation": os.path.join(
            DATASET_PATH,
            "validation.csv"
        )
    }
)
print(dataset)

# -------------------------------------------------------
# Load Tokenizer
# -------------------------------------------------------

print("\nLoading DistilRoBERTa Tokenizer...\n")

tokenizer = AutoTokenizer.from_pretrained(
    "distilroberta-base"
)

# -------------------------------------------------------
# Tokenization
# -------------------------------------------------------

def tokenize_function(example):

    return tokenizer(

        example["text"],

        truncation=True,

        padding="max_length",

        max_length=128
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

# -------------------------------------------------------
# Load Model
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

# -------------------------------------------------------
# Training Arguments
# -------------------------------------------------------

training_args = TrainingArguments(

    output_dir=MODEL_SAVE_PATH,

    num_train_epochs=4,

    learning_rate=2e-5,

    per_device_train_batch_size=4,

    per_device_eval_batch_size=4,

    weight_decay=0.01,

    eval_strategy="epoch",

    save_strategy="epoch",

    logging_steps=100,

    save_total_limit=2,

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

    tokenizer=tokenizer,

    compute_metrics=compute_metrics
)
# -------------------------------------------------------
# Resume Training (Automatic)
# -------------------------------------------------------

checkpoint = None

checkpoints = [

    os.path.join(MODEL_SAVE_PATH, folder)

    for folder in os.listdir(MODEL_SAVE_PATH)

    if folder.startswith("checkpoint-")
]

if len(checkpoints) > 0:

    checkpoint = max(
        checkpoints,
        key=os.path.getmtime
    )

    print("\n===================================")
    print("Previous Checkpoint Found")
    print("Resuming Training...")
    print(checkpoint)
    print("===================================\n")

else:

    print("\n===================================")
    print("No Previous Checkpoint Found")
    print("Starting Fresh Training")
    print("===================================\n")

# -------------------------------------------------------
# Start Training
# -------------------------------------------------------

print("===================================")
print("Training Started...")
print("===================================\n")

trainer.train(
    resume_from_checkpoint=checkpoint
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

print("\n===================================")
print("Training Completed Successfully")
print("===================================\n")

print("Model Saved At:\n")

print(MODEL_SAVE_PATH)