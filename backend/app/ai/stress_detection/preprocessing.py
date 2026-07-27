"""
=========================================================
Stress Detection Dataset Preprocessing
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load Clean Dataset
2. Clean Text
3. Save Processed Dataset

Author : Shamsa Akram
=========================================================
"""

import os
import re
import pandas as pd

# -------------------------------------------------------
# Dataset Paths
# -------------------------------------------------------

DATASET_PATH = os.path.join(
    os.getcwd(),
    "datasets",
    "stress",
    "processed"
)

TRAIN_FILE = os.path.join(
    DATASET_PATH,
    "clean_train.csv"
)

TEST_FILE = os.path.join(
    DATASET_PATH,
    "clean_test.csv"
)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\n========================================")
print("Loading Clean Dataset")
print("========================================\n")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

# -------------------------------------------------------
# Text Cleaning Function
# -------------------------------------------------------

def clean_text(text):

    text = str(text)

    # lowercase
    text = text.lower()

    # remove urls
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove html tags
    text = re.sub(r"<.*?>", "", text)

    # remove mentions
    text = re.sub(r"@\w+", "", text)

    # remove hashtags symbol only
    text = re.sub(r"#", "", text)

    # keep only letters, numbers and punctuation
    text = re.sub(r"[^a-zA-Z0-9.,!? ]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# -------------------------------------------------------
# Apply Cleaning
# -------------------------------------------------------

print("Cleaning Training Dataset...")

train_df["text"] = train_df["text"].apply(clean_text)

print("Cleaning Test Dataset...")

test_df["text"] = test_df["text"].apply(clean_text)

# -------------------------------------------------------
# Remove Empty Text
# -------------------------------------------------------

train_df = train_df[train_df["text"].str.len() > 0]

test_df = test_df[test_df["text"].str.len() > 0]

# -------------------------------------------------------
# Save Dataset
# -------------------------------------------------------

train_df.to_csv(
    TRAIN_FILE,
    index=False
)

test_df.to_csv(
    TEST_FILE,
    index=False
)

print("\n========================================")
print("Preprocessing Completed Successfully")
print("========================================")

print("\nTrain Samples :", len(train_df))
print("Test Samples  :", len(test_df))

print("\nExample Sentence\n")

print(train_df.iloc[0]["text"])