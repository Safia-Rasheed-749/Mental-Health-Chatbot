# DAIR-AI Emotion Detection — Project Report

## 1. Scope

This report documents only the DAIR-AI Emotion (`dair-ai/emotion`) text-classification work found in this repository. It describes the dataset files, preparation and training code, runtime integration, evaluation artifacts, recorded results, and observed project-state limitations. It does not describe the separate GoEmotions, MELD, stress, or depression classifiers except where needed to distinguish them.

## 2. Executive summary

The project includes a six-class emotion classification pipeline based on the Hugging Face dataset `dair-ai/emotion`. The training script fine-tunes `roberta-base`, saves a model intended to be named `emotion_dair_ai_roberta`, and evaluates the held-out test split. The saved evaluation report records 92.95% accuracy and 92.84% weighted F1 on 2,000 test samples.

The raw and processed DAIR-AI CSV files are present in `backend/datasets/emotion_dataset/`. Training, prediction, and evaluation source files are also present. However, the expected saved model directory `backend/models/emotion_dair_ai_roberta/` was not present when this report was prepared. The runtime predictor loads strictly from that local directory, so model inference requires the trained model and tokenizer artifacts to be present there.

## 3. Dataset

### 3.1 Source and task

- **Dataset identifier:** `dair-ai/emotion`
- **Source used by loader:** Hugging Face Datasets (`load_dataset("dair-ai/emotion")`)
- **Task:** Single-label, six-way text emotion classification
- **Expected input:** A text string
- **Expected target:** Integer class ID in the `label` column

### 3.2 Label mapping

| Label ID | Emotion |
|---:|---|
| 0 | sadness |
| 1 | joy |
| 2 | love |
| 3 | anger |
| 4 | fear |
| 5 | surprise |

The training script writes this mapping to `label_mapping.json` inside its model output directory. Evaluation artifacts also include a label-mapping JSON.

### 3.3 Dataset paths in this project

Raw CSV files, produced by `backend/app/ai/emotion_dataset/dataset_loader.py`:

```text
backend/datasets/emotion_dataset/raw/train.csv
backend/datasets/emotion_dataset/raw/validation.csv
backend/datasets/emotion_dataset/raw/test.csv
```

Processed CSV files, consumed by the training script:

```text
backend/datasets/emotion_dataset/processed/train_processed.csv
backend/datasets/emotion_dataset/processed/validation_processed.csv
backend/datasets/emotion_dataset/processed/test_processed.csv
```

The files exist in the repository workspace. The source dataset is also obtained through Hugging Face when the loader is run, which requires the `datasets` package and access to the Hugging Face dataset source/cache.

### 3.4 Dataset preparation behavior

`dataset_loader.py` downloads/loads the source dataset, converts each split to a pandas DataFrame, and writes the three raw CSVs. The raw schema is expected to contain at least `text` and `label`.

`preprocessing.py`:

1. Reads the three raw CSVs.
2. Drops duplicate rows.
3. Drops rows containing missing values.
4. Converts text to lowercase and trims leading/trailing whitespace.
5. Writes the processed CSV files.

The preprocessing code does not perform stemming, lemmatization, or punctuation removal. Tokenization is handled later by the RoBERTa tokenizer.

`label_encoder.py` adds an `emotion` string column based on the six-class mapping while retaining the numeric `label` column needed for training.

> **Path note:** The preparation scripts build dataset paths relative to the process working directory. Run them with the backend directory as the working directory so `datasets/emotion_dataset/...` resolves to `backend/datasets/emotion_dataset/...`.

## 4. Model and training

### 4.1 Main training source

```text
backend/app/ai/emotion_dataset/train_dair_ai.py
```

The script reads the processed CSV splits, validates that the training split has six distinct labels, loads the CSV splits as a Hugging Face `DatasetDict`, tokenizes text with the `roberta-base` tokenizer, fine-tunes `AutoModelForSequenceClassification`, evaluates validation and test data, and saves the model/tokenizer and evaluation output.

### 4.2 Model configuration

| Setting | Value in source |
|---|---|
| Base model | `roberta-base` |
| Number of labels | 6 |
| Maximum sequence length | 128 tokens |
| Epochs | 3 |
| Learning rate | `2e-5` |
| Per-device train batch size | 4 |
| Per-device evaluation batch size | 4 |
| Gradient accumulation steps | 2 |
| Weight decay | 0.01 |
| Seed | 42 |
| Best model selection | Validation accuracy |
| Dynamic padding | `DataCollatorWithPadding` |
| Reported metrics | Accuracy, weighted precision, weighted recall, weighted F1 |

