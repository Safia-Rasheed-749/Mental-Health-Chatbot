# Depression dataset: three-model comparison (evidence archive)

Source: `MindCare_AI_Depression_3_Model_Comparison.ipynb` run on Google Colab,
train/validation/test CSV splits from `backend/datasets/depression_v2/processed/`.

- Task: binary text classification (`0 = No Depression`, `1 = Depression`).
- Selection rule: highest **validation Macro-F1**; the test split was not used for selection.
- Selected production model: **roberta-base** (validation Macro-F1 0.9826),
  exported to `backend/models/depression_production_model/`.

Test results (descriptive, held-out):

| model | test accuracy | test macro-F1 |
|---|---:|---:|
| roberta-base | 0.9817 | 0.9817 |
| microsoft/deberta-v3-base | 0.9791 | 0.9791 |
| distilbert-base-uncased | 0.9808 | 0.9808 |

## File provenance

The downloaded copies of these files arrived with rotated/mismatched names
(`... (1).csv` duplicate-download suffixes). Every file kept here was
re-identified by its content and renamed to its true name.

Derived files (reconstructed deterministically from other kept artifacts;
the method was round-trip validated against the model whose original file
was available):
- `results/deberta_v3_base_test_confusion_matrix.csv (derived from its classification report)`
- `results/distilbert_base_test_classification_report.csv (derived from its confusion matrix)`

Recreated file (was missing from the download; values taken from the comparison table):
- `selected_model.json`

Not present in the downloaded evidence (re-download from Google Drive if needed):
- `results/roberta_base_test_predictions.csv`
- `results/distilbert_base_test_predictions.csv`

## Interpretation notice

These are dataset benchmark results, not clinical validation. The classifier
does not diagnose depression or estimate suicide risk.
