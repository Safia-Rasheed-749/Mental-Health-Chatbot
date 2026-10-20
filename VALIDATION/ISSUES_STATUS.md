# MindCare AI — Resolved and Remaining Issues

**Status date:** 2026-10-20  
**Scope:** Repository evidence currently available. “Resolved” means the indicated implementation or artifact exists; it does not mean clinical or production validation.

## Resolved or materially improved

| Issue | Status | Evidence / boundary |
|---|---|---|
| RAG evaluation runner could silently produce unusable results when Ollama model was missing | **Improved** | `backend/app/ai/evaluation_rag_llm/run_evaluation.py` checks the configured model and captures raw, explicitly unscored runs. Current run is recorded in `VALIDATION/rag_llm/raw_run_20261019T101040519198Z.jsonl`. Human evaluation remains incomplete. |
| RAG summaries could be produced without complete human scoring | **Resolved in tooling** | `backend/app/ai/evaluation_rag_llm/summarize_scores.py` refuses incomplete reviewer sheets; retrieval labels are separately summarized. No completed reviewer scores or retrieval annotations exist yet. |
| No repeatable dataset audit artifact | **Improved** | `backend/scripts/audit_datasets.py` and its outputs report row counts, class balance, missing values, duplicates, and possible overlap. Dataset provenance/licenses and investigation of flagged overlap remain open. |
| Common PII patterns were not protected by regression checks | **Improved** | Privacy tests cover common email, phone, and CNIC patterns. This is not full de-identification, nor proof that logs/raw evaluation files are PII-free. |
| Crisis testing lacked an auditable small diagnostic matrix | **Improved** | `backend/tests/safety/crisis_matrix.json` and its evaluator provide a small measured set. The recorded set includes false-positive/false-negative cases; it is not comprehensive crisis detection. |
| Rozan helpline number was incorrect | **Corrected in code/documentation** | Correction and source-check record are noted in `workdone.md` and `VALIDATION/safety/HELPLINES.md`. Reconfirm live availability and authoritative source before deployment. |
| Missing written retention/deployment/smoke-test guidance | **Documentation added** | `VALIDATION/privacy/RETENTION.md`, `DEPLOYMENT.md`, and `VALIDATION/e2e/SMOKE_CHECKLIST.md` now provide guidance/checklists. Execution and verification are still pending. |
| Misleading project readiness claims | **Improved** | `PROJECT_AUDIT_REPORT.md` and this status report distinguish implemented components from evaluated outcomes and retain the wellness-prototype limitation. |
| RAG human-review worksheet preparation | **Tooling implemented** | `backend/app/ai/evaluation_rag_llm/prepare_review.py` validates complete 30-case runs and produces enriched human score/retrieval sheets. Generated example sheets: `VALIDATION/rag_llm/review_templates/run_20261019T101040519198Z/`. This does not complete human scoring. |
| RAG diagnostic summaries | **Tooling improved** | Score report includes per-case low-score/comment diagnostics with means, SD and agreement; retrieval report adds per-case reviewer comparisons. See `backend/app/ai/evaluation_rag_llm/summarize_scores.py` and `summarize_retrieval.py`. |
| Leakage-remediation data copy workflow | **Tooling implemented; sample generated** | `backend/scripts/create_deduplicated_splits.py` produced immutable-source copies and a row/removal/hash manifest at `VALIDATION/datasets/deduplicated/depression_v2/`. This is not retraining or validated accuracy. |
| Probability calibration/leakage-adjusted metric utility | **Implemented; input-dependent** | `backend/scripts/evaluate_leakage_adjusted.py` requires full class-probability vectors, filters exact/audited near-overlap rows and writes bootstrap CIs, Brier score and calibration bins. Existing saved prediction artifacts lack full probability vectors, so no fresh real-model Brier/calibration result is reported. |
| Structured dataset rights tracking | **Scaffold implemented** | `VALIDATION/datasets/PROVENANCE.csv` and `backend/scripts/check_dataset_provenance.py` define required license/source evidence and block incomplete rows. It intentionally does not grant or infer licenses. |
| Cross-user session access checks | **Regression coverage added; route behavior hardened** | `backend/tests/security/test_access_control.py` authenticates two users and checks read, add-message, rename, delete, history, mood, and journal isolation. Tests found message reads/rename/delete could return success for a foreign session; conversation ownership is now explicitly checked and returns 404. Current test uses an isolated in-memory DB adapter; run against PostgreSQL before claiming DB integration certification. |
| Probability-export retraining workflow | **Scaffold implemented; model run pending** | `backend/scripts/train_and_export_probabilities.py` trains from `train_deduplicated.csv`, `validation_deduplicated.csv`, and `test_deduplicated.csv`, saves a separate model and exports complete `prob_0...prob_n` columns. No new training run was executed; existing data/model availability, compute, and review still determine final metrics. |
| Expanded crisis diagnostic matrix | **Expanded and measured** | 20 curated cases cover direct/indirect/conditional expressions, negation, non-personal mentions, hyperbole, and ordinary distress. `backend/scripts/evaluate_crisis_matrix.py` generated `VALIDATION/safety/crisis_matrix_report.json`: 11 TP, 0 FP, 0 FN, 9 TN (precision/recall 1.0 on this small curated set only). Not comprehensive detection. |

