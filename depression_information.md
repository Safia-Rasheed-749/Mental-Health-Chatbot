# Depression Dataset and Model — Project Reference

This document records the depression-related data and model pipeline found in this repository. It distinguishes checked-in artifacts from assumptions: where the repository does not establish a detail (for example, exact source provenance for the V2 CSVs), that limitation is stated rather than guessed.

## 1. At a glance

- **Primary/live task:** binary text classification, `No Depression` (label `0`) vs `Depression` (label `1`).
- **Primary model:** `roberta-base` fine-tuned for sequence classification.
- **Current V2 split:** 5,355 training, 1,147 validation, and 1,148 test examples (7,650 total, as documented by the V2 training/evaluation assets).
- **Current dataset files:** `backend/datasets/depression_v2/processed/{train.csv,validation.csv,test.csv}`.
- **Model artifacts:** `backend/models/depression_v2/` (directory is loaded by the runtime predictor).
- **Reported held-out test result:** 98.00% accuracy on 1,148 test examples. This is a dataset-specific result, not evidence of clinical or real-world diagnostic accuracy.
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

### V1 — legacy pipeline

- Expected raw input (referenced in scripts; raw folder is ignored/not present in the checked-in workspace): `backend/datasets/depression/raw/depression_dataset_reddit_cleaned.csv`.
- Legacy loader: `backend/app/ai/depression_detection/dataset_loader.py`.
- Legacy processed data: `backend/datasets/depression/processed/clean_dataset.csv`, with a backup at `clean_dataset_backup.csv`; `train.csv` and `validation.csv` are also present.
- The loader selects `clean_text` and `is_depression`, renames them to `text` and `label`, drops duplicate rows, then drops missing rows.
- Legacy split script creates an 80/20 train/validation split using `random_state=42` and stratification on `label`; it does not make a test split.
- `backend/app/ai/depression_detection/preprocessing.py` is also legacy. It lowercases text, attempts to remove URLs, removes non-ASCII letters, and collapses whitespace. It reads and writes the same `clean_dataset.csv` path, so running it overwrites that file. It is **not shown as the V2 preparation pipeline**.

The historical V1 scripts use relative paths rooted at the current working directory and expect to be run from `backend/` (or an equivalent working directory), e.g. `python app/ai/depression_detection/dataset_loader.py`. The current V2 trainer uses paths derived from its own file location and is less dependent on the shell working directory.

## 3. Provenance and interpretation

The legacy filename and text suggest Reddit-origin material, and the V2 evaluation artifacts show informal, Reddit-like post excerpts. However, the checked repository does not document a verifiable V2 dataset citation, license, collection date, Reddit communities, sampling method, annotation protocol, or the exact relationship between V1 and V2. Treat those as **unknown pending provenance confirmation**, not established facts.

Labels are dataset labels, not diagnoses assigned by this model. A post can discuss depression without its author having a diagnosis; a post can be labeled “No Depression” while containing distress, and a classifier can miss context, sarcasm, negation, or risk. The negative class also does not mean “healthy.”

## 4. Cleaning, preprocessing, and tokenization

### What the V1 scripts do

`dataset_loader.py` selects the two fields, renames them, removes exact duplicate rows, drops rows with missing values, and saves `clean_dataset.csv`. The subsequent legacy `preprocessing.py` performs text normalization, but its regex source uses doubled backslashes (for example `r"http\\S+"`), which may not behave as intended for URL/whitespace matching. Inspect/fix and test this before relying on it. The file overwrites its input.

### What the V2 trainer does

`backend/app/ai/depression_detection/train.py` loads the pre-existing V2 train and validation CSVs through Hugging Face Datasets. It checks that labels are exactly `[0, 1]`; it does not load test rows into the Trainer. Each text is encoded by the `roberta-base` tokenizer with truncation, fixed-length padding, and `max_length=128`. The label column is renamed to `labels` and converted to Torch tensors. The checked training script does **not** itself lowercase, strip HTML/URLs, deduplicate, drop missing rows, or create the CSV splits. The runtime predictor likewise applies only `.strip()` to input before tokenizer encoding.

Thus, do not describe legacy V1 cleaning as V2 cleaning. The V2 CSVs are called “processed,” but their upstream transformations are not recoverable from the available scripts.

## 5. Training details (V2)

Source: `backend/app/ai/depression_detection/train.py`.

- Base model: `roberta-base`; two output labels.
- Random seed: `42` (set with Transformers `set_seed`, and in TrainingArguments).
- Maximum token length: `128`.
- Epochs: `4`.
- Learning rate: `2e-5`.
- Per-device train/evaluation batch size: `4`.
- Weight decay: `0.01`; gradient accumulation: `1`.
- Evaluate and save each epoch; keep up to two checkpoints; reload best model according to validation accuracy.
- Binary precision/recall/F1 and accuracy are computed during evaluation; training runs with Hugging Face `Trainer`.
- Test CSV is checked for existence by the training script but is deliberately not loaded by Trainer.
- Saved model output: `backend/models/depression_v2/`, including tokenizer/model files and configured training logs/results. Exact library versions and complete run reproducibility are not fixed in the script.

The script uses `get_last_checkpoint()` and can resume training when a checkpoint exists. For a clean independent rerun, use a separately named output folder or preserve/copy existing artifacts first; do not remove existing model/checkpoint data without authorization.

