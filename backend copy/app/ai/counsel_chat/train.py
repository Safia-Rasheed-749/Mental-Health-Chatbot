"""
=========================================================
Counsel Chat Trainer
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
1. Load processed Counsel Chat dataset
2. Tokenize question and answer
3. Fine-tune language model
4. Save checkpoints
5. Save final model

NOTE:
This file is prepared now.
Training will be done later on a 16 GB RAM machine.
=========================================================
"""

import os
from pathlib import Path
import pandas as pd

print("=" * 60)
print("Counsel Chat Training Pipeline")
print("=" * 60)

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    BACKEND_DIR /
    "datasets" /
    "counsel_chat" /
    "processed" /
    "train_processed.csv"
)

MODEL_DIR = (
    BACKEND_DIR /
    "models" /
    "counsel_chat"
)

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

print("\nLoading Dataset...\n")

df = pd.read_csv(DATASET_PATH)

print(df.head())

print("\nTotal Samples :", len(df))

print("\nColumns")

print(df.columns.tolist())

print("\n")

print("=" * 60)
print("Dataset Ready")
print("=" * 60)

print("""
Next Step (Later)

Load Tokenizer
↓

Load Language Model

↓

Tokenize Question

↓

Tokenize Therapist Answer

↓

Fine-tune

↓

Save Model
""")