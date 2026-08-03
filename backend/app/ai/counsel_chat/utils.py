"""
=========================================================
Counsel Chat Utility Functions
Project : AI Mental Health Chatbot (FYP)

Purpose
-------
Reusable helper functions for:
1. Text cleaning
2. Text formatting
3. Question preprocessing
4. Answer preprocessing
=========================================================
"""

import re


def clean_text(text):
    """
    Clean input text.
    """

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


def clean_question(question):
    return clean_text(question)


def clean_answer(answer):
    return clean_text(answer)


if __name__ == "__main__":

    sample = "  I Feel VERY Anxious!!! Visit https://example.com "

    print("Original")

    print(sample)

    print()

    print("Cleaned")

    print(clean_text(sample))