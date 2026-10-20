# Classifier protocol template — fill from the actual training run

Copy this file to the relevant task folder (`emotion`, `depression`, `stress`) and replace `UNKNOWN` only with verifiable run records.

- Active model artifact path: `UNKNOWN`
- Artifact SHA-256: generated in `../baseline/MODEL_HASHES.json` after baseline capture
- Dataset source/revision/license: `UNKNOWN — see ../datasets/PROVENANCE.md`
- Dataset files and SHA-256: `../baseline/DATASET_HASHES.json`
- Exact train/validation/test row counts and class counts: `UNKNOWN — generate from dataset audit and training logs`
- Split strategy and random seed: `UNKNOWN`
- Text preprocessing/tokenization: `UNKNOWN`
- Base model and immutable revision: `UNKNOWN`
- Hyperparameters, epochs, early stopping and selection metric: `UNKNOWN`
- Python / PyTorch / Transformers versions: `../baseline/pip-freeze.txt`
- Hardware and runtime: `UNKNOWN`
- Reproduction command: `UNKNOWN — recover exact command from training logs before claiming reproducibility`
- Leakage checks: see `../datasets/DATASET_AUDIT.md`; exact and near duplicates require review
- Calibration, bootstrap confidence intervals and class-wise errors: `PENDING`
- Exact split overlap and normalized near-duplicate check: `../datasets/classifier_splits/DATASET_AUDIT.md` (if generated); skipped pair IDs are listed in JSON and remain unknown.
- Held-out prediction recalculation and false-negative review: `HELDOUT_METRICS.md` / `HELDOUT_METRICS.json` (generated from saved predictions only; does not represent retraining).

The existing scores are task- and split-specific classifier results, not clinical validation. Do not publish them as diagnostic accuracy.
