# Validation baseline capture

Captured: 2026-10-19T10:07:58.121883+00:00

- Git commit: `63af4671f1fcb4ce1a51de3839feceaa3e596b16`
- Worktree: dirty; see environment.json
- A Git tag was intentionally not created because the existing worktree includes uncommitted user/project changes.
- Python package snapshot: `pip-freeze.txt`
- SHA-256 manifests: `MODEL_HASHES.json`, `DATASET_HASHES.json`, and `KB_HASHES.json`
- Runtime availability probes: `environment.json`

A captured dirty-tree environment does not establish a reproducible clean checkout. Commit/tag only after the owner reviews and approves the full diff.
