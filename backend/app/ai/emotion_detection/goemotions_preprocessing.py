"""
=========================================================
GoEmotions Multi-Label Preprocessing
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load original GoEmotions TSV files
2. Clean text
3. Preserve ALL emotion labels
4. Convert labels into multi-hot format
5. Save processed datasets

IMPORTANT:
The original GoEmotions dataset is a multi-label dataset.
One text can contain multiple emotions.

This version DOES NOT convert multi-label -> single-label.

Author : Shamsa Akram
=========================================================
"""

import os
import re
import string
import pandas as pd


class GoEmotionsPreprocessor:

    def __init__(self):

        # =================================================
        # Original Dataset
        # =================================================

        self.dataset_path = os.path.join(
            os.getcwd(),
            "datasets",
            "GoEmotions"
        )

        # =================================================
        # New Processed Dataset
        # =================================================

        self.output_path = os.path.join(
            os.getcwd(),
            "datasets",
            "processed_goemotions_multilabel"
        )

        os.makedirs(
            self.output_path,
            exist_ok=True
        )

        # =================================================
        # GoEmotions Labels
        # =================================================

        self.emotion_labels = {

            0: "admiration",
            1: "amusement",
            2: "anger",
            3: "annoyance",
            4: "approval",
            5: "caring",
            6: "confusion",
            7: "curiosity",
            8: "desire",
            9: "disappointment",
            10: "disapproval",
            11: "disgust",
            12: "embarrassment",
            13: "excitement",
            14: "fear",
            15: "gratitude",
            16: "grief",
            17: "joy",
            18: "love",
            19: "nervousness",
            20: "optimism",
            21: "pride",
            22: "realization",
            23: "relief",
            24: "remorse",
            25: "sadness",
            26: "surprise",
            27: "neutral"
        }

        self.num_labels = len(
            self.emotion_labels
        )

    # =====================================================
    # Load Dataset
    # =====================================================

    def load_dataset(self):

        print("\n===================================")
        print("Loading GoEmotions Dataset")
        print("===================================\n")

        self.train = pd.read_csv(
            os.path.join(
                self.dataset_path,
                "train.tsv"
            ),
            sep="\t",
            header=None,
            names=[
                "text",
                "label",
                "id"
            ]
        )

        self.dev = pd.read_csv(
            os.path.join(
                self.dataset_path,
                "dev.tsv"
            ),
            sep="\t",
            header=None,
            names=[
                "text",
                "label",
                "id"
            ]
        )

        self.test = pd.read_csv(
            os.path.join(
                self.dataset_path,
                "test.tsv"
            ),
            sep="\t",
            header=None,
            names=[
                "text",
                "label",
                "id"
            ]
        )

        print(
            "Training samples   :",
            len(self.train)
        )

        print(
            "Validation samples :",
            len(self.dev)
        )

        print(
            "Test samples       :",
            len(self.test)
        )

    # =====================================================
    # Clean Text
    # =====================================================

    def clean_text(self, text):

        text = str(text)

        # Lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(
            r"http\S+|www\S+",
            "",
            text
        )

        # Remove mentions
        text = re.sub(
            r"@\w+",
            "",
            text
        )

        # Remove hashtag symbol
        text = re.sub(
            r"#",
            "",
            text
        )

        # IMPORTANT:
        # Keep punctuation because punctuation can carry
        # emotional information.

        # Remove extra whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text

    # =====================================================
    # Convert Labels To Multi-Hot Vector
    # =====================================================

    def convert_labels(self, label_string):

        label_string = str(label_string)

        labels = [
            int(x)
            for x in label_string.split(",")
            if x.strip() != ""
        ]

        multi_hot = [
            0
            for _ in range(self.num_labels)
        ]

        for label in labels:

            if 0 <= label < self.num_labels:

                multi_hot[label] = 1

        return multi_hot

    # =====================================================
    # Preprocess Dataset
    # =====================================================

    def preprocess(self, dataframe):

        dataframe = dataframe.copy()

        print(
            "\nCleaning text..."
        )

        dataframe["text"] = (
            dataframe["text"]
            .apply(self.clean_text)
        )

        # Remove empty text
        dataframe = dataframe[
            dataframe["text"].str.len() > 0
        ]

        # Remove duplicate text
        dataframe = dataframe.drop_duplicates(
            subset=["text"]
        )

        print(
            "Converting labels to multi-label format..."
        )

        dataframe["labels"] = (
            dataframe["label"]
            .apply(self.convert_labels)
        )

        # Keep only required columns
        dataframe = dataframe[
            [
                "text",
                "labels"
            ]
        ]

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        return dataframe

    # =====================================================
    # Save Dataset
    # =====================================================

    def save_dataset(self):

        print(
            "\n==================================="
        )
        print(
            "Processing Training Dataset"
        )
        print(
            "==================================="
        )

        train_clean = self.preprocess(
            self.train
        )

        print(
            "\n==================================="
        )
        print(
            "Processing Validation Dataset"
        )
        print(
            "==================================="
        )

        dev_clean = self.preprocess(
            self.dev
        )

        print(
            "\n==================================="
        )
        print(
            "Processing Test Dataset"
        )
        print(
            "==================================="
        )

        test_clean = self.preprocess(
            self.test
        )

        # =================================================
        # Save
        # =================================================

        train_file = os.path.join(
            self.output_path,
            "clean_train.csv"
        )

        dev_file = os.path.join(
            self.output_path,
            "clean_dev.csv"
        )

        test_file = os.path.join(
            self.output_path,
            "clean_test.csv"
        )

        train_clean.to_csv(
            train_file,
            index=False
        )

        dev_clean.to_csv(
            dev_file,
            index=False
        )

        test_clean.to_csv(
            test_file,
            index=False
        )

        # =================================================
        # Save Label Mapping
        # =================================================

        mapping_file = os.path.join(
            self.output_path,
            "label_mapping.json"
        )

        import json

        with open(
            mapping_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.emotion_labels,
                file,
                indent=4
            )

        # =================================================
        # Print Summary
        # =================================================

        print(
            "\n==================================="
        )
        print(
            "Preprocessing Completed Successfully"
        )
        print(
            "===================================\n"
        )

        print(
            "Output folder:"
        )

        print(
            self.output_path
        )

        print(
            "\nTrain samples      :",
            len(train_clean)
        )

        print(
            "Validation samples:",
            len(dev_clean)
        )

        print(
            "Test samples      :",
            len(test_clean)
        )

        print(
            "\nNumber of emotions:",
            self.num_labels
        )

        print(
            "\nSaved files:"
        )

        print(
            "- clean_train.csv"
        )

        print(
            "- clean_dev.csv"
        )

        print(
            "- clean_test.csv"
        )

        print(
            "- label_mapping.json"
        )


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    processor = GoEmotionsPreprocessor()

    processor.load_dataset()

    processor.save_dataset()