# Recalculated held-out classifier metrics

Generated from saved predictions; no model retraining was performed.

Bootstrap intervals use row-resampling with a fixed seed and percentile 95% bounds. Confidence files contain top-class confidence only, not full probability vectors, so calibration scores are not computed.

| Model | N | Accuracy | Accuracy 95% CI | Macro-F1 | Macro-F1 95% CI |
|---|---:|---:|---|---:|---|
| depression_deberta | 1148 | 0.9791 | 0.9713–0.9869 | 0.9791 | 0.9712–0.9869 |
| stress_deberta | 715 | 0.8196 | 0.7902–0.8462 | 0.8185 | 0.7890–0.8452 |
| stress_roberta | 715 | 0.7818 | 0.7497–0.8112 | 0.7758 | 0.7427–0.8062 |

## Depression exact-overlap sensitivity check

One of 1,148 test rows exactly matched normalized train text; zero matched validation and zero duplicated another test text. Excluding that train-overlap row from archived predictions yields accuracy 0.9791 (N=1147); this is a sensitivity subset, not retraining and not validation against near-duplicate leakage.

## Stress false negatives

- `stress_deberta`: 49 positive stress examples predicted negative (label 1→0). Theme counts: `{'education_stressor': 2, 'financial_or_work_stressor': 12, 'health_or_emotional_context': 5, 'other_or_contextual': 27, 'relationship_or_family_stressor': 3}`.
- `stress_roberta`: 31 positive stress examples predicted negative (label 1→0). Theme counts: `{'education_stressor': 1, 'financial_or_work_stressor': 11, 'health_or_emotional_context': 5, 'other_or_contextual': 13, 'relationship_or_family_stressor': 1}`.

Per-class precision/recall/F1 and confusion matrices are in `HELDOUT_METRICS.json`.

Stress false-negative counts and anonymized row IDs/error themes are in the JSON; text excerpts are deliberately omitted to avoid retaining sensitive narrative.
