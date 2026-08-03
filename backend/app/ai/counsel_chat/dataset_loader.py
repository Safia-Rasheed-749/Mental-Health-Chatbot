"""
=========================================================
Counsel Chat Dataset Loader
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
1. Download Counsel Chat Dataset
2. Save it into CSV
3. Store in datasets/counsel_chat/raw

Author : Shamsa Akram
=========================================================
"""

from datasets import load_dataset
import pandas as pd
import os

# Load dataset
dataset = load_dataset("nbertagnolli/counsel-chat")

train = dataset["train"].to_pandas()

# Create folders
os.makedirs("datasets/counsel_chat/raw", exist_ok=True)

# Save CSV
train.to_csv(
    "datasets/counsel_chat/raw/train.csv",
    index=False
)

print("=" * 50)
print("Counsel Chat Dataset Saved Successfully")
print("=" * 50)

print("\nFiles Created:")
print("train.csv")

print("\nTotal Samples:", len(train))