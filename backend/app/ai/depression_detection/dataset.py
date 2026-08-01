"""
============================================================
Depression Dataset Class
Project : AI Mental Health Chatbot
============================================================
"""

import importlib.util
import os
from pathlib import Path

import pandas as pd
import torch

from torch.utils.data import Dataset

# =====================================================
# Hugging Face Cache (Cross Platform)
# Centralized in app/ai/hf_cache.py
# Loaded by absolute file path so sys.path is never
# modified and installed packages are never shadowed.
# Must run before importing any Hugging Face library.
# =====================================================

HF_CACHE_PATH = Path(__file__).resolve().parents[1] / "hf_cache.py"

_hf_cache_spec = importlib.util.spec_from_file_location(
    "hf_cache", HF_CACHE_PATH
)
_hf_cache_module = importlib.util.module_from_spec(_hf_cache_spec)
_hf_cache_spec.loader.exec_module(_hf_cache_module)

from transformers import AutoTokenizer

# ---------------------------------------------------------
# Dataset Class
# ---------------------------------------------------------

class DepressionDataset(Dataset):

    def __init__(self, csv_file):

        self.data = pd.read_csv(csv_file)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilroberta-base"
        )

        self.max_length = 128

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        text = str(self.data.iloc[idx]["text"])

        label = int(self.data.iloc[idx]["label"])

        encoding = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )

        return {

            "input_ids": encoding["input_ids"].squeeze(),

            "attention_mask": encoding["attention_mask"].squeeze(),

            "labels": torch.tensor(label, dtype=torch.long)
        }


# ---------------------------------------------------------
# Test Dataset
# ---------------------------------------------------------

if __name__ == "__main__":

    DATA_PATH = os.path.join(
        os.getcwd(),
        "datasets",
        "depression",
        "processed",
        "clean_dataset.csv"
    )

    print("\n====================================")
    print("Loading Depression Dataset")
    print("====================================\n")

    dataset = DepressionDataset(DATA_PATH)

    print("Dataset Loaded Successfully")

    print("Total Samples :", len(dataset))

    sample = dataset[0]

    print("\n====================================")
    print("Dataset Information")
    print("====================================")

    print("\nKeys")

    print(sample.keys())

    print("\nInput Shape")

    print(sample["input_ids"].shape)

    print("\nAttention Mask Shape")

    print(sample["attention_mask"].shape)

    print("\nLabel")

    print(sample["labels"])