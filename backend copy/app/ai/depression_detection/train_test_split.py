"""
============================================================
Train Validation Split
Depression Detection Module
============================================================
"""

import os
import pandas as pd

from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

INPUT_FILE = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "processed",
    "clean_dataset.csv"
)

OUTPUT_DIR = os.path.join(
    os.getcwd(),
    "datasets",
    "depression",
    "processed"
)

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

print("\nLoading Dataset...\n")

df = pd.read_csv(INPUT_FILE)

print("Total Samples :", len(df))

# ---------------------------------------------------------
# Split Dataset
# ---------------------------------------------------------

train_df, validation_df = train_test_split(

    df,

    test_size=0.20,

    random_state=42,

    stratify=df["label"]

)

# ---------------------------------------------------------
# Save Files
# ---------------------------------------------------------

train_df.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "train.csv"
    ),

    index=False

)

validation_df.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "validation.csv"
    ),

    index=False

)

# ---------------------------------------------------------
# Information
# ---------------------------------------------------------

print("\n===================================")

print("Dataset Split Completed")

print("===================================\n")

print("Training Samples   :", len(train_df))

print("Validation Samples :", len(validation_df))

print("\nFiles Saved Successfully")