"""
============================================================
Depression Dataset Class
Project : AI Mental Health Chatbot
============================================================
"""

import os
import pandas as pd
import torch

from torch.utils.data import Dataset

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