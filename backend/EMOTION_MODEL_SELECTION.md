# Emotion model selection

## Comparison result and production target

The three-model comparison notebook is `notebooks/MindCare_AI_DAIR_AI_Emotion_3_Model_Complete_Colab.ipynb`. Following its stated selection rule (highest validation Macro-F1), its selected production model is fine-tuned **DistilBERT** (`distilbert-base-uncased`), with validation Macro-F1 **0.9136**. Its test-set results are 92.60% accuracy and 0.8820 Macro-F1. DeBERTa has higher test metrics, but the notebook reserves the test set for final descriptive reporting rather than model selection.

The exported DistilBERT production artifact is now in `models/emotion_dair_ai_production_model/`. The backend predictor loads that folder. The older separately trained RoBERTa emotion model is not part of the selected production model.

The notebook's comparison is suitable for presenting the three models because they share the same DAIR-AI dataset and train/validation/test splits. The notebook logs that early stopping was disabled because its callback could not find the expected validation metric; disclose this caveat when presenting the methodology.

## Files and datasets

- Keep the comparison notebook and the generated comparison report, selected-model metadata, per-model metrics/classification reports, and charts under `evaluation/emotion_three_model_comparison/` for the panel.
- The production model folder should contain `config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`, `vocab.txt`, and `label_mapping.json` (plus the notebook's production metadata if available). Do not put all three model weight sets in the production folder.
- Keep only `models/emotion_dair_ai_production_model/` for the deployed DAIR-AI emotion model; the three-model comparison notebook contains the training and comparison code for reproducibility.
- Keep all source datasets under `datasets/` unchanged.
- MELD, GoEmotions, and superseded single-model RoBERTa emotion artifacts were removed. The DAIR-AI dataset and selected DistilBERT production model are retained.
