# MindCare AI — Project Status and Team Handoff

**Prepared:** September 26, 2026  
**Repository:** `https://github.com/Safia-Rasheed-749/Mental-Health-Chatbot`  
**Purpose:** One consolidated reference for work completed on September 25–26, remaining work, GitHub handoff, and local Windows setup.

> This report describes the current working tree and existing project reports. It is not a claim that all current edits have been committed, pushed, or visually verified in a browser.

---

## 1. Executive summary

The application has been moved toward a three-layer architecture:

```text
Streamlit UI → FastAPI REST API → PostgreSQL
                         └──────→ local AI/RAG/Ollama services
```

The frontend uses the API client for authentication and application data. The recent work also addressed login/reset error handling, local LLM response time, and multiple refinements to the chat page, sidebar, and sticky React input.

The local working tree contains many modified and untracked files. **The latest work is not yet available to teammates through GitHub unless it is reviewed, committed, and pushed.** Do not push the complete working tree blindly: it contains numerous unrelated or possibly pre-existing changes, generated evaluation files, notebooks, a `backend copy/` directory, and an untracked notebook-like file.

---

## 2. Work completed by date

### September 25, 2026 — Gap 1 integration (per `GAP1_INTEGRATION_REPORT.md`)

- Established the Streamlit → FastAPI → PostgreSQL data path.
- Added API-backed frontend functions in `frontend/api_client.py` and retained the legacy function interface in `frontend/db.py`.
- Added PostgreSQL connection pooling, environment-driven settings, auth routes, bearer-token security, and bcrypt password hashing with support for legacy SHA-256 password hashes.
- Added the incremental database migration `backend/schema.sql`, including conversation and password-reset tables/fields and supporting indexes/constraints.
- Added protected application routes for authentication, mood, journal, conversations, history, activity, and administrative reads.
- Added or integrated privacy redaction and model-signal display in chat.
- The Gap 1 report records a local end-to-end smoke test for registration, login, mood, journal, conversation, and message operations, plus API protection checks.

### September 26, 2026 — Login, reset, chat performance, and UI refinements

#### Login and password reset

- Added a `BackendUnavailableError` and readable frontend messaging when FastAPI cannot be reached.
- Made HTTP error detail extraction resilient to empty or non-JSON responses, avoiding a secondary `JSONDecodeError` when a request fails.
- Reproduced the password-reset HTTP 500: the backend virtual environment did not have `bcrypt` installed. Installed it locally and verified that bcrypt hashing works. The dependency is declared in `backend/requirements.txt`; fresh environments still need that requirements file installed.
- Added startup batch files: `start_backend.bat` and `start_frontend.bat`.

#### Backend and chat performance

- Deferred the RAG/chat-service import in `backend/app/api/chat_routes.py` until a chat request so unrelated API routes do not need to load the full AI stack at import time.
- Changed the local Ollama default to `llama3.2:1b` with a bounded generation length/context in `backend/app/ai/llm/llm.py`; `OLLAMA_MODEL` can override it.
- Added frontend handling for chat timeouts, connection errors, HTTP errors, and invalid responses.

#### Chat page and sticky input

- Removed the large blue chat header and added a compact status row and a lavender medical/wellness disclaimer.
- Refined the empty state and added starter actions for anxiety, breathing exercises, and mood tracking.
- Added a scrollable Streamlit message container and adjusted message row spacing/wrapping.
- Kept the React chat input component fixed to the bottom; refined its rounded input surface, microphone/send controls, and component height.
- Centered and restyled the high-stress breathing recommendation action.
- Added a bottom anchor and a `components.html` script/observer intended to scroll the actual Streamlit overflow element.
- Removed the simulated character-by-character answer display; responses now render as complete messages.
- Refined sidebar page selection, selected/hover states, compact spacing, branding, and recent-session title treatment.
- Rebuilt the React sticky-input production bundle with `npm run build` after its source changes.

Detailed prior notes remain in:

```text
GAP1_INTEGRATION_REPORT.md
LOGIN_ISSUE_REPORT.md
CHAT_UI_REFINEMENT_REPORT.md
TEAM_HANDOFF_REPORT.md
```