Training evaluates periodically by steps, saves checkpoints, limits retained checkpoints, and is coded to detect a prior checkpoint. The script saves the final model and tokenizer under:

```text
backend/models/emotion_dair_ai_roberta/
```

It also writes the six-label mapping and an `evaluation_results.txt` file under that model directory after training completes.

### 4.3 Training entry point behavior

The training script uses absolute paths derived from its own location for dataset and model paths. It checks that all three processed CSV files exist and raises `FileNotFoundError` if one is missing. It expects a `label` column with integer values and text in `text`.

## 5. Runtime prediction and application integration

### 5.1 Predictor

```text
backend/app/ai/emotion_detection/predict.py
```

The predictor derives the backend path from its source location and expects:

```text
backend/models/emotion_dair_ai_roberta/
    config.json
    model weights (for example, model.safetensors or pytorch_model.bin)
    tokenizer files
    label_mapping.json
```

The exact model-weight filename depends on the Transformers version/save format. `predict.py` loads tokenizer and model with `local_files_only=True`, sets the model to evaluation mode, tokenizes input with truncation and padding (maximum length 96 in this predictor), applies softmax, and returns the highest-probability class.

Function contract:

```python
predict_emotion(text: str) -> {
    "emotion": str,
    "label": int,
    "confidence": float,  # percentage, rounded to 2 decimals
}
```

It raises `TypeError` for non-string input and `ValueError` for blank text.

### 5.2 Chat service integration

`backend/app/services/chat_service.py` calls `predict_emotion(text)` and includes the resulting `emotion` and `emotion_confidence` in its analysis result. The same service also calls the project’s separate stress and depression predictors; those are not part of the DAIR-AI emotion model.

### 5.3 Important runtime limitation

The expected model folder `backend/models/emotion_dair_ai_roberta/` was not found in the project files during inspection. Therefore, the source code and datasets are present, but local runtime prediction cannot load the DAIR-AI model unless its trained model/tokenizer artifacts and mapping file are generated or supplied at that path. Because loading is local-only, prediction does not automatically download missing model artifacts.

## 6. DAIR-AI code and artifact inventory

### 6.1 Dataset-specific source files

Directory: `backend/app/ai/emotion_dataset/`

| File | Role |
|---|---|
| `dataset_loader.py` | Loads `dair-ai/emotion` and writes raw split CSV files. |
| `preprocessing.py` | Cleans raw split files and writes processed CSV files. |
| `label_encoder.py` | Adds readable emotion names using the six-class mapping. |
| `label_mapping.py` | Label mapping helper. |
| `show_labels.py` | Displays labels for dataset inspection. |
| `dataset_summary.py` | Prints processed split shapes, columns, and class information. |
| `check_dataset.py` | Checks raw dataset files. |
| `check_processed.py` | Checks processed dataset files. |
| `dataset.py` | Dataset-related helper code. |
| `utils.py` | Supporting utilities. |
| `train_dair_ai.py` | Main DAIR-AI RoBERTa training/evaluation pipeline. |

### 6.2 Runtime source files

| File | Role |
|---|---|
| `backend/app/ai/emotion_detection/predict.py` | Loads the local DAIR-AI model and predicts an emotion. |
| `backend/app/services/chat_service.py` | Calls the emotion predictor as part of chat text analysis. |

The directory `backend/app/ai/emotion_detection/` also contains GoEmotions-related scripts and components. Those are not the DAIR-AI six-class trainer; `train_dair_ai.py` is the DAIR-AI-specific training source.

### 6.3 Evaluation source and output files

Directory: `backend/evaluation/dair_ai_emotion/`

Source scripts:

- `evaluate_emotion.py` — test-set evaluation and report generation.
- `extract_emotion_config.py` — extracts model configuration information.
- `read_emotion_training_args.py` — reads saved training arguments.
- `plot_emotion_training.py` — plots training/evaluation values.

Saved evaluation artifacts present in that directory:

- `emotion_metrics.txt`
- `emotion_classification_report.txt`
- `emotion_predictions.csv`
- `emotion_wrong_predictions.csv`
- `emotion_label_mapping.json`
- `emotion_training_history.json`
- `emotion_training_args.txt`
- `emotion_evaluation_terminal.txt`
- `emotion_confusion_matrix.png`
- `emotion_training_loss.png`
- `emotion_validation_loss.png`
- `emotion_validation_accuracy.png`

The metrics and plots are stored evaluation outputs; they should not be confused with the runtime model weights.

### 6.4 Additional project notebook/script

The repository root includes `# %% [markdown].py`, a notebook-style Python export documenting another RoBERTa-base DAIR-AI workflow. It reads the same raw/processed dataset locations and names the model output `emotion_dair_ai_roberta`. It is supplementary to the dedicated `train_dair_ai.py` script; check its current directory assumptions and configuration before running it.

