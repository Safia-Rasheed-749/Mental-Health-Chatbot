"""
=========================================================
Stress Detection Model
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Load DistilRoBERTa
2. Create Stress Classifier
3. Print Model Information

Author : Shamsa Akram
=========================================================
"""

import torch.nn as nn

from transformers import AutoModel


class StressClassifier(nn.Module):

    def __init__(

        self,

        num_classes=2,

        dropout=0.3

    ):

        super().__init__()

        print("\nLoading DistilRoBERTa Model...\n")

        self.transformer = AutoModel.from_pretrained(

            "distilroberta-base"

        )

        self.dropout = nn.Dropout(

            dropout

        )

        self.classifier = nn.Linear(

            self.transformer.config.hidden_size,

            num_classes

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


if __name__ == "__main__":

    print("=" * 60)
    print(" AI Mental Health Chatbot ")
    print(" Stress Detection Module ")
    print("=" * 60)

    model = StressClassifier()

    print("\n===================================")
    print("Model Loaded Successfully")
    print("===================================")

    print(model)

    total_params = sum(

        p.numel()

        for p in model.parameters()

        if p.requires_grad

    )

    print("\n===================================")
    print("Model Information")
    print("===================================")

    print("\nModel Name       : DistilRoBERTa")
    print("Hidden Size      :", model.transformer.config.hidden_size)
    print("Dropout          : 0.3")
    print("Output Classes   : 2")
    print("Trainable Params :", f"{total_params:,}")

    print("\n===================================")
    print("Model Ready For Training")
    print("===================================")