---

## 3. Current validation and known limitations

### Validation recorded

- Python syntax compilation passed for the recently edited chat/sidebar Python files.
- `git diff --check` passed for the recent chat/sidebar/component edits.
- The sticky React component production build passed with `npm run build`.
- Earlier Gap 1 documentation reports local API and data-flow smoke tests. Those results are historical and do not replace running the current test suite on a clean teammate setup.

### Not yet confirmed

- The latest chat UI has **not** been verified in an attached/connected browser. In particular, visually confirm the actual Streamlit DOM behavior for scroll-to-latest, the fixed input footer, sidebar radio state, and message spacing.
- No claim is made here that all automated tests pass on the current complete working tree.
- The repository state shown during preparation has many local changes. Their authorship and intended inclusion need review before staging.

### Assets and local services

The repository `.gitignore` excludes important local assets, including model files and generated vector-store data. A teammate may need the approved team copy of:

```text
backend/models/
backend/knowledge_base/pdfs/
backend/knowledge_base/vector_store/
```

Confirm exact required asset directories against the code and team storage. Do not commit large model/data assets or credentials without an explicit project decision. Chat also requires Ollama and the configured model to be available locally.

---

## 4. Remaining work

### Priority 1 — confirm current app behavior

1. Restart both backend and frontend from the current working tree.
2. Test login, signup, password reset, normal chat, long chat, crisis-safe behavior, navigation, and a stress-triggered exercise recommendation.
3. Confirm the newest assistant answer automatically appears at the bottom of the message viewport and the input remains fixed.
4. Confirm navigation selection stays in sync when entering pages from quick actions, recent chats, or other page buttons.
5. Inspect terminal logs for database, API, Ollama, model-loading, and email errors.

### Priority 2 — automate and harden

- Run and repair backend tests in `backend/tests/` and add automated API tests for authentication, reset, authorization, and conversation endpoints.
- Ensure `bcrypt` is installed by the normal backend dependency installation on a clean machine.
- Move signup verification and password-reset email/code behavior fully behind the backend. The current local/FYP reset flow may expose a reset code for development; do not deploy that behavior as production security.
- Verify password reset uses the latest unexpired code and handles database/API errors with actionable messages.
- Confirm the default JWT secret is overridden with a stable, strong per-environment secret for shared deployments.
- Document or automate the base PostgreSQL schema/bootstrap. `backend/schema.sql` is an incremental migration that expects the existing core tables such as `users`, `messages`, `mood`, and `journal`; it may not create the complete database from an empty PostgreSQL instance.
- Verify privacy, crisis-safety, and authorization behavior with tests; model outputs are wellness signals, not diagnoses.

### Priority 3 — packaging and team onboarding

- Add/verify safe, tracked environment examples for both backend and frontend. `backend/.env.example` exists; no `frontend/.env.example` was found during this report review.
- Check that `.env` and secrets are ignored, while intended `.env.example` files remain trackable.
- Add one supported setup method for missing model/vector-store assets and specify compatible Python, PostgreSQL, and Ollama versions.
- Visually QA responsive chat/sidebar layout after Streamlit upgrades; the styling uses Streamlit DOM selectors that can change across versions.

---

## 5. How teammates get the work from GitHub

### Important: current edits must be pushed first

The current Git status contains many modified and untracked files. Teammates only receive committed files that have been pushed to the shared branch.

Before pushing:

1. Review `git status` and `git diff`.
2. Determine which changes belong to this task and which are teammate/pre-existing work.
3. Stage only reviewed, intended files; do not use `git add .` without checking every listed file.
4. Do not commit `.env`, virtual environments, model files, local databases, secrets, or unintended generated evaluation artifacts.
5. Commit and push to the agreed branch; ask teammates to pull that branch.

Example review commands from the repository root:

```powershell
git status --short
git diff --check
git diff --stat
git diff -- frontend/ui/chat.py frontend/ui/sidebar.py frontend/api_client.py frontend/db.py
```

Only after an owner has reviewed and pushed the intended changes should teammates run:

