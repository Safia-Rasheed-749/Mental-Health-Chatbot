"""
=========================================================
Reddit Mental Health Dataset Loader
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
1. Download Reddit Mental Health Dataset
2. Save dataset as CSV
3. Store in raw folder

Author : Shamsa Akram
=========================================================
"""

import os
from datasets import load_dataset

print("=" * 50)
print("Loading Reddit Mental Health Dataset")
print("=" * 50)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

dataset = load_dataset(
    "solomonk/reddit_mental_health_posts"
)

# ----------------------------------------------------
# Create Folder
# ----------------------------------------------------

save_path = os.path.join(
    "datasets",
    "reddit_mental_health",
    "raw"
)

os.makedirs(save_path, exist_ok=True)

# ----------------------------------------------------
# Convert to Pandas
# ----------------------------------------------------

train = dataset["train"].to_pandas()

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

train.to_csv(
    os.path.join(save_path, "train.csv"),
    index=False
)

# ----------------------------------------------------
# Display Information
# ----------------------------------------------------

print("\nDataset Saved Successfully\n")

print("Location:")
print(os.path.join(save_path, "train.csv"))

print("\nTotal Samples :", len(train))

print("Columns")

for column in train.columns:
    print("-", column)

print("\nCompleted Successfully")