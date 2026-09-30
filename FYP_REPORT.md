# MindCare AI — Final Year Project Technical and Research Report

**Project:** MindCare AI — Multilingual AI-Powered Mental Health Support System  
**Report purpose:** Consolidated account of the base paper, project motivation, implementation, technologies, evaluation, completed work, limitations, and recommended next steps.  
**Prepared:** September 2026  
**Status:** Working FYP report; verify the exact final build, model assets, and evaluation runs before submission.

> **Evidence note.** This report distinguishes facts directly supported by the official base-paper abstract and this repository from details described in secondary full-text-derived material and from planned work. A feature existing in source code does not by itself prove that it has passed production-level validation.

---

## 1. Executive summary

MindCare AI is a web-based mental-wellness support platform. It combines a conversational interface with task-specific text classifiers, retrieval-augmented generation (RAG), language-aware response prompting, safety/privacy services, and account-backed wellness features. The current application is organized as a Streamlit frontend, a FastAPI REST backend, PostgreSQL persistence, local Hugging Face/PyTorch model inference, a local FAISS knowledge index, and Ollama-based language-model generation.

The research reference is **Mentalic Net (2025)**, a RAG-based conversational AI and evaluation framework for mental-health support. MindCare AI adopts the broad direction of evidence-grounded conversational support, but it does not claim to reproduce Mentalic Net, use its data, or improve its reported BERTScore. The project’s engineering contribution is its integration of independently trained task classifiers, English/Urdu/Roman Urdu interaction, a curated local retrieval pipeline, wellness modules, and an application/API/data architecture.

### Current evidence snapshot

| Component | Repository-backed status |
|---|---|
| Streamlit user interface | Implemented: public and authenticated pages, navigation, chat, dashboard, journal, mood, exercises, games, and history |
| FastAPI and PostgreSQL integration | Implemented: frontend requests use the REST client; backend exposes authentication, mood, journal, conversation/history and application routes |
| Production chat analysis | Emotion, stress, and depression model calls are integrated into the chat service |
| RAG and response generation | FAISS retrieval, top-4 context, prompt templates, and Ollama/LangChain generation are implemented |
| Language handling | Python-side language detection and English, Roman Urdu, and Urdu-script prompt paths are implemented |
| Safety/privacy | Crisis interception and sensitive-data redaction are present in the chat path; tests and operational review remain important |
| Model evaluation | Saved held-out test reports exist for multiple classifiers; these are task-specific results, not a single system score |
| RAG/LLM evaluation | Evaluation dataset, rubric, and runner exist; a saved result run has null/manual scores and an Ollama model-not-found error |
| Voice | UI-side microphone/audio capabilities and backend voice modules exist; do not represent a complete backend voice API as integrated without confirming the exact active route and end-to-end path |

---

## 2. Research base: Mentalic Net

### 2.1 Bibliographic record

