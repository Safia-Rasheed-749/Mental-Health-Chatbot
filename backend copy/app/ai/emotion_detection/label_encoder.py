"""
=========================================================
GoEmotions Label Encoder
Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Create emotion label mapping
2. Save mapping for prediction
3. Verify labels

Author : Shamsa Akram
=========================================================
"""

import os
import json


class EmotionLabelEncoder:

    def __init__(self):

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

        self.save_folder = os.path.join(
            os.getcwd(),
            "models",
            "emotion"
        )

        os.makedirs(self.save_folder, exist_ok=True)

    def show_labels(self):

        print("\n========== Emotion Labels ==========\n")

        for key, value in self.emotion_labels.items():
            print(f"{key} --> {value}")

    def save_labels(self):

        file_path = os.path.join(
            self.save_folder,
            "label_mapping.json"
        )

        with open(file_path, "w") as file:
            json.dump(self.emotion_labels, file, indent=4)

        print("\nLabel Mapping Saved Successfully!")

        print(file_path)


if __name__ == "__main__":

    encoder = EmotionLabelEncoder()

    encoder.show_labels()

    encoder.save_labels()