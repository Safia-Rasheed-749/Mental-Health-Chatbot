"""
=========================================================
DistilRoBERTa Emotion Classification Model

Project : AI Mental Health Chatbot (FYP)

Purpose:
1. Load DistilRoBERTa Pretrained Model
2. Add Emotion Classification Layer
3. Ready for Fine-Tuning

Author : Shamsa Akram
=========================================================
"""

import importlib.util
from pathlib import Path

import torch
import torch.nn as nn

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

from transformers import AutoModel


class EmotionClassifier(nn.Module):

    def __init__(self, num_labels=28):

        super(EmotionClassifier, self).__init__()

        print("Loading DistilRoBERTa Model...\n")

        # Load DistilRoBERTa
        self.transformer = AutoModel.from_pretrained(
            "distilroberta-base"
        )

        # Hidden Size (768)
        hidden_size = self.transformer.config.hidden_size

        # Dropout Layer
        self.dropout = nn.Dropout(0.3)

        # Classification Layer
        self.classifier = nn.Linear(
            hidden_size,
            num_labels
        )

    def forward(self, input_ids, attention_mask):

        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # CLS Token Embedding
        cls_embedding = outputs.last_hidden_state[:, 0, :]

        # Apply Dropout
        cls_embedding = self.dropout(cls_embedding)

        # Final Classification Layer
        logits = self.classifier(cls_embedding)

        return logits


def count_parameters(model):
    """
    Count total trainable parameters
    """

    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )


if __name__ == "__main__":

    print("=" * 60)
    print(" AI Mental Health Chatbot ")
    print(" Emotion Detection Module ")
    print("=" * 60)

    # Create Model
    model = EmotionClassifier(num_labels=28)

    print("\n===================================")
    print("Model Loaded Successfully")
    print("===================================\n")

    print(model)

    print("\n===================================")
    print("Model Information")
    print("===================================\n")

    print(f"Model Name        : DistilRoBERTa")

    print(f"Hidden Size       : {model.transformer.config.hidden_size}")

    print(f"Dropout           : 0.3")

    print(f"Emotion Classes   : 28")

    print(f"Trainable Params  : {count_parameters(model):,}")

    print("\n===================================")
    print("Model Ready For Training")
    print("===================================\n")