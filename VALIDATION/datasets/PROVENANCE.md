# Dataset provenance and licensing register

This register intentionally distinguishes files present in the checkout from facts that have not yet been evidenced. Do not treat a filename, model card, or project recollection as a license grant.

| Dataset/files | Stated use in project | Provenance evidence currently identified | License/redistribution status | Required next action |
|---|---|---|---|---|
| `backend/datasets/processed/clean_{train,dev,test}.csv` | General text classifier experiment/splits | Local processed CSVs; source URL/commit not embedded in the files | Unknown from inspected files | Trace to downloader/source and record source URL, version/date, license, and transformations |
| `backend/datasets/stress/processed/clean_{train,test}.csv` | Stress classifier | Local processed split files | Unknown from inspected files | Record original dataset, source, license, filtering and split method |
| `backend/datasets/depression_v2/processed/{train,validation,test}.csv` | Depression classifier experiments | Local processed files and comparison results | Unknown from inspected files | Trace source/license and document whether text was duplicated or derived |
| `backend/datasets/independent_test/mental_health_combined_test.csv` | Independent task evaluation | Local CSV plus `download_independent_test.py` | Must be checked against each constituent source | Inspect downloader and record source-level licenses and attribution |
| `counsel_chat/raw/train.csv` and `counsel_chat/emotion_dataset/{raw,processed}/*.csv` | Counseling/emotion experiments and RAG source material | Local files include CounselChat URLs/attribution fields | No redistribution license established by this audit | Confirm CounselChat terms, permission, and allowed model/RAG use before redistribution or deployment |
| Hugging Face datasets referenced by training scripts | Classifier training | Source names are discoverable in scripts/configuration but not tied here to a pinned revision | Not yet audited per dataset | Record repository ID, immutable revision, license, download date, and exact split provenance |

`backend/scripts/audit_datasets.py` produces row counts, label balance, missing values, exact duplicate counts and near-duplicate overlap flags. It does not establish legal provenance or data consent. See `dataset_audit.json` after running it. Any near-duplicate result marked skipped is unknown, not a pass.