## Remaining issues

1. **RAG/LLM quality and retrieval — OPEN (human review required):** enriched reviewer worksheets are generated in `VALIDATION/rag_llm/review_templates/run_20261019T101040519198Z/`; see `VALIDATION/rag_llm/REVIEWER_GUIDE.md`. The original root `scores.csv` remains 0/30 cases scored by both reviewers (0/60 rows scored); root retrieval relevance labels remain blank (0/60 rows). Consequently no reviewer agreement, retrieval precision/coverage, or RAG quality report can truthfully be produced. Two humans must independently review the same fixed run.
2. **Dataset provenance/classifier validity — PARTIALLY ADDRESSED, STILL OPEN:** deduplicated copies and a manifest were generated under `VALIDATION/datasets/deduplicated/depression_v2/`. The latest scoped audit (`VALIDATION/datasets/classifier_splits/DATASET_AUDIT.md`) records 1 exact depression test/train overlap, 3 stress test/train overlaps, and 4 high-similarity depression test/train candidates. Candidate recall is approximate; flagged rows still need review. No retraining was performed. Existing archived probability outputs lack full class-probability vectors; the new utility cannot produce real-model Brier/calibration until suitable predictions are exported. Dataset rights remain unverified; the new CSV/checker are a scaffold, not license confirmation. No source datasets were modified.
3. **Safety and privacy assurance:** the curated crisis matrix is now expanded and has measured precision/recall, but its 20 examples are not comprehensive. Audit logs/raw outputs for PII and verify deletion/export/audio handling and helplines.
4. **End-to-end and access control:** cross-user API regression tests pass against a deterministic in-memory adapter; repeat the auth/data-scoping matrix against a clean live PostgreSQL database and test frontend error/loading/empty states, browser/mobile flows, and accessibility.
5. **Classifier retraining/calibration:** the new generic retraining/export command is not yet run. Execute it on audited, licensed deduplicated splits, verify the exported probability vectors, and then run `evaluate_leakage_adjusted.py`. Existing archived metrics remain unchanged until then.
6. **Deployment readiness:** demonstrate clean-machine setup, migrations/health checks, secret and SMTP/recovery configuration, rate limiting/logging, and backup/restore. Documentation alone is not a passing deployment test.
7. **Voice:** full microphone-to-transcription-to-response-to-playback path, consent, and retention are not verified. Label as experimental/unverified unless tested.
8. **Baseline freeze:** no reviewed baseline tag/commit was made because the worktree had pre-existing changes. Create it only after reviewing the worktree and agreeing on the exact baseline.

## Requested issue resolution detail