```powershell
git clone https://github.com/Safia-Rasheed-749/Mental-Health-Chatbot.git
cd Mental-Health-Chatbot
git pull origin main
```

If the changes are pushed to another branch, use that branch instead of `main`.

---

## 6. Teammate setup on Windows (fresh clone)

### Prerequisites

- Git
- Python 3.10 (the backend project documentation specifies Python 3.10)
- PostgreSQL installed and running
- Node/npm only if rebuilding the sticky React component; teammates normally use the committed `dist/` bundle
- Ollama installed/running and model/assets available for full AI chat

### Step 1 — create virtual environments

From the repository root in PowerShell:

```powershell
py -3.10 -m venv venv
py -3.10 -m venv backend\venv
```

### Step 2 — install dependencies

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r frontend\requirements.txt
.\backend\venv\Scripts\python.exe -m pip install --upgrade pip
.\backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### Step 3 — create local environment files

Copy the backend example:

```powershell
Copy-Item backend\.env.example backend\.env
```

Edit `backend\.env` locally. Set at least:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fyp_chatbot
DB_USER=postgres
DB_PASSWORD=<your-local-postgres-password>
JWT_SECRET_KEY=<generate-a-long-random-secret>
ALLOW_LEGACY_SHA256=true
OLLAMA_MODEL=llama3.2:1b
```

Do not commit the resulting `backend\.env`.

The frontend defaults to `http://127.0.0.1:8000`. If the API is hosted elsewhere, set `API_URL` in the local environment before running Streamlit, for example:

```powershell
$env:API_URL="http://127.0.0.1:8000"
```

### Step 4 — prepare PostgreSQL

1. Start the PostgreSQL Windows service.
2. Create the `fyp_chatbot` database if it does not exist.
3. Ensure the project's **base schema** has been installed. The checked-in `backend/schema.sql` is an incremental migration and expects core user/message/mood/journal tables to exist.
4. Apply the project migration:

   ```powershell
   psql -U postgres -d fyp_chatbot -f backend\schema.sql
   ```

Use a local PostgreSQL password in `backend\.env`; never copy another developer's password from a report or chat.

### Step 5 — prepare AI assets and Ollama

Confirm access to the project's ignored local model and knowledge-base assets through the team's approved storage process. Then ensure Ollama is running and the configured model exists:

```powershell
ollama list
ollama pull llama3.2:1b
```

Large classifier model files and the FAISS vector store may be required in addition to the Ollama model. The clone alone may not contain these assets.

### Step 6 — run backend and frontend in separate terminals

**PowerShell window 1 — backend:**

```powershell
cd <path-to-cloned-repository>
.\backend\venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Wait for FastAPI's startup-complete message. Keep this window open.

**PowerShell window 2 — frontend:**

```powershell
cd <path-to-cloned-repository>
.\venv\Scripts\streamlit.exe run frontend\app.py
```

Open the Streamlit URL printed in the terminal, usually `http://localhost:8501`.

### Step 7 — smoke-test services and app

In another PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Then test account creation/login and the Dashboard. Test chat only after confirming Ollama, classifier model assets, and the vector store are available.

---

## 7. Optional: run the local startup batch files

From the repository root, the project includes:

```text
start_backend.bat
start_frontend.bat
```

Double-click `start_backend.bat` first and wait for the API to start. Then launch `start_frontend.bat`. Keep both windows open. The explicit PowerShell commands above are preferable for troubleshooting because they show errors directly.

---

## 8. Security and GitHub checklist

- Never commit `.env`, database passwords, JWT keys, SMTP credentials, user data, or access tokens.
- Do not put real secrets or personal account credentials in this report or GitHub issues.
- Check `git status --short` before staging. The current working tree has unrelated-looking changes and untracked content that needs owner review.
- Do not push virtual environments, `backend/models/`, local database dumps, or large generated assets without an explicit repository-storage plan.
- Ensure updated React `src/` changes have their matching rebuilt `dist/` assets committed if the Python component serves from `dist/` in release mode.
- Keep the backend process running while using Streamlit; both services are needed for API-backed auth and chat.
