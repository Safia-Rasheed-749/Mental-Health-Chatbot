# Depression Dataset and Model — Project Reference

This document records the depression-related data and model pipeline found in this repository. It distinguishes checked-in artifacts from assumptions: where the repository does not establish a detail (for example, exact source provenance for the V2 CSVs), that limitation is stated rather than guessed.

## 1. At a glance

- **Primary/live task:** binary text classification, `No Depression` (label `0`) vs `Depression` (label `1`).
- **Primary model:** `roberta-base` fine-tuned for sequence classification, selected from a three-model comparison (RoBERTa, DistilBERT, DeBERTa-v3) by validation Macro-F1.
- **Current V2 split:** 5,355 training, 1,147 validation, and 1,148 test examples (7,650 total, as documented by the V2 training/evaluation assets).
- **Current dataset files:** `backend/datasets/depression_v2/processed/{train.csv,validation.csv,test.csv}`.
- **Model artifacts:** `backend/models/depression_production_model/` (directory is loaded by the runtime predictor).
- **Comparison evidence:** `backend/evaluation/depression_three_model_comparison/` (reports, per-model results, plots, and a provenance README).
- **Reported held-out test result (selected model):** 98.17% accuracy (1,127 / 1,148) and Macro-F1 98.17%. This is a dataset-specific result, not evidence of clinical or real-world diagnostic accuracy.
- **Important:** this is a text signal from social/user-written text, not a diagnosis, validated screening instrument, or clinical risk estimate.

## 2. Which depression data is in the repository?

There are two dataset generations. Do not mix their paths, pipelines, splits, or results.

### V2 — current training/evaluation pipeline

| Split | Path | Rows stated in project artifacts | Purpose |
|---|---|---:|---|
| Train | `backend/datasets/depression_v2/processed/train.csv` | 5,355 | Fine-tuning |
| Validation | `backend/datasets/depression_v2/processed/validation.csv` | 1,147 | Per-epoch evaluation / model selection |
| Test | `backend/datasets/depression_v2/processed/test.csv` | 1,148 | Final held-out evaluation only |

The training and evaluation code expects columns named `text` and `label`. Labels are `0 = No Depression`, `1 = Depression`. The CSV split files exist locally. The source/raw V2 data and a reproducible V2 cleaning/splitting script were not found in the inspected dataset paths; therefore the provenance, exact cleaning history, and split-generation method for V2 cannot be fully verified from this repository alone. Do not claim those details without checking their original source or experiment records.

### V1 — legacy pipeline (removed from `backend/`, archived in `backend copy/`)

- Expected raw input (raw folder is ignored/not present in the checked-in workspace): `backend/datasets/depression/raw/depression_dataset_reddit_cleaned.csv`.
- Legacy processed data (`clean_dataset.csv`, `clean_dataset_backup.csv`, `train.csv`, `validation.csv`) was removed from `backend/datasets/depression/` at the user's request; an archived copy remains under `backend copy/datasets/depression/processed/`.
- The legacy loader selected `clean_text` and `is_depression`, renamed them to `text` and `label`, dropped duplicate rows, then dropped missing rows.
- The legacy split script created an 80/20 train/validation split using `random_state=42` and stratification on `label`; it did not make a test split.
- The legacy `preprocessing.py` lowercased text, attempted to remove URLs, removed non-ASCII letters, and collapsed whitespace. It read and wrote the same `clean_dataset.csv` path, so running it overwrote that file. It was **not** the V2 preparation pipeline.
- The V1 scripts (`dataset_loader.py`, `preprocessing.py`, `train_test_split.py`) were removed from `backend/app/ai/depression_detection/` at the user's request; only their behavior, as previously recorded here, remains. Because the raw input is not in the checkout, V1 cannot be reproduced from this repository alone.

## 3. Provenance and interpretation

The legacy filename and text suggest Reddit-origin material, and the evaluation artifacts show informal, Reddit-like post excerpts. However, the checked repository does not document a verifiable V2 dataset citation, license, collection date, Reddit communities, sampling method, annotation protocol, or the exact relationship between V1 and V2. Treat those as **unknown pending provenance confirmation**, not established facts.

Labels are dataset labels, not diagnoses assigned by this model. A post can discuss depression without its author having a diagnosis; a post can be labeled "No Depression" while containing distress, and a classifier can miss context, sarcasm, negation, or risk. The negative class also does not mean "healthy."

## 4. Cleaning, preprocessing, and tokenization

### V1 scripts (historical)

