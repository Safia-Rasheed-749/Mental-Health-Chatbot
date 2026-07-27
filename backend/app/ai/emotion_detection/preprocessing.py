"""
=========================================================
GoEmotions Dataset Preprocessing
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load GoEmotions Dataset
2. Clean Text
3. Convert Multi-label to Single Label
4. Save Clean Dataset

Author : Shamsa Akram (FYP)
=========================================================
"""

import os
import re
import string
import pandas as pd


class GoEmotionsPreprocessor:

    def __init__(self):

        # Original Dataset Folder
        self.dataset_path = os.path.join(
            os.getcwd(),
            "datasets",
            "GoEmotions"
        )

        # Processed Dataset Folder
        self.output_path = os.path.join(
            os.getcwd(),
            "datasets",
            "processed"
        )

        os.makedirs(self.output_path, exist_ok=True)

        # Priority emotions for Mental Health Chatbot
        self.priority_labels = [
            25,  # sadness
            16,  # grief
            14,  # fear
            19,  # nervousness
            9,   # disappointment
            24,  # remorse
            2,   # anger
            11,  # disgust
            3,   # annoyance
            6,   # confusion
            20,  # optimism
            17,  # joy
            18,  # love
            15,  # gratitude
            26,  # surprise
            27   # neutral
        ]

    # ----------------------------------------------------
    # Load Dataset
    # ----------------------------------------------------
    def load_dataset(self):

        self.train = pd.read_csv(
            os.path.join(self.dataset_path, "train.tsv"),
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        self.dev = pd.read_csv(
            os.path.join(self.dataset_path, "dev.tsv"),
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        self.test = pd.read_csv(
            os.path.join(self.dataset_path, "test.tsv"),
            sep="\t",
            header=None,
            names=["text", "label", "id"]
        )

        print("Datasets Loaded Successfully.")

    # ----------------------------------------------------
    # Clean Text
    # ----------------------------------------------------
    def clean_text(self, text):

        text = str(text).lower()

        text = re.sub(r"http\S+|www\S+", "", text)

        text = re.sub(r"@\w+", "", text)

        text = re.sub(r"#", "", text)

        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        text = re.sub(r"\d+", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    # ----------------------------------------------------
    # Convert Multi Label to Single Label
    # ----------------------------------------------------
    def convert_label(self, label):

        label = str(label)

        labels = [int(x) for x in label.split(",")]

        # Select priority mental-health emotion
        for emotion in self.priority_labels:
            if emotion in labels:
                return emotion

        # Otherwise return first label
        return labels[0]

    # ----------------------------------------------------
    # Preprocess Dataset
    # ----------------------------------------------------
    def preprocess(self, dataframe):

        dataframe = dataframe.copy()

        print("Cleaning Text...")

        dataframe["text"] = dataframe["text"].apply(self.clean_text)

        print("Converting Multi-label To Single Label...")

        dataframe["label"] = dataframe["label"].apply(self.convert_label)

        print("Removing Empty Rows...")

        dataframe = dataframe[dataframe["text"] != ""]

        dataframe = dataframe.drop_duplicates()

        dataframe.reset_index(drop=True, inplace=True)

        return dataframe

    # ----------------------------------------------------
    # Save Dataset
    # ----------------------------------------------------
    def save_dataset(self):

        print("\nProcessing Train Dataset...")

        train_clean = self.preprocess(self.train)

        print("\nProcessing Dev Dataset...")

        dev_clean = self.preprocess(self.dev)

        print("\nProcessing Test Dataset...")

        test_clean = self.preprocess(self.test)

        train_clean.to_csv(
            os.path.join(self.output_path, "clean_train.csv"),
            index=False
        )

        dev_clean.to_csv(
            os.path.join(self.output_path, "clean_dev.csv"),
            index=False
        )

        test_clean.to_csv(
            os.path.join(self.output_path, "clean_test.csv"),
            index=False
        )

        print("\n===================================")
        print("Preprocessing Completed Successfully")
        print("===================================")

        print("\nFiles Saved In:")

        print(self.output_path)

        print("\nTrain Shape :", train_clean.shape)
        print("Dev Shape   :", dev_clean.shape)
        print("Test Shape  :", test_clean.shape)

        print("\nChecking Labels...")

        print("Unique Labels in Train Dataset :",
              sorted(train_clean["label"].unique()))

        print("Total Labels :",
              len(train_clean["label"].unique()))

        print("\nSample Distribution:")

        print(train_clean["label"].value_counts().sort_index())


# --------------------------------------------------------
# Main
# --------------------------------------------------------
if __name__ == "__main__":

    processor = GoEmotionsPreprocessor()

    processor.load_dataset()

    processor.save_dataset()