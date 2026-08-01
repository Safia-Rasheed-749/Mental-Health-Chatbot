"""
============================================================
AI Mental Health Chatbot
Depression Detection Module
============================================================
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

# ---------------------------------------------------------
# Depression Classifier
# ---------------------------------------------------------

class DepressionClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        self.transformer = AutoModel.from_pretrained(
            "distilroberta-base"
        )

        self.dropout = nn.Dropout(0.3)

        self.classifier = nn.Linear(
            768,
            2
        )

    def forward(
        self,
        input_ids,
        attention_mask
    ):

        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled_output = outputs.last_hidden_state[:, 0]

        pooled_output = self.dropout(
            pooled_output
        )

        logits = self.classifier(
            pooled_output
        )

        return logits


# ---------------------------------------------------------
# Test Model
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print(" AI Mental Health Chatbot ")
    print(" Depression Detection Module ")
    print("=" * 60)

    print("\nLoading DistilRoBERTa Model...\n")

    model = DepressionClassifier()

    print("\n===================================")
    print("Model Loaded Successfully")
    print("===================================\n")

    print(model)

    total_params = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print("\n===================================")
    print("Model Information")
    print("===================================\n")

    print("Model Name       : DistilRoBERTa")
    print("Hidden Size      : 768")
    print("Dropout          : 0.3")
    print("Output Classes   : 2")
    print(f"Trainable Params : {total_params:,}")

    print("\n===================================")
    print("Model Ready For Training")
    print("===================================\n")