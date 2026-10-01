# MindCare AI — Project Audit Report

**Purpose:** Inventory what is implemented, what evidence exists, and what remains to be verified across the project modules.  
**Audit basis:** Repository source, model/evaluation artifacts, and project status documents available in this checkout.  
**Status:** Repository-level audit, not a clinical, security, or production certification. A feature in source code does not alone prove end-to-end operation.

## Executive summary

MindCare AI is a multilingual mental-wellness prototype with a Streamlit frontend, FastAPI backend, PostgreSQL persistence, transformer-based text classifiers, local FAISS retrieval, and Ollama-based response generation. The strongest completed evidence is the working module/code structure, saved classifier artifacts and held-out reports, and targeted tests for safety/privacy/language behavior. The main project-level gap is complete, reproducible end-to-end validation: in particular, human-scored RAG/LLM quality, clean deployment verification, and broader safety/security testing.

| Module | Current state | Audit assessment |
|---|---|---|
| Frontend | Streamlit pages, account flows, chat and wellness features | Implemented; verify each workflow against live API and responsive/accessibility behavior |
| API/backend | FastAPI routes/services, auth, application data, chat orchestration | Implemented; automated integration coverage remains incomplete |
| Classifier training | Emotion, stress, depression training/inference pipelines and saved models | Training/evaluation artifacts exist; reproducibility and external validity need work |
| RAG | Load, chunk, embed, index, retrieve; chat service consumes top-k context | Pipeline implemented; answer-quality evaluation incomplete |
| LLM | Ollama generation, language prompts, Roman Urdu validation | Integrated in source; runtime depends on locally available/configured model |
| Safety/privacy | Crisis interception, resources, redaction, tests | Controls present; not comprehensive protection or clinical crisis monitoring |
| Persistence/security | PostgreSQL schema/services, pooling, signed-token auth/password hashing | Implemented; deployment and security review still required |
| Voice | UI and backend STT/TTS modules/routes | Partially integrated; do not claim verified end-to-end voice without a full run |
| Testing/evaluation | Focused pytest tests, classifier reports, RAG runner/rubric | Useful foundation; full system evaluation not yet complete |

## 1. Frontend

**Implemented:** Streamlit app (`frontend/app.py`) with public landing/about/demo views and authenticated application views. UI modules cover chat, dashboard, mood analytics, journal, history, guided exercises, games, authentication, sidebar/navigation, and admin. Plotly is used for mood analytics. Journal entries display title, mood and date/time metadata while remaining compatible with the existing text-entry API. A wellness-summary PDF helper and a small React/Vite sticky-chat component are also present.

**Integration:** `frontend/api_client.py` provides the REST client and `frontend/db.py` preserves function interfaces used by UI modules while routing application persistence through the backend. The project notes say account-backed chat, mood, journal, and history are supported.

**Gaps / verification:** Confirm every page's save/read flows against a running backend and database; verify signup/reset email configuration (signup OTP delivery is still noted as frontend-side); install optional PDF dependency (`reportlab`); exercise mobile/responsive layouts, accessibility, empty/error/loading states, and the sticky-chat integration. Repository-level tests include navbar and DB-connection tests, but this does not establish comprehensive browser end-to-end coverage.

## 2. Backend and API

**Implemented:** FastAPI app (`backend/app/main.py`) and route modules for authentication, chat, mood, journal, voice, and general application functions. Services separate chat, auth, mood, journal, crisis, privacy, and RAG-chat responsibilities. Request/schema validation, bearer-token authorization, password hashing, PostgreSQL connection pooling, and database models/schema are present. Frontend/backend boundary is HTTP REST/JSON.

**Gaps / verification:** Run API integration tests with a clean PostgreSQL instance and validate authorization/user scoping on all protected routes. Confirm migrations and environment setup from a clean machine. Operational settings, secrets, SMTP, account recovery, logging, rate limiting/cache/session behavior, and production deployment configuration require explicit review. Existing reports document integration work, but historical validation notes should not be treated as proof of current production readiness.

## 3. Model training and inference

### Production-scoped classifiers

