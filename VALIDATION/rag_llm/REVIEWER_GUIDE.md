# RAG/LLM human reviewer worksheet guide

The saved run currently contains 30 generated-but-unscored cases. Do not treat system output, model self-critique, or another reviewer's ratings as a human score.

## Create/recreate worksheets

From `backend/`, for example:

```powershell
python -m app.ai.evaluation_rag_llm.prepare_review `
  --raw ..\VALIDATION\rag_llm\raw_run_20261019T101040519198Z.jsonl `
  --output-dir ..\VALIDATION\rag_llm\review_templates\run_20261019T101040519198Z
```

The tool validates all 30 unique successful cases and writes `scores.csv` and `retrieval_metrics.csv` with question, expected behavior, model/prompt identifiers, generated answer, and retrieved chunk content. Existing files are never overwritten unless explicitly requested. Each CSV contains one independent row per case for each reviewer role.

## Review

Assign one reviewer to each reviewer role. Both should inspect every answer and retrieved passage independently, using `backend/app/ai/evaluation_rag_llm/evaluation_rubric.py` anchors. Enter integer 1–5 on all five dimensions and explain notable/low ratings in comments. Retrieval worksheet: identify retrieved occurrence IDs relevant to the question and list the complete relevant retrieved set; use `NONE` only when that set is explicitly empty. Keep the raw run and completed worksheets associated with the same model digest/prompt hashes. Do not overwrite one reviewer's independent judgments during reconciliation.

## Summaries

Once completed, run from `backend/`:

```powershell
python -m app.ai.evaluation_rag_llm.summarize_scores `
  --scores ..\VALIDATION\rag_llm\review_templates\run_20261019T101040519198Z\scores.csv `
  --report ..\VALIDATION\rag_llm\REPORT.md
python -m app.ai.evaluation_rag_llm.summarize_retrieval `
  --input ..\VALIDATION\rag_llm\review_templates\run_20261019T101040519198Z\retrieval_metrics.csv `
  --report ..\VALIDATION\rag_llm\RETRIEVAL_REPORT.md `
  --scored-output ..\VALIDATION\rag_llm\retrieval_metrics_scored.csv
```

The generators refuse missing/invalid ratings or annotations. The score report includes per-dimension means, sample SD, exact agreement, Cohen's kappa, and per-case low-score/comment diagnostics. Retrieval report includes aggregate precision@k/coverage and per-case reviewer comparison. These metrics describe only the specific run and index snapshot; they are not clinical validation.