### RAG/LLM quality and retrieval

**Resolved:** runtime preflight/raw capture, complete-score refusal, complete-retrieval-label refusal, score sheet, retrieval label sheet, and reporting scripts are present. **Not resolved:** the substantive two-independent-human-reviewer task. Current sheets are still blank. No metric or report will be fabricated. Complete by assigning two independent reviewers (roles are sufficient), having both score Q01–Q30 from the same raw run, then run:

```powershell
cd backend
python -m app.ai.evaluation_rag_llm.summarize_scores
python -m app.ai.evaluation_rag_llm.summarize_retrieval
```

The score tool should produce `VALIDATION/rag_llm/REPORT.md`; retrieval tool should produce `RETRIEVAL_REPORT.md` and `retrieval_metrics_scored.csv`. If scoring disagreements occur, preserve both original sheets and document rubric reconciliation rather than overwrite independent ratings.

### Dataset provenance and classifier validity

**Resolved:** repeatable dataset inventory/exact-overlap reporting, approximate near-duplicate candidate detection, archived prediction recalculation, bootstrap intervals, per-class metrics, and stress false-negative summaries are available. **Not resolved:** license confirmation requires authoritative upstream license/terms and attribution; near-duplicate flags require row-level review; clean deduplicated retraining and full probability-vector calibration require suitable training code/data/predictions, which are not present for all active classifiers. Do not call those findings clean or leakage-adjusted. See the scoped audit and classifier report cited above. Keep original splits immutable; create versioned deduplicated splits only after provenance and label review, then retrain/evaluate and record hashes.

### Voice pipeline update

The voice issue is **partially resolved**: explicit consent, visible processing disclosure, a backend consent gate, temporary-file cleanup, removal of transcript debug logging, and a manual device acceptance protocol have been added. Full mic → Whisper → LLM → TTS playback, provider retention, and failure-path behavior still need a real-device run. See `VALIDATION/voice/PIPELINE_VERIFICATION.md`; voice remains experimental/unverified until its checklist is completed.

## Two additional issues addressed in this remediation (not multilingual)

These are evidence/tooling improvements, not claims that the underlying system is fully validated.

1. **Model availability/version ambiguity:** the runner now preflights the configured Ollama tag and records the observed model identity/digest and runtime details with the run. Local evidence reports Ollama `0.40.6`, with `llama3.2:1b` and `llama3.2:3b` installed at capture time. This does not prove availability on another machine or quality of generated answers.
2. **Reproducibility/hash capture:** baseline tooling now captures runtime/Git state and SHA-256 manifests for relevant model/data artifacts. See `backend/scripts/capture_validation_baseline.py` and generated manifests under `artifacts/`. The repository baseline tag was intentionally not created; review of dirty/pre-existing work remains necessary.

## Verification boundary

`workdone.md` records 24 focused backend tests passing at the time of that note; `PROJECT_AUDIT_REPORT.md` records a later backend run of 41 passing tests on 2026-10-19. Neither is a clean-install, database-backed end-to-end, security certification, or clinical validation. Consult the reports and rerun the documented commands before relying on the counts.

For this update, the focused access-control, crisis matrix, and dataset-remediation tests passed **9 tests** (one Starlette TestClient deprecation warning); Python compilation and `git diff --check` passed. The crisis diagnostic result is recorded above. The generated depression split manifest records 5,355→5,354 training rows, 1,147→1,144 validation rows, and 1,148→1,144 test rows. This is dataset preparation only—no classifier was retrained and no new model score is asserted. The provenance checker is intentionally expected to fail while source/license evidence remains pending.

**Overall conclusion:** useful validation tooling and some archived sensitivity analyses exist, but human RAG review, license confirmation, investigation of flagged near/exact duplicates, clean leakage-adjusted retraining/calibration, comprehensive safety/privacy review, full end-to-end testing, and deployment demonstration remain open. Present MindCare AI as a wellness-support prototype, not a clinically validated or production-ready system.