The project records DAIR-AI emotion, stress, and depression models as the active classifier scope. Training/preprocessing/dataset/prediction modules exist under `backend/app/ai/`; model weights and tokenizer/config files are present. The chat service invokes emotion, stress, and depression analysis.

| Task | Recorded held-out result | Audit interpretation |
|---|---|---|
| Emotion (RoBERTa, six labels) | 2,000 examples; accuracy 92.95%, weighted F1 92.84%, macro F1 88.68% | General emotion classification only; not a diagnosis |
| Depression (binary) | 1,148 examples; accuracy 98.00%, F1 97.94% | Result on the recorded dataset split; not clinical validation; high score merits leakage/duplicate checks |
| Stress (binary) | 715 examples; accuracy 81.40%, F1 82.10% | Materially weaker than other reported scores; analyze false negatives/positives |

### Experimental or evaluation-only work

- Reddit mental-health topic classification has an independent evaluation artifact (125 examples; accuracy 85.60%, weighted F1 85.56%). It is not established as a production chat classifier.
- GoEmotions 28-label multilabel experiment and evaluation workflow are present; project scope explicitly treats it as experimental and not connected to live chat.
- MELD is explicitly out of scope.
- Training/evaluation notebooks and scripts also cover emotion, depression, stress and related dataset experiments.

**Gaps / verification:** Report dataset provenance/licensing, class balance, preprocessing, exact train/validation/test protocol, random seeds, hyperparameters, package versions, and model hashes. Perform deduplication/leakage checks, calibration and confidence analysis, confidence intervals, per-class error analysis, and external/multilingual testing. Metrics are task- and dataset-specific and must not be combined into one system accuracy or compared with generation metrics such as BERTScore.

## 4. RAG / knowledge retrieval

**Implemented:** `backend/app/ai/rag/` contains document loading, chunking, embedding, vector-store creation/loading, and retrieval components. Project documentation records Sentence Transformers `all-MiniLM-L6-v2`, FAISS, chunking defaults of 500 characters with 100-character overlap, and retrieval of up to four chunks. Knowledge sources are described as curated mental-health material, including WHO/APA/Mayo Clinic-type resources and CounselChat-derived content. The chat service inserts retrieved context into generation prompts.

**Evaluation status:** A 30-case question set, evaluation runner, and five-dimension human rubric exist (context relevance, faithfulness, response relevance, safety, helpfulness). Existing saved output has null/manual score fields and includes a model-not-found error. This is a prepared evaluation workflow, **not a completed successful RAG quality evaluation**.

**Gaps:** Re-run with the configured Ollama model installed, score all cases (preferably independent reviewers), document agreement and failure examples, measure retrieval relevance/coverage, and retain source metadata/citations. Check source licensing, currency, provenance, chunk traceability, and duplicates. No project RAG recall or generated-answer score should be claimed from the incomplete run.

## 5. LLM, prompts, and multilingual behavior

**Implemented:** LangChain/Ollama generation is integrated in the chat path. The configured default is documented as `llama3.2:1b`, which must be present in the local Ollama runtime. Prompt templates provide English, Roman Urdu, and Urdu-script response paths. Python-side language detection uses Urdu script ranges and Roman Urdu word/token heuristics, with English fallback. Roman Urdu style guidance and response validation can detect some language drift/forbidden terms and trigger a limited corrective generation.

**Gaps:** Confirm the actual configured model and runtime on the deployment machine. Evaluate language detection and response-language fidelity across short text, spelling variants, code-switching, and Urdu script. Validate generation for groundedness, helpfulness, safety, empathy and language fidelity using a completed human-reviewed evaluation. Prompt instructions and retrieval do not guarantee truthful or clinically appropriate output.

## 6. Safety, privacy, and responsible use

**Implemented:** Crisis phrase detection and language-sensitive response/resource helpers; crisis path is checked before ordinary RAG/LLM generation. Sensitive email, phone and CNIC-like patterns are redacted in relevant message-processing/storage paths. Prompts include non-diagnosis and safety guidance. Project notes record privacy/crisis/language/API-security tests and a persistent wellness disclaimer.

