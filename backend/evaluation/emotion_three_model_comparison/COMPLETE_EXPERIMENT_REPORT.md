# DAIR-AI Emotion: three-model comparison

## Dataset and protocol

- Dataset: `dair-ai/emotion`; 16,000 train / 2,000 validation / 2,000 test examples.
- Six labels: sadness, joy, love, anger, fear, surprise.
- Same official splits, seed 42, sequence length 128, learning rate 2e-5, 3 configured epochs, and effective batch size 16.
- Selection rule: highest validation Macro-F1. The test set is held out for descriptive comparison only.

## Results

| Model | Validation Macro-F1 | Test accuracy | Test Macro-F1 | Test weighted F1 | Parameters | Training time |
|---|---:|---:|---:|---:|---:|---:|
| DistilBERT (`distilbert-base-uncased`) | **0.9136** | 0.9260 | 0.8820 | 0.9261 | 66.96M | 5.98 min |
| DeBERTa-v3 (`microsoft/deberta-v3-base`) | 0.9130 | **0.9355** | **0.8929** | **0.9349** | 184.43M | 15.36 min |
| RoBERTa (`roberta-base`) | 0.9118 | 0.9300 | 0.8802 | 0.9287 | 124.65M | 8.45 min |

## Selection

The selected production model is **DistilBERT**, because it has the highest validation Macro-F1 (0.9136), matching the notebook's predeclared selection rule. DeBERTa's higher test scores are reported as held-out results and were not used to choose the model.

## Methodology caveat

The notebook output reports that early stopping was disabled because the callback could not find the configured validation metric. Disclose this when presenting the comparison; do not claim early stopping was applied.

These benchmark results are not clinical validation and do not establish diagnostic performance.
