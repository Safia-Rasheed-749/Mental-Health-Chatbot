"""
============================================================
Depression Dataset Preprocessing
Project : AI Mental Health Chatbot
============================================================
"""

import os
import re
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

INPUT_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "processed",
    "clean_dataset.csv"
)

OUTPUT_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "processed",
    "clean_dataset.csv"
)

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

print("\n========================================")
print("Loading Depression Dataset")
print("========================================\n")

df = pd.read_csv(INPUT_PATH)

# ---------------------------------------------------------
# Text Cleaning Function
# ---------------------------------------------------------

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\\S+", "", text)

    text = re.sub(r"www\\S+", "", text)

    text = re.sub(r"[^a-zA-Z\\s]", " ", text)

    text = re.sub(r"\\s+", " ", text).strip()

    return text

# ---------------------------------------------------------
# Apply Cleaning
# ---------------------------------------------------------

print("Cleaning Text...\n")

df["text"] = df["text"].apply(clean_text)

# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ---------------------------------------------------------
# Information
# ---------------------------------------------------------

print("========================================")
print("Preprocessing Completed Successfully")
print("========================================")

print("\nTotal Samples :", len(df))

print("\nExample Sentence:\n")

print(df["text"].iloc[0])