**Limitations:** Phrase matching can miss indirect or novel expressions and can false-trigger; redaction is not full de-identification. Crisis handling is not emergency monitoring or a hotline. Verify local helpline information against authoritative sources. Review client-supplied history, logs, retention, audio, encryption, authorization, admin controls, account recovery, and secrets before real-world use. Use model predictions as non-clinical signals only.

## 7. Persistence, data, and wellness features

**Implemented:** PostgreSQL schema/models/services support account and application data including conversations/messages, moods, journals and activity. Pooling and transaction helpers are present. UI includes mood tracking/analytics, journal, history, dashboard, exercises and games. Current journal metadata is encoded alongside text for compatibility rather than represented as dedicated queryable columns.

**Gaps:** Validate retention/deletion/export behavior and per-user access boundaries. Consider dedicated journal metadata columns if filtering/searching becomes necessary. Test backup/restore and schema migration procedures. Do not represent wellness activities as treatment or therapy.

## 8. Voice

Voice-related UI/audio files and backend STT/TTS/Whisper modules/routes exist. This supports describing voice as present in the codebase or partially integrated. The available project evidence does not establish a reliable complete microphone → backend transcription → response → audio playback workflow. Verify route registration, installed model/dependencies, language behavior, consent, retention and privacy before describing it as complete.

## 9. Test and delivery evidence

Focused tests cover crisis detection, language detection, privacy, API security, chat service and selected frontend/database behavior. A project status note records a prior validation run with Python compilation passing and five automated tests passing. These are point-in-time notes, not a fresh test run for this audit. The repository has startup scripts for frontend/backend, requirements files, Docker Compose, model assets and setup notes; a clean-machine, repeatable installation and full end-to-end smoke test remain necessary.

## 10. Prioritized remaining work

1. **Finish RAG/LLM evaluation:** ensure Ollama model availability; run the 30 cases; human-score every rubric dimension; document reviewers, method, failures and model/prompt versions.
2. **Reproducibility:** freeze dataset/model versions and hashes; document splits, preprocessing, seeds and hyperparameters; audit duplicates/leakage and calibrate classifiers.
3. **Safety and privacy validation:** test crisis language/negation/code-switching; validate local resources; inspect history, logs, retention, user scoping and secret handling.
4. **End-to-end application testing:** clean database setup, auth, chat, mood/journal persistence, history, errors, and browser/mobile workflows.
5. **Deployment readiness:** document Python/PostgreSQL/Ollama versions, model downloads, environment variables, migrations, optional dependencies, startup checks and backup/restore.
6. **Voice and UX claims:** run the whole audio workflow if it is to be presented as complete; test accessibility and responsive behavior.

## Overall conclusion

The project has progressed beyond a UI mock-up: it contains integrated application, API, persistence, classifier, retrieval, generation, and safety-oriented components. Classifier training and task-specific held-out evaluation are evidenced by saved models and reports. The frontend includes multiple account-backed wellness features. However, the RAG/LLM quality evaluation is not complete, deployment/end-to-end behavior needs current verification, and neither classifier results nor safety mechanisms establish clinical effectiveness. Present the system as a wellness-support prototype and clearly separate implemented features from experimentally validated outcomes.

## Key repository evidence

- `FYP_REPORT.md` — detailed project architecture, metrics, limitations, and audit cautions.
- `REMAINING_GAPS_STATUS.md` — recent model-scope decisions and outstanding operational work.
- `backend/MODEL_SCOPE.md` — production/experimental/excluded classifiers.
- `backend/app/services/rag_chat_service.py` — integrated chat flow.
- `backend/app/ai/rag/` — RAG pipeline.
- `backend/app/ai/llm/` — Ollama, prompts, language validation.
- `backend/app/ai/evaluation_rag_llm/` — generation evaluation dataset, rubric and runner.
- `backend/app/services/crisis_detector.py`, `crisis_resources.py`, `privacy.py` — safety/privacy components.
- `frontend/app.py`, `frontend/ui/`, `frontend/api_client.py` — UI pages and API integration.
