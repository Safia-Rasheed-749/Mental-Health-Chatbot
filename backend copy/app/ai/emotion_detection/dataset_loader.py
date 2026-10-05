"""
=========================================================
GoEmotions Dataset Loader
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load GoEmotions Dataset
2. Display Dataset Information
3. Verify dataset is loaded correctly

Author : Shamsa Akram (FYP)
=========================================================
"""

import os
import pandas as pd


class GoEmotionsDatasetLoader:

    def __init__(self):

        # Dataset Folder
        self.dataset_path = os.path.join(
            os.getcwd(),
            "datasets",
            "GoEmotions"
        )

        self.train_data = None
        self.dev_data = None
        self.test_data = None

    def load_dataset(self):
        """
        Load Train, Dev and Test datasets
        """

        train_file = os.path.join(self.dataset_path, "train.tsv")
        dev_file = os.path.join(self.dataset_path, "dev.tsv")
        test_file = os.path.join(self.dataset_path, "test.tsv")

        # Load TSV files (Official GoEmotions format)
        self.train_data = pd.read_csv(
            train_file,
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        self.dev_data = pd.read_csv(
            dev_file,
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        self.test_data = pd.read_csv(
            test_file,
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        print("\n====================================")
        print(" GoEmotions Dataset Loaded Successfully ")
        print("====================================\n")

    def show_dataset_info(self):

        print("========== TRAIN DATA ==========")
        print(f"Rows    : {self.train_data.shape[0]}")
        print(f"Columns : {self.train_data.shape[1]}")

        print("\nColumn Names:")
        print(self.train_data.columns.tolist())

        print("\nFirst Five Rows:")
        print(self.train_data.head())

        print("\n----------------------------------------")

        print("\n========== DEV DATA ==========")
        print(f"Rows    : {self.dev_data.shape[0]}")
        print(f"Columns : {self.dev_data.shape[1]}")

        print("\nFirst Five Rows:")
        print(self.dev_data.head())

        print("\n----------------------------------------")

        print("\n========== TEST DATA ==========")
        print(f"Rows    : {self.test_data.shape[0]}")
        print(f"Columns : {self.test_data.shape[1]}")

        print("\nFirst Five Rows:")
        print(self.test_data.head())

    def check_missing_values(self):

        print("\n===================================")
        print(" Missing Values (Train Dataset)")
        print("===================================\n")

        print(self.train_data.isnull().sum())

    def check_duplicate_rows(self):

        print("\n===================================")
        print(" Duplicate Rows (Train Dataset)")
        print("===================================\n")

        duplicates = self.train_data.duplicated().sum()

        print("Duplicate Rows :", duplicates)

    def dataset_summary(self):

        print("\n===================================")
        print(" Dataset Summary ")
        print("===================================\n")

        print("Train Shape :", self.train_data.shape)
        print("Dev Shape   :", self.dev_data.shape)
        print("Test Shape  :", self.test_data.shape)

        print("\nUnique Labels in Train Dataset:")

        print(sorted(self.train_data["label"].unique()))

        print("\nTotal Unique Labels :",
              self.train_data["label"].nunique())


if __name__ == "__main__":

    loader = GoEmotionsDatasetLoader()

    loader.load_dataset()

    loader.show_dataset_info()

    loader.check_missing_values()

    loader.check_duplicate_rows()

    loader.dataset_summary()

    print("\nDataset Loader Executed Successfully!")