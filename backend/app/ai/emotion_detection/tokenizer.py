"""
=========================================================
GoEmotions Tokenizer
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load cleaned dataset
2. Load RoBERTa Tokenizer
3. Convert text into tokens
4. Save tokenized dataset

Author : Shamsa Akram
=========================================================
"""

import importlib.util
import os
from pathlib import Path

import pandas as pd
import torch

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


class EmotionTokenizer:

    def __init__(self):

        self.dataset_path = os.path.join(
            os.getcwd(),
            "datasets",
            "processed"
        )

        self.output_path = os.path.join(
            os.getcwd(),
            "datasets",
            "tokenized"
        )

        os.makedirs(self.output_path, exist_ok=True)

        print("Loading RoBERTa Tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

    ######################################################

    def load_dataset(self):

        self.train = pd.read_csv(
            os.path.join(self.dataset_path, "clean_train.csv")
        )

        self.dev = pd.read_csv(
            os.path.join(self.dataset_path, "clean_dev.csv")
        )

        self.test = pd.read_csv(
            os.path.join(self.dataset_path, "clean_test.csv")
        )

        print("Datasets Loaded Successfully.")

    ######################################################

    def tokenize(self, dataframe):

        tokens = self.tokenizer(

            dataframe["text"].tolist(),

            padding=True,

            truncation=True,

            max_length=128,

            return_tensors="pt"

        )

        labels = torch.tensor(
            dataframe["label"].tolist()
        )

        return tokens, labels

    ######################################################

    def save_tokens(self):

        print("\nTokenizing Train Dataset...")

        train_tokens, train_labels = self.tokenize(self.train)

        print("Tokenizing Dev Dataset...")

        dev_tokens, dev_labels = self.tokenize(self.dev)

        print("Tokenizing Test Dataset...")

        test_tokens, test_labels = self.tokenize(self.test)

        torch.save(

            {

                "tokens": train_tokens,

                "labels": train_labels

            },

            os.path.join(
                self.output_path,
                "train_tokens.pt"
            )

        )

        torch.save(

            {

                "tokens": dev_tokens,

                "labels": dev_labels

            },

            os.path.join(
                self.output_path,
                "dev_tokens.pt"
            )

        )

        torch.save(

            {

                "tokens": test_tokens,

                "labels": test_labels

            },

            os.path.join(
                self.output_path,
                "test_tokens.pt"
            )

        )

        print("\n===================================")
        print("Tokenization Completed Successfully")
        print("===================================")

        print("\nSaved In")

        print(self.output_path)

        print("\nTrain Samples :", len(train_labels))
        print("Dev Samples   :", len(dev_labels))
        print("Test Samples  :", len(test_labels))


if __name__ == "__main__":

    tokenizer = EmotionTokenizer()

    tokenizer.load_dataset()

    tokenizer.save_tokens()