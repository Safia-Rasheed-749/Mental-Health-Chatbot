"""
============================================================
Depression Dataset Loader
Project : AI Mental Health Chatbot
============================================================
"""

import os
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

RAW_DATA = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "raw",
    "depression_dataset_reddit_cleaned.csv"
)

PROCESSED_DIR = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "processed"
)

os.makedirs(PROCESSED_DIR, exist_ok=True)

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

print("\n========================================")
print("Loading Depression Dataset")
print("========================================\n")

df = pd.read_csv(RAW_DATA)

# ---------------------------------------------------------
# Keep Required Columns
# ---------------------------------------------------------

df = df[
    [
        "clean_text",
        "is_depression"
    ]
]

# Rename Columns

df.columns = [
    "text",
    "label"
]

# ---------------------------------------------------------
# Remove Duplicates
# ---------------------------------------------------------

duplicates = df.duplicated().sum()

df.drop_duplicates(inplace=True)

# ---------------------------------------------------------
# Missing Values
# ---------------------------------------------------------

df.dropna(inplace=True)

# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

SAVE_PATH = os.path.join(
    PROCESSED_DIR,
    "clean_dataset.csv"
)

df.to_csv(
    SAVE_PATH,
    index=False
)

# ---------------------------------------------------------
# Information
# ---------------------------------------------------------

print("Dataset Shape :", df.shape)

print("\nColumns")

print(df.columns)

print("\nMissing Values\n")

print(df.isnull().sum())

print("\nDuplicate Rows Removed :", duplicates)

print("\n========================================")
print("Dataset Saved Successfully")
print("========================================")

print("\nSaved Location")

print(SAVE_PATH)

print("\nTotal Samples :", len(df))