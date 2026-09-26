# MindCare AI — Team Handoff Report

## Current architecture

```text
Streamlit Frontend → FastAPI REST API → PostgreSQL
                                      └→ AI/RAG/LLM services
```

The Streamlit frontend no longer opens PostgreSQL connections directly.
Authentication, mood, journal, conversations, history, and activity requests
now pass through FastAPI.

## Main work completed

### Backend and database

- Added environment configuration in `backend/app/core/config.py`.
- Added a thread-safe PostgreSQL connection pool.
- Added JWT authentication and bcrypt password hashing.
- Added legacy SHA-256 verification with automatic bcrypt migration.
- Added authentication, mood, journal, conversation, history, and activity
  API routes.
- Added user-scoped authorization: users can access their own records;
  administrators can access selected users' records.
- Added `backend/schema.sql`.
- Created/migrated `conversations`, `password_reset_tokens`,
  `email_verification_codes`, and `messages.conversation_id`.

### Frontend architecture

- Added `frontend/api_client.py`.
- Replaced direct SQL behavior in `frontend/db.py` with REST calls while
  preserving existing UI function names.
- Fixed the dashboard 403 error caused by normal users calling admin routes.
- Added timestamp normalization for REST ISO strings in the dashboard.

### Chat and safety

- Added emotion, stress, and depression prediction chips.
- Added multi-turn context support.
- Added privacy redaction for emails, phone numbers, and CNIC values.
- Added compact wellness disclaimer.
- Added session model-signal trajectory chart.
- Added high-stress breathing-exercise recommendation.
- Fixed the breathing-exercise button to open the authenticated Exercises page.
- Added extra bottom spacing and automatic scroll-to-latest-message behavior so
  the fixed chat input does not hide messages.

### Frontend visual refinement

- Centralized widget styling in `frontend/layout_utils.py`.
- Improved cards, buttons, metrics, inputs, alerts, charts, tables, spacing,
  focus states, sidebar styling, and responsive behavior.
- Fixed invalid navbar/sidebar CSS.
- Added authenticated `Exercises` and `History` navigation.
- Added a privacy-conscious wellness PDF generator utility. The dashboard
  action was intentionally removed from the main dashboard to keep the
  wellness overview focused; it can be placed later on Mood Analytics or a
  dedicated Reports page.

### Model scope

- DAIR-AI emotion, stress, and depression remain production models.
- GoEmotions is experimental/evaluation-only and is not connected to the
  frontend or live chat.
- MELD is excluded from the current project scope.
- Rewrote `backend/notebooks/05_goemotions_evaluation.ipynb` to match the
  improved 28-label multi-label model, sigmoid output, and threshold `0.30`.

## Validation completed

```text
Frontend/backend syntax: PASS
API protected-route test: PASS
Privacy/crisis/language tests: PASS
GoEmotions notebook JSON: PASS
PDF generation: PASS
git diff --check: PASS
```

## Important: local files are not pushed

These files are intentionally ignored and must be created separately by each
teammate:

```text
backend/.env
frontend/.env
```

Never commit database passwords, SMTP passwords, JWT secrets, or model API
secrets.

## Teammate setup after `git pull`

### 1. Pull changes

```powershell
git pull origin main
```

### 2. Install dependencies

```powershell
python -m pip install -r backend\requirements.txt
python -m pip install -r frontend\requirements.txt
```

### 3. Create environment files

```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

Set the real PostgreSQL values in `backend\.env`:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fyp_chatbot
DB_USER=postgres
DB_PASSWORD=your_password
JWT_SECRET_KEY=your_generated_secret
ALLOW_LEGACY_SHA256=true
```

Set this in `frontend\.env`:

```text
API_URL=http://127.0.0.1:8000
APP_URL=http://localhost:8501
```

### 4. Apply the database migration

Create the `fyp_chatbot` database if necessary, then run:

```powershell
psql -U postgres -d fyp_chatbot -f backend\schema.sql
```

The database migration is not performed by GitHub; every local database needs
the schema migration.

### 5. Confirm large project assets

Teammates must also have access to the model and knowledge-base assets if they
are excluded from Git because of size:

```text
backend/models/
backend/datasets/
backend/knowledge_base/pdfs/
backend/knowledge_base/vector_store/
```

### 6. Start the services

Terminal 1:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
streamlit run frontend\app.py
```

### 7. Verify the application

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Then test login, dashboard loading, mood creation, journal creation, chat,
history, and the breathing-exercise button.

## Git workflow

Before committing:

```powershell
git status
git diff --check
git diff --stat
```

Stage only the intended source, schema, tests, notebook, requirements, and
documentation files. Do not stage `.env`, virtual environments, generated
model files, unrelated teammate changes, or credentials.

After backend changes, restart FastAPI. After frontend changes, restart
Streamlit if hot reload does not refresh the page.