## 7. Recorded evaluation results

The saved report `backend/evaluation/dair_ai_emotion/emotion_metrics.txt` identifies the base model as `roberta-base`, the fine-tuned model as `emotion_dair_ai_roberta`, the dataset as `dair-ai/emotion`, and the test set as 2,000 samples.

| Metric | Saved result |
|---|---:|
| Accuracy | 0.929500 (92.95%) |
| Weighted precision | 0.931699 (93.17%) |
| Weighted recall | 0.929500 (92.95%) |
| Weighted F1 | 0.928393 (92.84%) |
| Macro precision | 0.909220 (90.92%) |
| Macro recall | 0.873943 (87.39%) |
| Macro F1 | 0.886812 (88.68%) |
| Correct predictions | 1,859 / 2,000 |
| Incorrect predictions | 141 / 2,000 |
| Recorded evaluation time | 227.94 seconds |

### 7.1 Per-class test results

| Emotion | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| sadness | 97.86% | 94.66% | 96.24% | 581 |
| joy | 93.32% | 96.55% | 94.91% | 695 |
| love | 93.60% | 73.58% | 82.39% | 159 |
| anger | 93.07% | 92.73% | 92.90% | 275 |
| fear | 82.77% | 98.66% | 90.02% | 224 |
| surprise | 84.91% | 68.18% | 75.63% | 66 |

The saved confusion matrix is:

```text
[[550   4   0  18   9   0]
 [  4 671   8   1   3   8]
 [  0  42 117   0   0   0]
 [  3   2   0 255  15   0]
 [  3   0   0   0 221   0]
 [  2   0   0   0  19  45]]
```

Rows and columns follow label order: sadness, joy, love, anger, fear, surprise. The lower recall for surprise and love relative to the other classes is visible in the report. The saved results are reported project artifacts; this report does not claim the model was retrained or the metrics were independently reproduced.

## 8. Reproduction workflow

The following is the workflow represented by the repository code. Run from the backend project directory for scripts using relative dataset paths:

1. Load and export source splits using `app/ai/emotion_dataset/dataset_loader.py`.
2. Generate processed CSVs using `app/ai/emotion_dataset/preprocessing.py`.
3. Optionally add readable labels and inspect the dataset using `label_encoder.py`, `dataset_summary.py`, and the check/show scripts.
4. Run `app/ai/emotion_dataset/train_dair_ai.py` to fine-tune, evaluate, and save the model.
5. Confirm the model, tokenizer, and `label_mapping.json` exist under `models/emotion_dair_ai_roberta/`.
6. Run `evaluation/dair_ai_emotion/evaluate_emotion.py` if a fresh evaluation is needed. Its model and dataset paths are derived from its location and point to the expected backend model/data folders.
7. Start the backend and test `predict_emotion()` through the application flow.

The repository does not include a single requirements list in this report. The relevant Python environment must provide compatible versions of PyTorch, Transformers, Datasets, pandas, NumPy, scikit-learn, and Matplotlib. Model training may require substantial compute and downloads of the base model/tokenizer.

## 9. Limitations and checks before relying on results

1. **Model artifact availability:** The expected trained model directory was absent at inspection; runtime prediction needs that directory populated.
2. **Reported metrics versus reproducibility:** Metrics are present as saved files. Re-running training/evaluation is needed to independently verify them in the current environment.
3. **Training and predictor maximum lengths differ:** The training script uses 128 tokens; `predict.py` truncates at 96 tokens. This is not necessarily invalid, but should be confirmed as intentional and kept consistent if exact serving parity is required.
4. **Preprocessing is lightweight:** It lowercases/trims and removes missing/duplicate rows; it does not normalize spelling or handle domain-specific text beyond that.
5. **Class-level variation:** The saved results show notably lower recall for surprise and love than for the larger sadness/joy classes. Consider per-class evaluation when using the model in the mental-health chatbot.
6. **Not a clinical assessment:** The classifier predicts a dataset emotion label from text. It is not a diagnosis, crisis detector, or clinical measure.
7. **Working-directory sensitivity:** Dataset utility scripts use relative paths, so running them from the wrong directory can create/read files in an unintended location.

## 10. Bottom line

The repository contains a complete DAIR-AI six-emotion data-preparation and RoBERTa training/evaluation source pipeline, the raw and processed dataset CSVs, and recorded test-evaluation outputs. It also has runtime integration code. The key operational gap is the missing `backend/models/emotion_dair_ai_roberta/` artifact directory: provide or regenerate the local model and tokenizer artifacts there before expecting the application predictor to work.
