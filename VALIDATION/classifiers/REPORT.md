# Classifier validity and reproducibility report

**Scope:** repository evidence review and recalculation from saved held-out predictions. No classifier was retrained in this remediation. No clinical validity claim is made.

## Acceptance status

| Criterion | Result | Evidence / limitation |
|---|---|---|
| Exact duplicates within/across classifier splits | Completed for available local split files | `../datasets/classifier_splits/DATASET_AUDIT.md` and JSON record row numbers, label values and SHA-256 hashes of normalized text. Exact train/evaluation overlaps: depression 1, stress 3, local emotion corpus 11 test/train and 5 train/validation. Local emotion raw/processed same-split copies are separately identified. |
| Near-duplicate method and explicit limits | Implemented; targeted tests pass | Normalized char 3–5-gram Jaccard on bottom-32 MinHash-LSH candidates; possible approximate recall documented. Pair cap emits exact unprocessed row-range spans. |
| Dataset source/license trace | Partial | `../datasets/PROVENANCE.md`; unknown/unverified permissions remain unresolved. |
| Training protocol reproducibility | Partial | `REPRODUCIBILITY.md`; stress path/seed/validation leak fixed in code but no training run. Emotion/depression still Colab-only/archived. |
| Held-out confusion/class metrics and CIs | Passed where archived predictions exist | `HELDOUT_METRICS.json`; emotion per-row predictions unavailable. |
| Calibration | Partial | Top-class ECE only; full probability vectors/Brier not saved. |
| Depression exact-overlap sensitivity | Partial | One test/train exact overlap removed from archived predictions; no clean retraining/deduplicated validation split. |
| Stress false-negative review | Passed for saved comparisons | FN counts, row IDs and coarse non-quoting themes; text deliberately not retained. |

## Dataset overlap

Run `python backend/scripts/audit_datasets.py ...` and review `../datasets/classifier_splits/DATASET_AUDIT.md` plus JSON. The completed audit covers available local depression/stress split files and the local CounselChat emotion raw/processed split copies. It records row numbers, labels, hashes of normalized duplicate text (not text content), split/file paths, method, cap, and skipped comparison ranges. Exact normalized text checks are exhaustive among audited split files. Near-duplicate retrieval uses bottom-32 MinHash LSH over normalized character 3–5-gram shingles; Jaccard similarity is measured exactly for candidates, but candidate recall is approximate. No pair cap was reached in this run. Files are not modified.

Exact overlaps identified include depression test/train 1, stress test/train 3, and local emotion raw/processed train/test 11 and train/validation 5, plus test/validation 3. Raw/processed same-split matching records (e.g. 2,000 test copies) are source copies, not train/evaluation leakage. The local CounselChat emotion corpus is not assumed to be the DAIR-AI `dair-ai/emotion` dataset used in the active model comparison. No near-duplicate candidates at the 0.95 Jaccard threshold were found in the checked split pairs; candidate generation is approximate, so this is not proof of zero near-duplicate leakage.

## Archived held-out prediction recalculation

See `HELDOUT_METRICS.md` and `HELDOUT_METRICS.json` for confusion matrices, class precision/recall/F1, fixed-seed bootstrap intervals, and top-label ECE where saved top-class confidence exists. Current key archived values:

- Depression DeBERTa, N=1,148: accuracy 0.9791; 95% bootstrap interval approximately 0.9713–0.9869. Confusion matrix [[576, 8], [16, 548]]. Exactly one test row overlaps normalized training text and none overlap validation; excluding that row yields N=1,147 and accuracy 0.9791. This sensitivity test does not eliminate near-duplicate/model-selection leakage and does not involve retraining.
- Stress DeBERTa, N=715: accuracy 0.8196; confusion matrix [[266, 80], [49, 320]], including **49 false negatives** (stress class 1 predicted as not stressed).
- Stress RoBERTa, N=715: accuracy 0.7818; confusion matrix [[221, 125], [31, 338]], including **31 false negatives**.
- Stress false-negative records are represented by source row IDs, predicted confidence, and coarse theme counts. Their text excerpts are omitted from evidence to avoid persisting potentially identifiable or sensitive narratives.
- ECE uses 10 equal-width bins and saved maximum-class confidence only. Brier score and full multiclass calibration cannot be calculated from these CSVs; emotion per-example predictions are not retained, so equivalent recalculation is unavailable.

The depression score is still a high archived benchmark result that merits further scrutiny. Only exact overlap was removed in the sensitivity result. A clean deduplicated retraining/test split cannot be claimed because the retained training notebook uses Colab paths and the active training script/model artifacts are missing.

## Reproducibility

See `REPRODUCIBILITY.md` and `../datasets/PROVENANCE.md`. Environment package capture is in `../baseline/pip-freeze.txt`; it does not prove those versions were used in the historical Colab runs. Dataset licenses with no reliable evidence are explicitly **unverified**. Do not redistribute or deploy those datasets without confirming rights.

The stress training script was hardened: it now seeds Python/NumPy/Transformers, anchors paths to the project, and creates stratified validation from train only, leaving `clean_test.csv` untouched for held-out evaluation. This corrected code has not been executed to train a model. Historical comparison metrics remain from the archived experiment and are not results of the corrected pipeline.
