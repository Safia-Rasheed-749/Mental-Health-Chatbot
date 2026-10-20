# Classifier reproducibility and validity notes

Generated from repository artifacts and training code inspection. This is documentation, not a claim that models were retrained.

| Task/artifact | Evidence currently available | Reproducible command / limitation |
|---|---|---|
| Emotion DAIR-AI | `backend/evaluation/emotion_three_model_comparison/COMPLETE_EXPERIMENT_REPORT.md` states official 16k/2k/2k splits, seed 42, max length 128, LR 2e-5, 3 epochs, effective batch 16, validation Macro-F1 selection. Notebook is `backend/notebooks/MindCare_AI_DAIR_AI_Emotion_3_Model_Complete_Colab (4).ipynb`. | Notebook is Colab-oriented; no standalone pinned training invocation and no held-out per-row prediction CSV retained. Retraining/per-class recomputation not established. |
| Depression | `backend/evaluation/depression_three_model_comparison/README.md` and notebook record validation Macro-F1 model selection; notebook config records seed 42, max length 128, LR 2e-5, 3 epochs, per-device batch 8, gradient accumulation 2, eval batch 32, weight decay 0.01. Saved DeBERTa held-out predictions are available. | Notebook uses Colab/Drive paths. Active local model path is declared in `backend/app/ai/depression_detection/predict.py` but model files and training script are absent. No honest local retraining command is available. Archived predictions can be recalculated only. |
| Stress | `backend/app/ai/stress_detection/train.py`: `roberta-base`, max length 128, 5 epochs, LR 2e-5, batch 8, weight decay .01, seed/data seed 42, stratified 10% validation subset from train only, latest-checkpoint resume. The held-out `clean_test.csv` is no longer used for model selection. Archived three-model evidence/predictions remain historical and do not reflect an execution of the corrected script. | From `backend`: `$env:STRESS_MODEL_OUTPUT_DIR='models/stress_roberta_repro_v1'; python -m app.ai.stress_detection.train`. Paths are anchored to the script. A fresh output path avoids resuming/overwriting existing artifacts. No training was run in this remediation. |

Package versions: see `VALIDATION/baseline/pip-freeze.txt` (environment capture; not proof those exact versions were used for historical Colab training). Model hashes are in `VALIDATION/baseline/MODEL_HASHES.json` only for artifacts present at capture; missing model files cannot be hashed.

To rerun available archived-prediction calculations:

```powershell
python backend/scripts/analyze_classifier_predictions.py --replicates 5000
```

To rerun split audit (exact normalized equality is exhaustive; near-duplicate comparison uses normalized character 3–5 gram Jaccard over bottom-32 MinHash-LSH candidates, so candidate-generation recall is approximate; any cap and skipped ranges are emitted):

```powershell
python backend/scripts/audit_datasets.py --roots backend/datasets/depression_v2 backend/datasets/stress counsel_chat/emotion_dataset --output VALIDATION/datasets/classifier_splits --pair-cap 500000
```

No original datasets or model artifacts are changed by these commands. Unknown dataset licenses remain unverified; no redistribution/deployment permission is inferred.
