# Dataset audit

Generated (UTC): 2026-10-19T10:09:25.968035+00:00

This report inventories CSV files, missing fields, class balance, exact duplicates, and near-duplicate train/split overlap.

| CSV | Rows | Text | Label | Exact row dupes | Exact text dupes |
|---|---:|---|---|---:|---:|
| `backend\datasets\depression_v2\processed\test.csv` | 1148 | text | label | 0 | 0 |
| `backend\datasets\depression_v2\processed\train.csv` | 5355 | text | label | 1 | 1 |
| `backend\datasets\depression_v2\processed\validation.csv` | 1147 | text | label | 0 | 0 |
| `backend\datasets\independent_test\mental_health_combined_test.csv` | 125 | text | label | 58 | 58 |
| `backend\datasets\processed\clean_dev.csv` | 5426 | text | label | 0 | 20 |
| `backend\datasets\processed\clean_test.csv` | 5427 | text | label | 0 | 17 |
| `backend\datasets\processed\clean_train.csv` | 43407 | text | label | 0 | 522 |
| `backend\datasets\stress\processed\clean_test.csv` | 715 | text | label | 0 | 0 |
| `backend\datasets\stress\processed\clean_train.csv` | 2823 | text | label | 2 | 5 |
| `counsel_chat\emotion_dataset\processed\test_processed.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\processed\train_processed.csv` | 15999 | text | label | 0 | 30 |
| `counsel_chat\emotion_dataset\processed\validation_processed.csv` | 2000 | text | label | 0 | 2 |
| `counsel_chat\emotion_dataset\raw\test.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\raw\train.csv` | 16000 | text | label | 1 | 31 |
| `counsel_chat\emotion_dataset\raw\validation.csv` | 2000 | text | label | 0 | 2 |
| `counsel_chat\processed\train_processed.csv` | 2612 | not inferred | not inferred | 0 | 0 |
| `counsel_chat\raw\train.csv` | 2775 | not inferred | not inferred | 0 | 0 |

## Cross-split exact duplicate text

- `backend\datasets\depression_v2\processed\test.csv` vs `backend\datasets\depression_v2\processed\train.csv`: 1 duplicate texts
- `backend\datasets\processed\clean_dev.csv` vs `backend\datasets\processed\clean_test.csv`: 25 duplicate texts
- `backend\datasets\processed\clean_dev.csv` vs `backend\datasets\processed\clean_train.csv`: 92 duplicate texts
- `backend\datasets\processed\clean_test.csv` vs `backend\datasets\processed\clean_train.csv`: 85 duplicate texts
- `backend\datasets\stress\processed\clean_test.csv` vs `backend\datasets\stress\processed\clean_train.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\train_processed.csv`: 11 duplicate texts
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\processed\train_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: 5 duplicate texts
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\train.csv`: 11 duplicate texts
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: 3 duplicate texts
- `counsel_chat\emotion_dataset\raw\train.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: 5 duplicate texts

## Near-duplicate checks

- `backend\datasets\depression_v2\processed\test.csv` vs `backend\datasets\depression_v2\processed\train.csv`: complete; 14 pairs at cosine ≥ 0.95 (possible comparisons: 6147540).
- `backend\datasets\depression_v2\processed\train.csv` vs `backend\datasets\depression_v2\processed\validation.csv`: complete; 6 pairs at cosine ≥ 0.95 (possible comparisons: 6142185).
- `backend\datasets\processed\clean_dev.csv` vs `backend\datasets\processed\clean_train.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 235526382).
- `backend\datasets\processed\clean_test.csv` vs `backend\datasets\processed\clean_train.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 235569789).
- `backend\datasets\stress\processed\clean_test.csv` vs `backend\datasets\stress\processed\clean_train.csv`: complete; 3 pairs at cosine ≥ 0.95 (possible comparisons: 2018445).
- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\train_processed.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 31998000).
- `counsel_chat\emotion_dataset\processed\train_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 31998000).
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\train.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 32000000).
- `counsel_chat\emotion_dataset\raw\train.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: skipped_pair_cap; 0 pairs at cosine ≥ 0.95 (possible comparisons: 32000000).

Skipped comparisons are unknown, not clean. Similarity flags require manual review. See `dataset_audit.json` for exact details.
