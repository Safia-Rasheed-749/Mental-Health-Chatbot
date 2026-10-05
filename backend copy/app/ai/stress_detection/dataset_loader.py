"""
=========================================================
Stress Detection Dataset Loader
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load Dreaddit Dataset
2. Display Dataset Information
3. Check Missing Values
4. Remove Duplicate Rows
5. Save Clean Dataset

Author : Shamsa Akram
=========================================================
"""

import os
import pandas as pd

# -------------------------------------------------------
# Dataset Paths
# -------------------------------------------------------

RAW_DATASET_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "stress",
    "raw"
)

PROCESSED_DATASET_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "stress",
    "processed"
)

os.makedirs(PROCESSED_DATASET_PATH, exist_ok=True)

TRAIN_FILE = os.path.join(
    RAW_DATASET_PATH,
    "dreaddit-train.csv"
)

TEST_FILE = os.path.join(
    RAW_DATASET_PATH,
    "dreaddit-test.csv"
)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\n========================================")
print("Loading Dreaddit Dataset")
print("========================================\n")

train_df = pd.read_csv(TRAIN_FILE)

test_df = pd.read_csv(TEST_FILE)

# -------------------------------------------------------
# Keep Required Columns
# -------------------------------------------------------

train_df = train_df[
    [
        "text",
        "label"
    ]
]

test_df = test_df[
    [
        "text",
        "label"
    ]
]

# -------------------------------------------------------
# Dataset Information
# -------------------------------------------------------

print("Train Shape :", train_df.shape)

print("Test Shape  :", test_df.shape)

print("\nTrain Columns")

print(train_df.columns)

print("\nTest Columns")

print(test_df.columns)

# -------------------------------------------------------
# Missing Values
# -------------------------------------------------------

print("\nMissing Values (Train)\n")

print(train_df.isnull().sum())

print("\nMissing Values (Test)\n")

print(test_df.isnull().sum())

# -------------------------------------------------------
# Remove Missing Rows
# -------------------------------------------------------

train_df = train_df.dropna()

test_df = test_df.dropna()

# -------------------------------------------------------
# Remove Duplicate Rows
# -------------------------------------------------------

train_duplicates = train_df.duplicated().sum()

test_duplicates = test_df.duplicated().sum()

print("\nDuplicate Rows")

print("Train :", train_duplicates)

print("Test  :", test_duplicates)

train_df = train_df.drop_duplicates()

test_df = test_df.drop_duplicates()

# -------------------------------------------------------
# Save Clean Dataset
# -------------------------------------------------------

train_df.to_csv(

    os.path.join(
        PROCESSED_DATASET_PATH,
        "clean_train.csv"
    ),

    index=False
)

test_df.to_csv(

    os.path.join(
        PROCESSED_DATASET_PATH,
        "clean_test.csv"
    ),

    index=False
)

print("\n========================================")
print("Dataset Saved Successfully")
print("========================================")

print("\nSaved Location")

print(PROCESSED_DATASET_PATH)

print("\nTrain Samples :", len(train_df))

print("Test Samples  :", len(test_df))