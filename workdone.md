# Work Done and Remaining Issues

## What has been done

- Added a RAG evaluation runner that checks whether the configured Ollama model is installed and saves the generated responses and run details. It does not invent quality scores.
- Added tools that refuse to produce RAG evaluation summaries until both reviewers complete the score sheets.
- Added a dataset audit tool and report for row counts, class balance, missing data, duplicates, and possible train/test overlap.
- Added a small crisis-language test set and report, and expanded detection for some Urdu-script phrases and simple negations.
- Added privacy tests for common email, phone, and Pakistan CNIC formats.
- Corrected the Rozan helpline number in the crisis responses based on its published contact page.
- Added baseline-capture tooling and documentation for dataset provenance, privacy/retention, deployment, and manual end-to-end checks.
- Updated the project audit report to make clear which claims are supported and which checks are still pending.

## Verification completed

- Focused backend tests: **24 passed**.
- Python compilation checks passed.
- `git diff --check` passed.
- Local Ollama was available and had `llama3.2:3b` and `llama3.2:1b` installed when checked.
- The small crisis test matrix reported **0.857 precision and 0.857 recall**. This is only a small diagnostic test, not proof of comprehensive crisis detection.
- Dataset audit found duplicates and possible split overlap. The datasets were not changed; results are recorded for review.

## Issues still remaining

- **RAG/LLM quality is not validated.** Generated answers need two independent human reviewers to complete the score sheets. Retrieval labels also need review. Do not claim answer quality until that work is complete.
- **Dataset provenance and licenses need confirmation.** Some exact and possible near-duplicate examples need investigation. No datasets were silently modified or deduplicated.
- **Classifier reproducibility and validity need more work.** Training details, source licenses, leakage-adjusted metrics, confidence intervals, calibration, and stress false-negative analysis are not yet complete.
- **Safety checks are limited.** Crisis phrase detection can miss indirect or unfamiliar expressions and can false-trigger. The small test matrix is not comprehensive or clinical validation.
- **Privacy review is incomplete.** Redaction covers common patterns only. Log PII exposure, retention, deletion, export, audio handling, and backup deletion need verification.
- **End-to-end workflows are not fully tested.** Live PostgreSQL save/read paths, authentication, user-to-user data isolation, error states, responsive behavior, and accessibility still need checks.
- **Deployment readiness is not demonstrated.** A clean-machine installation, migrations, secrets configuration, SMTP recovery, rate limiting, monitoring, and backup/restore still need testing.
- **Voice workflow is not verified end-to-end.** Microphone, transcription, response playback, consent, and audio retention need a full test if the feature is claimed.
- **Baseline tag/commit was not created.** The repository had existing changes, so no tag or commit was made automatically.

## Overall status

MindCare AI should continue to be described as a **wellness-support prototype**. The work adds useful validation tools and records, but does not establish clinical validity, comprehensive safety, or production readiness.
