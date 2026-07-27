"""
=========================================================
PyTorch Dataset Class

Project : AI Mental Health Chatbot

Dataset : GoEmotions

Purpose
-------
1. Load Clean Dataset
2. Tokenize Text
3. Return PyTorch Tensors

Author : Shamsa Akram
=========================================================
"""

import os
import pandas as pd
import torch

from torch.utils.data import Dataset
from transformers import AutoTokenizer


class GoEmotionsDataset(Dataset):

    def __init__(self, file_path, max_length=128):

        print(f"\nLoading Dataset : {file_path}")

        self.data = pd.read_csv(file_path)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilroberta-base"
        )

        self.max_length = max_length

        print("Dataset Loaded Successfully")
        print("Total Samples :", len(self.data))

    def __len__(self):

        return len(self.data)

    def __getitem__(self, index):

        text = str(self.data.iloc[index]["text"])

        label = int(self.data.iloc[index]["label"])

        encoding = self.tokenizer(

            text,

            padding="max_length",

            truncation=True,

            max_length=self.max_length,

            return_tensors="pt"

        )

        return {

            "input_ids": encoding["input_ids"].squeeze(0),

            "attention_mask": encoding["attention_mask"].squeeze(0),

            "labels": torch.tensor(label, dtype=torch.long)

        }


if __name__ == "__main__":

    dataset_path = os.path.join(

        os.getcwd(),

        "datasets",

        "processed",

        "clean_train.csv"

    )

    dataset = GoEmotionsDataset(dataset_path)

    print("\n====================================")

    print("Dataset Information")

    print("====================================")

    print("Total Samples :", len(dataset))

    sample = dataset[0]

    print("\nKeys")

    print(sample.keys())

    print("\nInput Shape")

    print(sample["input_ids"].shape)

    print("\nAttention Mask Shape")

    print(sample["attention_mask"].shape)

    print("\nLabel")

    print(sample["labels"])