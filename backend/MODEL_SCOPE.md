# MindCare AI Model Scope

## Production models

These models are used by the live FastAPI `/chat` and `/predict` routes:

- DAIR-AI RoBERTa emotion classifier
- Stress RoBERTa classifier
- Depression RoBERTa classifier

## Experimental comparison model

GoEmotions is a research/evaluation model only. It is not imported by the
frontend, `/chat`, or the production mental-state response. Its notebook and
metrics must be presented as an experimental 28-label multi-label comparison.

## Excluded model

MELD is not part of the MindCare production scope. No runtime MELD predictor
is required unless a future research phase explicitly adds conversational
emotion benchmarking.

## Terminology

The outputs are model predictions or screening signals. They are not medical
diagnoses and must not be represented as clinical risk probabilities.