**Title:** *Mentalic Net: Development of RAG-based Conversational AI and Evaluation Framework for Mental Health Support*  
**Authors:** Anandi Dutta, Shivani Mruthyunjaya, Jessica Saddington, and Kazi Sifatul Islam  
**arXiv:** 2509.04456, submitted 27 August 2025  
**Record:** [https://arxiv.org/abs/2509.04456](https://arxiv.org/abs/2509.04456)  
**DOI:** [https://doi.org/10.48550/arXiv.2509.04456](https://doi.org/10.48550/arXiv.2509.04456)  
**Publication note:** The arXiv record describes it as a preprint accepted in ISEMV 2025. Cite the publication venue and final bibliographic details according to the version required by the university.

### 2.2 What the official abstract establishes

The arXiv abstract directly states that Mentalic Net:

- is a mental-health support chatbot intended to **augment professional healthcare**;
- emphasizes safe and meaningful application;
- evaluates accuracy, empathy, trustworthiness, privacy, and bias;
- uses a **retrieval-augmented generation (RAG)** framework;
- integrates prompt engineering;
- fine-tunes a pretrained model on novel datasets; and
- reports a **BERTScore of 0.898**, with other evaluation metrics described as satisfactory.

The abstract advocates human-in-the-loop use and a long-term responsible development strategy. It does not, by itself, identify a specific pretrained transformer, dataset names, detailed model architecture, a 500-example test set, or a RAG recall value.

### 2.3 Additional details and source caution

The secondary full-text-derived summary supplied with the project brief reports more detailed elements, including vector retrieval, psychometric prediction, scales such as BDI-II/PHQ-9/CES-D/UCLA-8, a 500-sample evaluation, and RAG recall of 0.86. Treat these as **secondary-source details** until checked directly against the paper PDF and its methods/results sections. Do not cite the arXiv abstract as evidence for details it does not contain. Secondary source supplied: [ChatPaper full-text-derived page](https://chatpaper.com/pt/chatpaper/paper/186450).

For the FYP, the safe summary is: **Mentalic Net is a RAG-based conversational mental-health support system with prompt engineering, fine-tuning on research-developed datasets, multi-dimensional evaluation, and a reported BERTScore of 0.898.** Avoid assigning a specific model or dataset to it unless the full paper explicitly supports that statement.

### 2.4 Why it is a relevant base paper

Mentalic Net is relevant because it addresses the same broad problem domain: responsible, knowledge-grounded conversational AI for mental-health support. MindCare AI uses it as a **conceptual and architectural reference**, not as a source of code, trained weights, or datasets. RAG, prompt engineering, fine-tuning, and safety-oriented evaluation are established ideas in the reference work and are not claimed as inventions of this FYP.

---

## 3. Problem statement and objectives

People may need accessible, low-friction wellness support, but an AI system in this area must avoid presenting itself as a clinician or turning uncertain text predictions into diagnoses. A useful student project must therefore address both the user experience and the supporting technical system: model-based text analysis, relevant evidence retrieval, language-appropriate dialogue, privacy, crisis handling, persistence, and evaluation.

### Project objectives

1. Build a usable web application for conversational wellness support.
2. Analyze messages with separate emotion, stress, and depression text classifiers.
3. Ground factual mental-health responses with a local RAG knowledge pipeline.
4. Detect English, Urdu script, and Roman Urdu in Python and select suitable response prompts.
5. Add safety/privacy mechanisms and user-facing wellness tools.
6. Evaluate classifiers on held-out test data and document integration gaps honestly.

### Intended use boundary

MindCare AI is an **assistive wellness prototype**, not a diagnostic or treatment system, not a crisis hotline, and not a replacement for a licensed mental-health professional. Classifier outputs are model predictions/screening signals; they are not clinical diagnoses or calibrated clinical risk probabilities.

---

## 4. System architecture

```text
                       ┌─────────────────────────────┐
                       │ Streamlit web application   │
                       │ chat, dashboard, mood,       │
                       │ journal, exercises, history  │
                       └──────────────┬──────────────┘
                                      │ REST / JSON
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ FastAPI backend                                                  │
│ auth + app routes + chat API + privacy + crisis guardrail        │
└──────────┬───────────────────────┬──────────────────┬───────────┘
           │                       │                  │
           ▼                       ▼                  ▼
 PostgreSQL             Classifier services     RAG + generation
 users, messages,        emotion/stress/         embeddings → FAISS
 conversations, mood,   depression              → top-k context
 journal, activity                               → prompt → Ollama
```

### 4.1 Request flow for a normal chat message

Based on `backend/app/services/rag_chat_service.py` and the chat API:

1. The authenticated or demo client submits a message (and, for the supported chat request shape, optional conversation history).
2. Crisis text is checked before the ordinary response-generation path. A detected crisis is returned through a dedicated crisis response rather than proceeding to ordinary RAG/LLM generation.
3. Sensitive identifiers (email, phone number, Pakistani CNIC patterns) are redacted from the current message before the normal model/retrieval/generation path; application message-storage routes also redact content. Review history supplied by clients separately as part of privacy validation.
4. Emotion, stress, and depression predictors analyze the user message.
5. Python detects the input language and chooses an English, Roman Urdu, or Urdu-script prompt.
6. A FAISS retriever selects up to four relevant knowledge chunks (`TOP_K = 4`).
7. Retrieved context, classifier-derived mental-state cues, conversation history, and the current message are assembled for the prompt.
8. LangChain invokes the configured Ollama chat model (project reports use `llama3.2:1b` as the default; deployment must confirm the model is installed and configured).
9. The API returns the response and model signals; the frontend displays the response and prediction chips.

### 4.2 Persistence and service boundaries

The current target data path is **Streamlit → FastAPI → PostgreSQL**. `frontend/api_client.py` and `frontend/db.py` provide the frontend REST boundary while retaining repository-style function names used by UI modules. FastAPI routes enforce bearer-token authorization and derive user identity from token claims rather than trusting arbitrary user IDs in protected requests. PostgreSQL connection pooling and transaction helpers are in `backend/app/database/connection.py`.

---

## 5. What MindCare AI implements

### 5.1 User-facing platform

The Streamlit interface includes:

- public landing/about pages and a demo-chat route;
- authentication flows (registration/login and account recovery/verification support; production email/reset hardening remains a deployment concern);
- authenticated dashboard, AI chat, mood analytics, journal, chat history, and administration views;
- guided wellness exercises and calming games;
- mood logging and interactive Plotly analytics;
- structured journal entry fields (title, mood, date/time) and history cards;
- voice-related front-end interaction components where enabled by the page and installed dependencies.

The latest journal UI stores its title/mood/date/time alongside the journal text in the existing entry field, preserving compatibility with the existing API/data model. A future schema migration should create first-class metadata columns if querying/filtering by metadata becomes a requirement.

### 5.2 Classifier models and reported results

The repository’s model scope file (`backend/MODEL_SCOPE.md`) identifies DAIR-AI emotion, stress, and depression classifiers as the production classifiers. It explicitly says GoEmotions is experimental/evaluation-only and MELD is excluded from current production scope. The Reddit mental-health model has an evaluation artifact but should not be described as a live production chat classifier unless integration is separately verified.

| Task | Base model / dataset recorded in evaluation assets | Held-out evaluation in repository | Important interpretation |
|---|---|---|---|
| Emotion | `roberta-base`, DAIR-AI emotion; 6 labels: sadness, joy, love, anger, fear, surprise | 2,000 samples; accuracy **92.95%**, weighted F1 **92.84%**, macro F1 **88.68%** | General emotion classification; not diagnosis |
| Depression | `roberta-base`, Depression V2; binary | 1,148 samples; accuracy **98.00%**, binary F1 **97.94%** | Dataset-specific held-out result; not clinical screening validation |
| Stress | `roberta-base`, stress dataset; binary | 715 samples; accuracy **81.40%**, binary F1 **82.10%** | Lower than the other reported task scores; requires error and calibration analysis |
| Mental-health topic categories | Reddit mental-health model; independent test artifact | 125 samples; accuracy **85.60%**, weighted F1 **85.56%** | Evaluation result only; small test set and production integration not established by `MODEL_SCOPE.md` |
| Fine-grained emotion | GoEmotions, 28-label multilabel experiment | Evaluation files/notebook exist; experimental scope | Not connected to live chat; do not mix with the six-class production emotion score |

The metrics are **not directly comparable across tasks or datasets**. In particular, classifier accuracy/F1 must not be compared numerically with Mentalic Net’s response-generation BERTScore. High held-out scores do not establish clinical validity, generalization, calibration, or safety.

### 5.3 RAG and knowledge grounding

Implemented RAG building blocks in `backend/app/ai/rag/` include document loading, chunking, embedding generation, FAISS vector-store creation/loading, and retrieval. The evaluation/audit documents list sources such as CBT materials, DSM-5 material, psychotherapy references, WHO mental-health/stress resources, and CounselChat data. The reported embedding model is `sentence-transformers/all-MiniLM-L6-v2`; the chat service retrieves top four chunks by similarity.

RAG is used to supply supporting context to a generative model; it does not guarantee that the final response is correct, clinically appropriate, or fully supported. Source curation, licensing, chunk/source metadata, retrieval quality, and answer faithfulness need continued review.

### 5.4 Multilingual interaction

`backend/app/ai/llm/prompt.py` implements deterministic Python-side language detection:

- Urdu Unicode is detected from script ranges;
- Roman Urdu is detected using a word list and a token-hit ratio;
- English is the fallback.

The prompt module contains separate response instructions for English, Roman Urdu, and Urdu script. `roman_urdu_style.py` and `validator.py` provide vocabulary guidance and post-generation checks for language drift/forbidden terms, with a limited corrective regeneration path. This is a rule-based engineering approach; performance should be measured using a representative language test set, especially for code-switching and short messages.

### 5.5 Safety, privacy, and responsible use

- `crisis_detector.py` detects phrase patterns at high, medium, and low severity, including English and Roman Urdu patterns.
- `crisis_resources.py` builds language-sensitive crisis responses/resources.
- `rag_chat_service.py` checks for crisis before the ordinary generation flow and can bypass RAG/LLM for a detected event.
- Crisis event logging records matched phrases/severity/language rather than storing the full message (per its implementation comments and code path).
- `privacy.py` redacts email, phone, and CNIC-like patterns before normal model/storage use.
- The prompts instruct the language model not to diagnose or give medical advice and to encourage emergency/trusted-person support when self-harm is mentioned.
- UI/backend output should consistently say “model prediction” or “screening signal,” not diagnosis or clinical probability.

These controls reduce some risks but cannot guarantee crisis detection or prevent all privacy leakage. Pattern matching can miss indirect expressions and produce false positives; redaction is not complete de-identification. Human support and verified local emergency guidance remain essential.

### 5.6 Voice and user-support modules

The repository includes voice modules for speech-to-text/text-to-speech and front-end microphone/audio functionality. The backend application route registration does not establish that every voice module is exposed as a fully operational API workflow. For a report/demo, describe voice as **implemented in the codebase / partially integrated**, and verify a complete microphone → backend transcription → response → audio playback flow before claiming end-to-end completion.

Mood tracking, journaling, exercises/games, history, and account persistence turn the prototype into a broader wellness-support application rather than a chat-only demo. These are product/integration contributions, not evidence that the application provides therapy.

---

## 6. Methods and technologies used

| Layer | Technology / method | Role in this project |
|---|---|---|
| UI | Python, Streamlit, HTML/CSS, small React sticky-chat component | Web pages, forms, charts, navigation, chat experience |
| API | FastAPI, Pydantic, Uvicorn | JSON endpoints, request validation, authentication, application/chat services |
| Persistence | PostgreSQL, `psycopg2` connection pool, SQL schema/migrations | User accounts, messages, conversations, moods, journals, activity data |
| API security | Bearer/JWT-style signed tokens, bcrypt password hashing, legacy-hash migration support | Authenticated access and password storage |
| NLP training/inference | PyTorch, Hugging Face Transformers, `roberta-base` fine-tuning | Emotion, stress, depression, and experimental classifiers |
| RAG orchestration | LangChain components and `langchain-ollama` | Document pipeline, retriever-to-prompt-to-LLM request path |
| Embeddings | Sentence Transformers `all-MiniLM-L6-v2` | Convert document chunks and queries into vector representations |
| Vector retrieval | FAISS CPU index | Local similarity search over indexed knowledge chunks |
| Response generation | Ollama local runtime, configured Llama 3.2 model | Generate context-conditioned response; requires local model availability |
| Data/evaluation | Hugging Face datasets, scikit-learn, NumPy/Pandas, evaluation scripts | Dataset preparation, metrics, confusion matrices, confidence/error review |
| Interactive charts | Plotly in Mood Analytics | Vector-quality trend and distribution charts with hover behavior |
| Voice utilities | Whisper/STT, gTTS/TTS-related packages and UI recording tools | Voice interaction components; end-to-end status must be verified |
| Tests | pytest and focused backend tests | Privacy, crisis detection, language detection, API/security behavior |

### 6.1 Model development method

The documented model workflow is task-specific: prepare/labeled dataset → tokenize text with the pretrained transformer tokenizer → fine-tune a classification head/model using PyTorch/Hugging Face tooling → save model/tokenizer assets → run evaluation on a held-out test split → report accuracy, precision, recall, F1, and confusion matrix. The FYP should include the exact split method, random seed, preprocessing, hyperparameters, class distribution, and artifact hash/version for every final result; the report files alone do not establish all of those reproducibility details.

### 6.2 RAG construction method

The documented knowledge pipeline loads local PDF/web documents and CounselChat-derived documents, divides content into chunks (pipeline defaults: 500 characters with 100-character overlap), embeds chunks, creates/saves a FAISS vector index, then exposes a similarity retriever. The runtime requests top-k=4 chunks. The generator receives retrieved context, current query, language-specific system prompt, optional bounded conversation history, and uncertain classifier cues.

---

## 7. Base paper versus MindCare AI

| Dimension | Mentalic Net (official abstract) | MindCare AI (repository-backed implementation) |
|---|---|---|
| Main goal | Conversational mental-health support intended to augment professional healthcare | Multilingual wellness support application with chat plus user-facing wellness modules |
| Core response method | RAG, prompt engineering, pretrained model fine-tuning on novel datasets | Local FAISS RAG, prompt templates, Ollama generation, locally integrated classifiers |
| Named model details | Abstract says pretrained model; does not name a specific model | `roberta-base`-based task classifiers; configured local Llama 3.2 via Ollama for generation |
| Data | Abstract calls fine-tuning data “novel datasets”; specific identities need full-paper confirmation | Public/task-specific evaluation data recorded for DAIR-AI, Depression V2, Stress, Reddit; CounselChat and curated sources for retrieval; GoEmotions experimental |
| Language/localization | Not established by the abstract as English/Urdu/Roman Urdu support | Python language detection and prompt paths for English, Roman Urdu, and Urdu script |
| Safety/responsibility | Abstract explicitly emphasizes accuracy, empathy, trustworthiness, privacy, bias, and human-in-the-loop | Crisis interception/resources, privacy redaction, disclaimers/prompt safety rules, and privacy/crisis tests are present; broader validation is needed |
| User experience | Conversational support system | Streamlit platform with chat, mood, journal, dashboard, exercises/games, history, auth/admin, and voice-related components |
| Evaluation | Abstract reports BERTScore 0.898 and satisfactory other metrics | Task-specific classifier held-out results; RAG/LLM rubric evaluation is present but saved scores are incomplete |

### Accurate contribution statement

> **MindCare AI adapts the RAG-based mental-health conversational direction represented by Mentalic Net into a multilingual wellness-support platform, integrating task-specific transformer-based emotion, stress, and depression classifiers, a curated local retrieval pipeline, privacy/crisis-oriented processing, and user wellness modules. The project evaluates classifiers on task-specific held-out datasets and is continuing work on complete, reproducible evaluation of end-to-end generated responses.**

This phrasing does not claim to invent RAG, outperform Mentalic Net, use its private/novel datasets, or equate different evaluation metrics.

---

## 8. Work completed so far

### AI and research assets

- Fine-tuned and evaluated the DAIR-AI six-class emotion classifier.
- Fine-tuned and evaluated depression and stress classifiers.
- Produced a Reddit mental-health topic-classification independent-test report.
- Created a 28-label GoEmotions evaluation workflow; current model scope labels it experimental and not live.
- Saved test metrics, class reports, confusion matrices, training/evaluation materials, and confidence/error analysis artifacts in `backend/evaluation/`.
- Implemented language-specific prompting, Roman Urdu vocabulary checks, and a response-validation/regeneration component.

### Application and backend integration

- Built Streamlit public and authenticated UI pages and navigation.
- Established a FastAPI REST boundary between the frontend and PostgreSQL for application data.
- Added token-authenticated routes for auth, mood, journal, conversation/history, and activity functionality.
- Added PostgreSQL pooling, schema migration assets, and password-security helpers.
- Integrated the chat service with classifier calls, retrieval, prompt construction, local generation, bounded multi-turn history, crisis handling, and privacy redaction.
- Added interactive mood charts and journal metadata/history presentation.
- Added exercises/games and voice-related interfaces/utilities.
- Added focused tests and recorded integration/hand-off validation in project reports.

### Work from the current editing session

- Replaced static Mood Analytics plots with Plotly trend, donut distribution, and chat activity visualizations; standardized colors and corrected layout/ticks/legend.
- Reworked the Journal screen into Write Entry and Past Entries tabs, adding title, mood, date/time, counters, and structured history cards while keeping the current text storage API compatible.
- Added UTF-8 coding declarations to the 150 tracked Python files, removed encoding corruption in the touched Mood/Journal UI text, and added global spacing rules in `frontend/app.py`.

---

## 9. Evaluation results and interpretation

### Classifier results

The numbers in Section 5.2 are recorded in the project’s evaluation text artifacts. Present each result with its task, dataset, test sample count, metric definition, and split protocol. Avoid a single “overall model accuracy”: the classes, datasets, sample sizes, and tasks differ.

For interpretation, include macro and weighted metrics, class-level precision/recall, confusion matrices, and examples of errors. The stress classifier has a notably lower accuracy/F1 than depression and emotion in the current reports. The depression dataset result is very high and deserves checks for near-duplicate leakage, split contamination, label artifacts, and calibration before being framed as robust performance. The Reddit test has only 125 examples, so its estimate has substantial uncertainty.

### RAG and generated-response evaluation

The codebase includes a curated question set, a manual rubric with five dimensions (context relevance, faithfulness, response relevance, safety, helpfulness), and a runner that captures retrieved chunks and generated responses. However, one stored 30-question result file states that scores must be filled manually, contains null score values, and includes an Ollama `model not found` error in a generated response. This artifact is **not evidence of a completed RAG evaluation**. Re-run it with a verified model, complete human scoring using at least two reviewers if feasible, report the rubric and agreement, and include failure cases. Do not report a RAG recall or BERTScore for MindCare AI unless generated and validated by the project’s actual evaluation pipeline.

---

## 10. Known limitations and risk areas

1. **Clinical validity:** The classifiers are trained on general/social text datasets and do not establish clinical screening validity. User-facing probabilities must not be framed as diagnosis or actual clinical risk.
2. **Dataset/split validity:** Document dataset licenses, class balance, preprocessing, deduplication, split strategy, and leakage checks. Results can be inflated by duplicates or dataset-specific cues.
3. **Calibration:** High confidence can occur on wrong examples in the stored confidence analysis. Evaluate calibration (e.g., reliability diagrams, ECE/Brier score) and consider showing no user-facing confidence until validated.
4. **Stress model quality:** Current held-out stress accuracy is 81.40%, with 133 incorrect predictions out of 715. Analyze false negatives and false positives and describe the limitations.
5. **Small independent topic test:** The Reddit mental-health test contains 125 samples. Expand and diversify it before making broad claims.
6. **Language/code-switching:** Rule-based Roman Urdu detection may fail on short, spelling-variable, mixed English/Urdu, or regional input. Build a labeled multilingual test set.
7. **Generated-response evidence:** The saved RAG evaluation is incomplete and one run had a missing Ollama model. End-to-end quality/safety claims require a successful reproducible evaluation.
8. **Knowledge-source governance:** Verify source licensing, clinical currency, provenance, chunk traceability, and appropriateness. DSM-5 and other copyrighted documents require careful lawful use.
9. **Crisis detection:** Phrase matching can miss implicit risk, negation/context, slang, or new forms and can also false-trigger. It is not emergency monitoring. Validate language coverage and provide clear human/emergency escalation.
10. **Privacy/security:** Pattern redaction is incomplete. Review retention, encryption, authorization, logs, account recovery, reset-code delivery, admin protections, and secret management before any real-world deployment.
11. **Voice integration:** Confirm the whole audio path, consent, retention, language accuracy, and privacy before claiming complete voice support.
12. **Operational reproducibility:** Model weights, vector assets, PostgreSQL setup, Ollama availability, Python versions, and environment variables must be documented for a clean-machine deployment.

---

## 11. Recommended improvements and implementation roadmap

### Priority 1 — safety and truthful interaction

- Review crisis detector recall/precision by language with synthetic and expert-reviewed test cases; test negation, quotations, indirect expressions, and Roman Urdu variants.
- Maintain verified, region-specific emergency resources and date/version them.
- Ensure crisis responses provide supportive language and clear instructions to contact local emergency services/trusted people; ensure ordinary RAG does not bypass crisis handling.
- Keep model outputs hidden or carefully qualified; avoid presenting screening signals as diagnoses or calibrated probabilities.
- Complete privacy/data-retention review, especially logs, conversations, journals, audio, and account recovery.

### Priority 2 — reliable experimental evaluation

- Freeze versions and hashes for datasets, preprocessing, model weights, tokenizer, and test splits.
- Deduplicate before splits and prevent train/test contamination; report class distributions and random seeds.
- Add per-class metrics, confidence intervals, error analysis, calibration metrics, and subgroup/language-specific results.
- Re-run RAG evaluation with the configured local Ollama model present; score all rubric dimensions, record prompts/retrieved sources/model version, and use independent reviewers.
- Add generated-response evaluation for groundedness, helpfulness, empathy, safety, and language fidelity; do not optimize solely for BERTScore.
- Compare with simple baselines only on the same task and test split (e.g., majority class, TF-IDF + linear model, unfine-tuned transformer).

### Priority 3 — multilingual robustness and retrieval quality

- Create English, Urdu-script, Roman Urdu, and code-switched evaluation suites with spelling variants and short utterances.
- Measure language detection, response-language fidelity, Roman Urdu validator interventions, and human ratings separately.
- Add source metadata/citations to retrieved chunks and show references when appropriate.
- Review chunking, top-k, duplicate retrieved chunks, retrieval relevance, source coverage, and query rewriting; benchmark alternatives before making claims.

### Priority 4 — application engineering and product usability

- Complete a clean-machine setup guide with Python/PostgreSQL/Ollama versions, model download steps, environment examples, migrations, and startup checks.
- Add automated API tests for auth, user scoping, journal/mood persistence, conversations, crisis bypass, privacy redaction, and validation errors.
- Complete end-to-end browser tests for main workflows and responsive layouts.
- Decide whether journal metadata should move from the encoded text field into dedicated database columns for search, filtering, and export.
- Verify voice pipeline integration and document disabled/optional features accurately.
- Add accessibility checks, keyboard navigation, contrast review, loading/error states, and understandable empty states.

### Priority 5 — thesis and defense package

- Write a reproducible methodology chapter: dataset provenance, preprocessing, training parameters, compute, split strategy, metrics, software versions, and safety boundary.
- Write a results chapter separating classifier results from RAG generation evaluation.
- Include system architecture, sequence diagrams, schema/API design, screenshots, confusion matrices, ablation/baseline comparisons, and limitations.
- Prepare a live demo with normal chat, all supported language modes, mood/journal save-history, retrieval-backed factual query, and safe crisis-path behavior—using test accounts and non-sensitive inputs.
- Ensure all references are verified against primary sources and university citation style.

---

## 12. Suggested viva responses

### “What is your base paper?”

> Our research reference is Dutta et al., *Mentalic Net: Development of RAG-based Conversational AI and Evaluation Framework for Mental Health Support* (arXiv:2509.04456, 2025). Its abstract describes RAG, prompt engineering, fine-tuning a pretrained model on novel datasets, responsible evaluation, and reports BERTScore 0.898.

### “What did you take from it?”

> We adopted the direction of evidence-grounded conversational mental-health support and the need to evaluate safety and response quality. We do not claim to have invented RAG or reproduced the paper’s private/novel dataset.

### “What did your project add?”

> MindCare AI combines separate emotion, stress, and depression classifiers with a local RAG/LLM response path, English/Urdu/Roman Urdu prompting, crisis and privacy-oriented processing, and application features such as mood tracking, journaling, exercises, and persistent accounts.

### “Why are your accuracy results not compared to BERTScore 0.898?”

> They measure different tasks. Our accuracy and F1 values measure classifier predictions on labeled text. BERTScore measures semantic similarity of generated responses against references. They cannot be ranked against each other.

### “Did Mentalic Net use DAIR-AI or GoEmotions?”

> The official abstract says the authors fine-tuned a pretrained model on novel datasets but does not name those datasets. We use DAIR-AI and other task-specific datasets for our own reproducible experiments; we do not attribute them to Mentalic Net.

### “Is your depression model clinically accurate at 98%?”

> The 98% is the recorded accuracy on a particular 1,148-example held-out Depression V2 test set. It is not evidence of clinical validity or real-world diagnostic accuracy. We treat the model as an experimental text signal and report the dataset and limitations.

---

## 13. Suggested final abstract / project description

> **MindCare AI is a multilingual mental-wellness support prototype that integrates a Streamlit application, FastAPI services, PostgreSQL persistence, task-specific transformer classifiers, local retrieval-augmented response generation, and user wellness tools. Drawing on the RAG-based conversational direction of Mentalic Net, the system combines emotion, stress, and depression text analysis with FAISS retrieval over a curated mental-health knowledge collection and language-aware English, Urdu, and Roman Urdu prompting. It also provides account-backed chat, mood and journal features, exercises, and safety/privacy-oriented processing. Classifier performance is reported separately for each task and dataset; evaluation artifacts currently include emotion, depression, stress, and topic-classification test results. Full human-scored evaluation of generated responses remains a required next step. The prototype is intended to support wellness conversations and does not diagnose or replace professional care.**

---

## 14. References and repository evidence

### Research reference

1. Dutta, A., Mruthyunjaya, S., Saddington, J., & Islam, K. S. (2025). *Mentalic Net: Development of RAG-based Conversational AI and Evaluation Framework for Mental Health Support*. arXiv:2509.04456. [https://arxiv.org/abs/2509.04456](https://arxiv.org/abs/2509.04456). Use the final ISEMV citation details if required and verified from the proceedings.
2. Secondary full-text-derived overview supplied for project planning: [ChatPaper page](https://chatpaper.com/pt/chatpaper/paper/186450). Use only as a discovery aid; verify its detailed claims against the paper PDF before academic citation.

### Key project evidence

- `backend/MODEL_SCOPE.md` — production/experimental/excluded model scope.
- `backend/evaluation/dair_ai_emotion/emotion_metrics.txt` — emotion test metrics and class report.
- `backend/evaluation/depression_v2/depression_v2_metrics.txt` — depression test metrics.
- `backend/evaluation/stress_detection/stress_metrics.txt` — stress test metrics.
- `backend/evaluation/reddit_mental_health/reddit_independent_metrics.txt` — topic-classification independent-test metrics.
- `backend/app/services/rag_chat_service.py` — integrated chat processing, bounded history, retrieval/generation, crisis/privacy path.
- `backend/app/ai/rag/` — loaders, chunking, embeddings, FAISS, retriever, vector-store pipeline.
- `backend/app/ai/llm/prompt.py`, `roman_urdu_style.py`, `validator.py` — language prompts and language-style controls.
- `backend/app/services/crisis_detector.py`, `crisis_resources.py`, `privacy.py` — safety/privacy-oriented services.
- `backend/app/ai/evaluation_rag_llm/` — curated response-evaluation set, rubric, and runner; current saved result artifacts require completion.
- `GAP1_INTEGRATION_REPORT.md` and `TEAM_HANDOFF_REPORT.md` — API/database integration and historical validation notes.

---

## 15. Final positioning

**Base report:** Mentalic Net (2025).  
**Base approach adopted:** RAG-based, prompt-guided mental-health conversational support.  
**Classifier backbone:** task-specific fine-tuned `roberta-base` models as documented by evaluation artifacts.  
**MindCare AI contribution:** integration of task-specific analysis, multilingual/localized prompting, local evidence retrieval and generation, safety/privacy mechanisms, and wellness application modules.  
**Critical next academic task:** complete and document reproducible, human-reviewed evaluation of generated responses and end-to-end safety before making system-level effectiveness claims.
