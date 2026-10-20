# Dataset audit

Generated (UTC): 2026-10-20T06:51:06.830701+00:00

This report inventories CSV files, missing fields, class balance, exact duplicates, and near-duplicate train/split overlap.

| CSV | Rows | Text | Label | Exact row dupes | Exact text dupes |
|---|---:|---|---|---:|---:|
| `counsel_chat\emotion_dataset\processed\test_processed.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\processed\train_processed.csv` | 15999 | text | label | 0 | 30 |
| `counsel_chat\emotion_dataset\processed\validation_processed.csv` | 2000 | text | label | 0 | 2 |
| `counsel_chat\emotion_dataset\raw\test.csv` | 2000 | text | label | 0 | 0 |
| `counsel_chat\emotion_dataset\raw\train.csv` | 16000 | text | label | 1 | 31 |
| `counsel_chat\emotion_dataset\raw\validation.csv` | 2000 | text | label | 0 | 2 |

## Cross-split exact duplicate text

- `counsel_chat\emotion_dataset\processed\test_processed.csv` (test) vs `counsel_chat\emotion_dataset\processed\train_processed.csv` (train): 11 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\test_processed.csv` (test) vs `counsel_chat\emotion_dataset\processed\validation_processed.csv` (validation): 3 normalized text hashes; cross-split overlap; review provenance
- `counsel_chat\emotion_dataset\processed\test_processed.csv` (test) vs `counsel_chat\emotion_dataset\raw\test.csv` (test): 2000 normalized text hashes; same-split source copies, not train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\test_processed.csv` (test) vs `counsel_chat\emotion_dataset\raw\train.csv` (train): 11 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\test_processed.csv` (test) vs `counsel_chat\emotion_dataset\raw\validation.csv` (validation): 3 normalized text hashes; cross-split overlap; review provenance
- `counsel_chat\emotion_dataset\processed\train_processed.csv` (train) vs `counsel_chat\emotion_dataset\processed\validation_processed.csv` (validation): 5 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\train_processed.csv` (train) vs `counsel_chat\emotion_dataset\raw\test.csv` (test): 11 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\train_processed.csv` (train) vs `counsel_chat\emotion_dataset\raw\train.csv` (train): 15969 normalized text hashes; same-split source copies, not train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\train_processed.csv` (train) vs `counsel_chat\emotion_dataset\raw\validation.csv` (validation): 5 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\validation_processed.csv` (validation) vs `counsel_chat\emotion_dataset\raw\test.csv` (test): 3 normalized text hashes; cross-split overlap; review provenance
- `counsel_chat\emotion_dataset\processed\validation_processed.csv` (validation) vs `counsel_chat\emotion_dataset\raw\train.csv` (train): 5 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\processed\validation_processed.csv` (validation) vs `counsel_chat\emotion_dataset\raw\validation.csv` (validation): 1998 normalized text hashes; same-split source copies, not train/evaluation leakage
- `counsel_chat\emotion_dataset\raw\test.csv` (test) vs `counsel_chat\emotion_dataset\raw\train.csv` (train): 11 normalized text hashes; POTENTIAL train/evaluation leakage
- `counsel_chat\emotion_dataset\raw\test.csv` (test) vs `counsel_chat\emotion_dataset\raw\validation.csv` (validation): 3 normalized text hashes; cross-split overlap; review provenance
- `counsel_chat\emotion_dataset\raw\train.csv` (train) vs `counsel_chat\emotion_dataset\raw\validation.csv` (validation): 5 normalized text hashes; POTENTIAL train/evaluation leakage

## Near-duplicate checks

Method: Unicode NFKC + casefold + URL replacement + punctuation removal + whitespace collapse; character 3–5-gram Jaccard evaluated for candidate pairs from bottom-32 MinHash LSH (8 bands × 4 values). Exact normalized matches are separately detected exhaustively. Candidate generation is approximate; near-duplicate recall is not guaranteed.

- `counsel_chat\emotion_dataset\processed\test_processed.csv` vs `counsel_chat\emotion_dataset\processed\train_processed.csv`: complete; 0 flagged candidate pairs at Jaccard ≥ 0.95; candidate similarities computed 668; skipped ranges 0 (all-pairs possible: 31998000).
- `counsel_chat\emotion_dataset\processed\train_processed.csv` vs `counsel_chat\emotion_dataset\processed\validation_processed.csv`: complete; 0 flagged candidate pairs at Jaccard ≥ 0.95; candidate similarities computed 713; skipped ranges 0 (all-pairs possible: 31998000).
- `counsel_chat\emotion_dataset\raw\test.csv` vs `counsel_chat\emotion_dataset\raw\train.csv`: complete; 0 flagged candidate pairs at Jaccard ≥ 0.95; candidate similarities computed 668; skipped ranges 0 (all-pairs possible: 32000000).
- `counsel_chat\emotion_dataset\raw\train.csv` vs `counsel_chat\emotion_dataset\raw\validation.csv`: complete; 0 flagged candidate pairs at Jaccard ≥ 0.95; candidate similarities computed 713; skipped ranges 0 (all-pairs possible: 32000000).

Similarity flags indicate possible leakage, not proof of it; inspect source data and labels before interpreting. Comparisons listed as skipped are unknown, not clean. See `dataset_audit.json` for row-level details.
