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

## Terminology

The outputs are model predictions or screening signals. They are not medical
diagnoses and must not be represented as clinical risk probabilities.
