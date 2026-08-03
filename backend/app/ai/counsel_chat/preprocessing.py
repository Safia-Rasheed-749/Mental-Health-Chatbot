"""
=========================================================
Counsel Chat Dataset Preprocessing
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
1. Load Counsel Chat Dataset
2. Remove missing values
3. Remove duplicate rows
4. Clean text
5. Save processed dataset

Author : Shamsa Akram
=========================================================
"""

import pandas as pd
import re

# Load Dataset
df = pd.read_csv(
    "datasets/counsel_chat/raw/train.csv"
)

# -----------------------------------------------------
# Remove Missing Values
# -----------------------------------------------------

df = df.dropna(
    subset=["questionText", "answerText"]
)

# -----------------------------------------------------
# Remove Duplicates
# -----------------------------------------------------

df = df.drop_duplicates()

# -----------------------------------------------------
# Text Cleaning Function
# -----------------------------------------------------

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\\S+", "", text)

    text = re.sub(r"www\\S+", "", text)

    text = re.sub(r"\\s+", " ", text)

    return text.strip()

# -----------------------------------------------------
# Clean Question
# -----------------------------------------------------

df["questionText"] = df["questionText"].apply(clean_text)

# -----------------------------------------------------
# Clean Answer
# -----------------------------------------------------

df["answerText"] = df["answerText"].apply(clean_text)

# -----------------------------------------------------
# Save Processed Dataset
# -----------------------------------------------------

df.to_csv(
    "datasets/counsel_chat/processed/train_processed.csv",
    index=False
)

print("="*50)
print("Counsel Chat Preprocessing Completed")
print("="*50)

print("\nProcessed Samples :", len(df))

print("\nSaved Successfully")

print("\ndatasets/counsel_chat/processed/train_processed.csv")