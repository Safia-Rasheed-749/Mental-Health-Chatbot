# Dataset audit

Generated (UTC): 2026-10-20T07:35:05.834544+00:00

This report inventories CSV files, missing fields, class balance, exact duplicates, and near-duplicate train/split overlap.

| CSV | Rows | Text | Label | Exact row dupes | Exact text dupes |
|---|---:|---|---|---:|---:|
| `backend\datasets\depression_v2\processed\test.csv` | 1148 | text | label | 0 | 0 |
| `backend\datasets\depression_v2\processed\train.csv` | 5355 | text | label | 1 | 1 |
| `backend\datasets\depression_v2\processed\validation.csv` | 1147 | text | label | 0 | 0 |
| `backend\datasets\stress\processed\clean_test.csv` | 715 | text | label | 0 | 0 |
| `backend\datasets\stress\processed\clean_train.csv` | 2823 | text | label | 2 | 5 |
| `counsel_chat\emotion_dataset\processed\test_processed.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\processed\train_processed.csv` | 15999 | text | label | 0 | 30 |
| `counsel_chat\emotion_dataset\processed\validation_processed.csv` | 2000 | text | label | 0 | 2 |
| `counsel_chat\emotion_dataset\raw\test.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\raw\train.csv` | 16000 | text | label | 1 | 31 |
| `counsel_chat\emotion_dataset\raw\validation.csv` | 2000 | text | label | 0 | 2 |

## Cross-split exact duplicate text

- `backend\datasets\depression_v2\processed\test.csv` vs `backend\datasets\depression_v2\processed\train.csv`: 1 duplicate texts
- `backend\datasets\stress\processed\clean_test.csv` vs `backend\datasets\stress\processed\clean_train.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\train_processed.csv`: 11 duplicate texts
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\processed\train_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: 5 duplicate texts
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\train.csv`: 11 duplicate texts
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\raw\train.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: 5 duplicate texts

## Near-duplicate checks

Method: Unicode NFKC + casefold + URL replacement + punctuation removal + whitespace collapse; character 3–5 gram TF-IDF cosine; threshold as configured. Exact normalized matches are reported separately.

- `backend\datasets\depression_v2\processed\test.csv` vs `backend\datasets\depression_v2\processed\train.csv`: complete; 6 flagged pairs at cosine ≥ 0.95; candidate pairs compared 3181, skipped 0 (all-pairs possible: 6147540).
- `backend\datasets\depression_v2\processed\train.csv` vs `backend\datasets\depression_v2\processed\validation.csv`: complete; 3 flagged pairs at cosine ≥ 0.95; candidate pairs compared 3784, skipped 0 (all-pairs possible: 6142185).
- `backend\datasets\stress\processed\clean_test.csv` vs `backend\datasets\stress\processed\clean_train.csv`: complete; 3 flagged pairs at cosine ≥ 0.95; candidate pairs compared 1910, skipped 0 (all-pairs possible: 2018445).
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\train_processed.csv`: complete; 11 flagged pairs at cosine ≥ 0.95; candidate pairs compared 7128, skipped 0 (all-pairs possible: 31998000).
- `counsel_chat\emotion_dataset\processed\train_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: complete; 5 flagged pairs at cosine ≥ 0.95; candidate pairs compared 7372, skipped 0 (all-pairs possible: 31998000).
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\train.csv`: complete; 11 flagged pairs at cosine ≥ 0.95; candidate pairs compared 7128, skipped 0 (all-pairs possible: 32000000).
- `counsel_chat\emotion_dataset\raw\train.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: complete; 5 flagged pairs at cosine ≥ 0.95; candidate pairs compared 7372, skipped 0 (all-pairs possible: 32000000).

Similarity flags indicate possible leakage, not proof of it; inspect source data and labels before interpreting. Comparisons listed as skipped are unknown, not clean. See `dataset_audit.json` for row-level details.
