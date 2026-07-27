"""
=========================================================
Stress Detection Dataset
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load processed dataset
2. Tokenize text
3. Return PyTorch Dataset

Author : Shamsa Akram
=========================================================
"""

import os
import pandas as pd
import torch

from torch.utils.data import Dataset

from transformers import AutoTokenizer


# -------------------------------------------------------
# Dataset Class
# -------------------------------------------------------

class StressDataset(Dataset):

    def __init__(

        self,

        csv_file,

        tokenizer,

        max_length=128

    ):

        self.data = pd.read_csv(csv_file)

        self.tokenizer = tokenizer

        self.max_length = max_length

    # ---------------------------------------------

    def __len__(self):

        return len(self.data)

    # ---------------------------------------------

    def __getitem__(self, index):

        text = str(

            self.data.iloc[index]["text"]

        )

        label = int(

            self.data.iloc[index]["label"]

        )

        encoding = self.tokenizer(

            text,

            padding="max_length",

            truncation=True,

            max_length=self.max_length,

            return_tensors="pt"

        )

        return {

            "input_ids":

                encoding["input_ids"].flatten(),

            "attention_mask":

                encoding["attention_mask"].flatten(),

            "labels":

                torch.tensor(

                    label,

                    dtype=torch.long

                )

        }


# -------------------------------------------------------
# Testing
# -------------------------------------------------------

if __name__ == "__main__":

    DATASET_PATH = os.path.join(

        os.getcwd(),

        "datasets",

        "stress",

        "processed",

        "clean_train.csv"

    )

    print("\n====================================")
    print("Loading Stress Dataset")
    print("====================================\n")

    tokenizer = AutoTokenizer.from_pretrained(

        "distilroberta-base"

    )

    dataset = StressDataset(

        csv_file=DATASET_PATH,

        tokenizer=tokenizer,

        max_length=128

    )

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