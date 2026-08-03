"""
=========================================================
Reddit Mental Health Dataset Preprocessing
=========================================================
"""

import os
import pandas as pd

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = pd.read_csv(
    "datasets/reddit_mental_health/raw/train.csv"
)

# ----------------------------------------------------
# Keep Useful Columns
# ----------------------------------------------------

df = df[
    [
        "title",
        "body",
        "subreddit"
    ]
]

# ----------------------------------------------------
# Remove Missing Values
# ----------------------------------------------------

df = df.dropna()

# ----------------------------------------------------
# Remove Duplicate Rows
# ----------------------------------------------------

df = df.drop_duplicates()

# ----------------------------------------------------
# Clean Text
# ----------------------------------------------------

df["title"] = (
    df["title"]
    .astype(str)
    .str.lower()
    .str.strip()
)

df["body"] = (
    df["body"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# ----------------------------------------------------
# Create Output Folder
# ----------------------------------------------------

os.makedirs(
    "datasets/reddit_mental_health/processed",
    exist_ok=True
)

# ----------------------------------------------------
# Save Dataset
# ----------------------------------------------------

df.to_csv(
    "datasets/reddit_mental_health/processed/train_processed.csv",
    index=False
)

# ----------------------------------------------------
# Results
# ----------------------------------------------------

print("=" * 50)
print("Reddit Mental Health Preprocessing Completed")
print("=" * 50)

print("\nProcessed Samples :", len(df))

print("\nSaved Successfully")

print("\ndatasets/reddit_mental_health/processed/train_processed.csv")