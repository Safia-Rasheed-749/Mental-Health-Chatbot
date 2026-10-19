# Validation evidence workspace

This folder contains repeatable evidence and reviewer worksheets. It is not a certification of safety, clinical effectiveness, or production readiness.

## Evidence generation

Run from the repository root unless noted:

```powershell
python backend/scripts/capture_validation_baseline.py
python backend/scripts/audit_datasets.py
python backend/scripts/evaluate_crisis_matrix.py
```

Run the RAG generation capture from `backend` after Ollama is available:

```powershell
python -m app.ai.evaluation_rag_llm.run_evaluation
```

This checks the configured Ollama tag before importing the heavyweight RAG service, writes a timestamped JSONL output and refuses to report model quality. The two reviewers must complete `VALIDATION/rag_llm/scores.csv` and `retrieval_metrics.csv`; then run `python -m app.ai.evaluation_rag_llm.summarize_scores` and `python -m app.ai.evaluation_rag_llm.summarize_retrieval`. Incomplete or invalid sheets are rejected.

No scores, agreement values, retrieval metrics, clean-install results, or browser-test results are claimed until their corresponding artifacts exist and have been reviewed. Unavailable checks are marked pending in the project audit report.
