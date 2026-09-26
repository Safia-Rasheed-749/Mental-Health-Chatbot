# MindCare AI — Remaining Gaps Resolution Status

## Model-scope decision

- DAIR-AI emotion, stress, and depression models remain the production models.
- GoEmotions is explicitly experimental/evaluation-only and is not connected
  to the frontend or live chat endpoint.
- MELD is explicitly out of scope. No MELD runtime module will be added.

## Resolved in this pass

- Added privacy redaction for email addresses, phone numbers, and CNICs before
  normal model processing and before application message/activity storage.
- Added a persistent chat wellness disclaimer.
- Added session model-signal trajectory chart.
- Added high-stress breathing-exercise recommendation.
- Added privacy-conscious wellness-summary PDF export.
- Added API, crisis, privacy, and language-detection tests.
- Added a reproducible RAG evaluation runner that exports all 30 cases and
  leaves the five rubric scores for transparent human review.
- Rewrote the empty GoEmotions notebook for the actual improved artifact:
  `goemotions_roberta_improved`, 28 named labels, multi-label sigmoid output,
  and threshold `0.30`.

## Validation

```text
Notebook JSON validation: PASS (8 cells)
Python compilation: PASS
Automated tests: 5 passed
Git diff check: PASS
```

## Remaining operational work

- Install `reportlab` before using PDF export:
  `pip install -r frontend/requirements.txt`.
- Run the RAG evaluation runner from `backend` and manually score the output
  using `evaluation_rubric.py`:
  `python -m app.ai.evaluation_rag_llm.run_evaluation`.
- Configure backend SMTP and move signup OTP generation/delivery fully into
  FastAPI before production. The current UI still sends signup email through
  its existing helper.
- Verify crisis helpline numbers with authoritative local sources before the
  defense.