The removed V1 loader produced `clean_dataset.csv` from the raw file; the removed `preprocessing.py` performed text normalization, but its regex source used doubled backslashes (for example `r"http\\S+"`), which may not have behaved as intended for URL/whitespace matching, and it overwrote its input. Do not describe legacy V1 cleaning as V2 cleaning.

### Current V2 pipeline (Colab notebook)

The comparison notebook `backend/notebooks/MindCare_AI_Depression_3_Model_Comparison.ipynb` loads the pre-existing V2 train and validation CSVs directly (pandas), checks that labels are exactly `[0, 1]`, and never loads test rows into training. Each text is encoded by the corresponding base model's tokenizer with truncation and `max_length=128`. The notebook does **not** itself lowercase, strip HTML/URLs, deduplicate, drop missing rows, or create the CSV splits. The runtime predictor likewise applies only `.strip()` to input before tokenizer encoding.

Thus the V2 CSVs are called "processed," but their upstream transformations are not recoverable from the available scripts.

## 5. Training details

Source: the notebook above and the archived `experiment_config.json` in the comparison evidence folder.

### Current protocol (three-model comparison)

- Models: `roberta-base`, `distilbert-base-uncased`, `microsoft/deberta-v3-base`.
- Random seed: `42`. Maximum token length: `128`.
- Epochs: `3`. Learning rate: `2e-5`.
- Per-device train batch size `8` with gradient accumulation `2` (effective batch `16`); evaluation batch size `32`.
- Weight decay `0.01`; warmup ratio `0.1`.
- Selection rule: **highest validation Macro-F1** (`eval_macro_f1`); the test split was not used for selection.
- All three models trained with the Hugging Face `Trainer` (fp16 on a Colab GPU).
- Selected model: **`roberta-base`** (validation Macro-F1 0.9826), exported with tokenizer, label mapping, training args, and metadata to `backend/models/depression_production_model/`.

### Historical local V2 run (artifacts removed)

