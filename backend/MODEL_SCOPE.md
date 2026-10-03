# MindCare AI Model Scope

## Production models

These models are used by the live FastAPI `/chat` and `/predict` routes:

- DAIR-AI RoBERTa emotion classifier
- Stress RoBERTa classifier
- Depression RoBERTa classifier

## Emotion model selection

DAIR-AI RoBERTa is the retained emotion classifier. The MELD and GoEmotions
experiments and their associated assets have been removed from this project at
the user's request.

## Depression model selection

The three-model Colab comparison (RoBERTa, DistilBERT, DeBERTa-v3) selected
RoBERTa by validation Macro-F1; its exported artifact under
`backend/models/depression_production_model/` is the retained depression
classifier. The earlier `depression_v2` local checkpoints and evaluation
outputs, the legacy V1 training scripts, and the superseded evaluation folder
have been removed from this project at the user's request. The prepared
`backend/datasets/depression_v2/processed/` splits and the comparison
evidence under `backend/evaluation/depression_three_model_comparison/` are
retained.

## Terminology

The outputs are model predictions or screening signals. They are not medical
diagnoses and must not be represented as clinical risk probabilities.