## 6. Evaluation and reported performance

Evaluation source: `backend/evaluation/depression_v2/evaluate_depression_v2.py`; notebook: `backend/notebooks/04_depression_detection_v2.ipynb`.

The saved report `backend/evaluation/depression_v2/depression_v2_metrics.txt` records:

| Metric | Reported value |
|---|---:|
| Accuracy | 98.00% |
| Binary precision (positive = Depression) | 98.74% |
| Binary recall | 97.16% |
| Binary F1 | 97.94% |
| Macro F1 | 98.00% |
| Correct / incorrect | 1,125 / 23 |

Reported confusion matrix (rows actual, columns predicted; order `No Depression`, `Depression`): `[[577, 7], [16, 548]]`. Test counts in the report are 584 `No Depression` and 564 `Depression`.

Related output files include:

- `backend/evaluation/depression_v2/depression_v2_metrics.txt` and `depression_v2_metrics_notebook.txt` — metric reports.
- `depression_v2_predictions.csv` and `depression_v2_predictions_notebook.csv` — per-example predictions.
- `depression_v2_wrong_predictions.csv` — error review.
- `depression_v2_confusion_matrix.png` and `depression_v2_confusion_matrix_nb.png` — confusion matrices.
- `depression_v2_confidence_analysis.txt` — confidence analysis.

The numbers above are transcribed from saved project artifacts, not independently recomputed here. The 98% result should be investigated for duplicates or near-duplicates crossing splits, source/subreddit or annotation artifacts, leakage, and calibration. A single random held-out test set does not establish external validity. Include class-level metrics and uncertainty intervals in formal reporting where possible.

## 7. Runtime usage

Production scope lists the Depression RoBERTa classifier as active (`backend/MODEL_SCOPE.md`). Runtime implementation: `backend/app/ai/depression_detection/predict.py`.

It loads model and tokenizer locally from `backend/models/depression_v2/`, tokenizes at max length 128, computes softmax probabilities, and returns:

```json
{"depression": "Depression", "label": 1, "confidence": 98.7}
```

`confidence` is the maximum softmax probability expressed as a percentage. It is not calibrated clinical confidence or a probability that a person has a disorder. The predictor is called from chat services; user-facing product language should say “model prediction/signal,” never diagnosis. The model can fail on short, out-of-domain, multilingual, or context-dependent messages.

## 8. Useful related files

| File/folder | Role |
|---|---|
| `backend/app/ai/depression_detection/train.py` | V2 fine-tuning |
| `backend/app/ai/depression_detection/predict.py` | Runtime inference |
| `backend/app/ai/depression_detection/dataset_loader.py` | Legacy V1 raw-to-clean loader |
| `backend/app/ai/depression_detection/preprocessing.py` | Legacy V1 text cleaner |
| `backend/app/ai/depression_detection/train_test_split.py` | Legacy V1 80/20 split |
| `backend/datasets/depression/processed/` | Legacy V1 processed files |
| `backend/datasets/depression_v2/processed/` | Current V2 CSV splits |
| `backend/models/depression_v2/` | V2 model/tokenizer/checkpoints |
| `backend/evaluation/depression_v2/` | V2 test results and analysis |
| `backend/notebooks/04_depression_detection_v2.ipynb` | V2 evaluation notebook |
| `backend/MODEL_SCOPE.md` | Production vs experimental model scope |

## 9. Reproduction outline

From the repository root, run the V2 trainer with the backend environment and project import/dependency setup, for example:

```powershell
cd backend
python app/ai/depression_detection/train.py
```

The three V2 processed CSVs and required Python dependencies must be present. The script saves output under `models/depression_v2`. Final test evaluation should be run separately with `python evaluation/depression_v2/evaluate_depression_v2.py` after training/model availability is confirmed. Check the scripts' expected paths and installed versions before running; this document does not execute or overwrite training artifacts.

For V1, scripts expect the raw CSV under `datasets/depression/raw/`; the raw input is not present in the inspected local data paths, so the V1 loader cannot be reproduced from this checkout alone.

## 10. Responsible use, privacy, and data handling

- Do not use this classifier to diagnose, triage, deny services, or make treatment decisions.
- Do not infer that a “No Depression” output means a person is safe or has no depression. High confidence does not remove this limitation.
- Treat source posts and model inputs as sensitive mental-health information. Follow applicable consent, platform terms, dataset license, retention, and access-control requirements; avoid publishing raw text unnecessarily.
- Document the source/license and annotation method before redistributing data or model outputs. The current repository does not fully document V2 provenance or license.
- Any crisis or self-harm response must be handled by a separate, explicit safety process; this binary model is not a suicide-risk detector.
- Evaluate across language, dialect, demographic and topic subgroups where ethically and legally appropriate, and review false negatives as well as false positives.

## 11. Open documentation/research gaps

Before presenting the dataset/model as fully reproducible, record: canonical dataset citation and version; license/terms; collection and labeling methods; inclusion/exclusion criteria; exact V2 cleaning script; class counts for all three splits; split strategy and seed; duplicate/near-duplicate leakage audit; source overlap; preprocessing/tokenizer versions; full training environment; checkpoint selection; calibration; external validation; and model/data hashes. At present, several of these are not established by the checked-in V2 source files.