An earlier local script (`backend/app/ai/depression_detection/train.py`, removed at the user's request) fine-tuned `roberta-base` with seed `42`, `4` epochs, learning rate `2e-5`, per-device batch `4`, gradient accumulation `1`, evaluation each epoch, keeping up to two checkpoints and reloading the best model by validation accuracy, writing output to `backend/models/depression_v2/`. That run reported 98.00% test accuracy; its checkpoints, logs, and evaluation outputs have been removed from this project, so the number is historical only and is superseded by the comparison results below.

## 6. Evaluation and reported performance

Evidence: `backend/evaluation/depression_three_model_comparison/` — see its `README.md` for file provenance (the downloaded files arrived with rotated/mismatched names and were re-identified by content; two files were derived by a round-trip-validated method; two row-level prediction files were not part of the download).

Selection was on validation Macro-F1; test columns are descriptive/held-out:

| model | validation Macro-F1 | test accuracy | test Macro-F1 |
|---|---:|---:|---:|
| **roberta-base (selected)** | 0.9826 | 98.17% | 0.9817 |
| microsoft/deberta-v3-base | 0.9808 | 97.91% | 0.9791 |
| distilbert-base-uncased | 0.9756 | 98.08% | 0.9808 |

Selected model (RoBERTa) on the 1,148-example test split:

| Metric | Reported value |
|---|---:|
| Accuracy | 98.17% (1,127 correct / 21 incorrect) |
| Macro precision | 98.18% |
| Macro recall | 98.16% |
| Macro F1 | 98.17% |
| Weighted F1 | 98.17% |

Confusion matrix (rows actual, columns predicted; order `No Depression`, `Depression`): `[[576, 8], [13, 551]]`. Test class counts: 584 `No Depression`, 564 `Depression`.

Retained files:

- Top level: `COMPLETE_EXPERIMENT_REPORT.md`, `three_model_comparison.csv`, `experiment_config.json`, `all_training_summaries.json`, `dataset_class_distribution.csv`, `selected_model.json`, `selected_model_error_summary.csv`, `depression_three_model_comparison.xlsx`, `README.md`.
- `results/` — per model: `*_training_history.csv`, `*_training_summary.json`, `*_test_metrics.json`, `*_test_classification_report.csv`, `*_test_confusion_matrix.csv`; plus `deberta_v3_base_test_predictions.csv`.
- `plots/` — comparison plots (test accuracy, test Macro-F1, test weighted F1, training time) and the selected model's test confusion matrix.

The numbers above are transcribed from saved project artifacts, not independently recomputed here. The ~98% result should be investigated for duplicates or near-duplicates crossing splits, source/subreddit or annotation artifacts, leakage, and calibration. A single random held-out test set does not establish external validity. Include class-level metrics and uncertainty intervals in formal reporting where possible.

## 7. Runtime usage

Production scope lists the Depression RoBERTa classifier as active (`backend/MODEL_SCOPE.md`). Runtime implementation: `backend/app/ai/depression_detection/predict.py`.

It loads model and tokenizer locally from `backend/models/depression_production_model/`, tokenizes at max length 128, computes softmax probabilities, and returns:

```json
{"depression": "Depression", "label": 1, "confidence": 98.7}
```

`confidence` is the maximum softmax probability expressed as a percentage. It is not calibrated clinical confidence or a probability that a person has a disorder. The predictor is called from chat services; user-facing product language should say "model prediction/signal," never diagnosis. The model can fail on short, out-of-domain, multilingual, or context-dependent messages.

## 8. Useful related files

| File/folder | Role |
|---|---|
| `backend/app/ai/depression_detection/predict.py` | Runtime inference (loads the production model) |
| `backend/app/ai/depression_detection/model.py` | Legacy classifier definition; not used by the runtime predictor |
| `backend/datasets/depression_v2/processed/` | Current V2 CSV splits |
| `backend copy/datasets/depression/processed/` | Archived legacy V1 processed files |
| `backend/models/depression_production_model/` | Production model, tokenizer, label mapping, metadata |
| `backend/evaluation/depression_three_model_comparison/` | Three-model comparison evidence: reports, results, plots |
| `backend/notebooks/MindCare_AI_Depression_3_Model_Comparison.ipynb` | Colab training/comparison notebook |
| `backend/MODEL_SCOPE.md` | Production vs experimental model scope |

Removed at the user's request (no longer in `backend/`): the `backend/models/depression_v2/` checkpoints, `backend/evaluation/depression_v2/` outputs and `evaluate_depression_v2.py`, `backend/notebooks/04_depression_detection_v2.ipynb`, the local `train.py` and V1 legacy scripts, `backend/check_depression_dataset.py`, and the V1 `backend/datasets/depression/` processed files. Copies of the legacy scripts and V1 data remain under `backend copy/`, and removed folders may also still be recoverable from the Recycle Bin.

## 9. Reproduction outline

1. Open `backend/notebooks/MindCare_AI_Depression_3_Model_Comparison.ipynb` in Google Colab with a GPU runtime.
2. Make the three V2 CSVs available (upload them, or place them in a mounted Google Drive folder); the notebook prompts for any missing file.
3. Run all cells: the three models are trained with the recorded configuration, evaluated, compared, and the selected model (validation Macro-F1 winner) is exported as `production_model/`.
4. Copy the exported production folder to `backend/models/depression_production_model/` for local runtime use.
5. Evaluation artifacts are written under `reports/`, `results/`, and `plots/`; the kept copies live in `backend/evaluation/depression_three_model_comparison/`.

The removed local scripts (`app/ai/depression_detection/train.py`, `evaluation/depression_v2/evaluate_depression_v2.py`) are no longer part of the tree; the notebook is the supported training/evaluation path. Check installed library versions before running.

## 10. Responsible use, privacy, and data handling

- Do not use this classifier to diagnose, triage, deny services, or make treatment decisions.
- Do not infer that a "No Depression" output means a person is safe or has no depression. High confidence does not remove this limitation.
- Treat source posts and model inputs as sensitive mental-health information. Follow applicable consent, platform terms, dataset license, retention, and access-control requirements; avoid publishing raw text unnecessarily.
- Document the source/license and annotation method before redistributing data or model outputs. The current repository does not fully document V2 provenance or license.
- Any crisis or self-harm response must be handled by a separate, explicit safety process; this binary model is not a suicide-risk detector.
- Evaluate across language, dialect, demographic and topic subgroups where ethically and legally appropriate, and review false negatives as well as false positives.

## 11. Open documentation/research gaps

Before presenting the dataset/model as fully reproducible, record: canonical dataset citation and version; license/terms; collection and labeling methods; inclusion/exclusion criteria; exact V2 cleaning script; class counts for all three splits; split strategy and seed; duplicate/near-duplicate leakage audit; source overlap; preprocessing/tokenizer versions; full training environment; checkpoint selection; calibration; external validation; and model/data hashes. At present, several of these are not established by the checked-in V2 source files.
