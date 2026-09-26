# MindCare AI — Gap 1 Integration Report

**Status:** Implemented
**Date:** 25 September 2026

## Objective

Remove direct PostgreSQL access from Streamlit and establish the target
architecture:

```text
Streamlit frontend → FastAPI REST API → PostgreSQL
                                  └──→ AI/RAG services
```

## What was integrated

### Backend foundation

- Added environment-driven settings in `backend/app/core/config.py`.
- Added a thread-safe `psycopg2.pool.ThreadedConnectionPool` in
  `backend/app/database/connection.py`.
- Added a transaction-safe `db_cursor()` context manager with automatic
  commit, rollback, cursor close, and connection return.
- Added password and token security helpers in
  `backend/app/core/security.py`:
  - bcrypt for new passwords;
  - legacy SHA-256 verification for existing accounts;
  - automatic bcrypt rehash after a successful legacy login;
  - signed HMAC-SHA256 bearer tokens with expiry.

### Database migration

`backend/schema.sql` was applied to the running `fyp_chatbot` PostgreSQL
database. It added:

- `conversations`;
- `messages.conversation_id`;
- `password_reset_tokens`;
- `email_verification_codes`;
- indexes for user, conversation, mood, and journal queries;
- cascading user cleanup for application records.

The original live database contained only `users`, `messages`, `mood`,
`journal`, and `user_activity`. The missing conversation and reset-token
tables were therefore created as part of this implementation.

### FastAPI routes

Registered in `backend/app/main.py`:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/user`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST/GET /mood`
- `POST/GET /journal`
- conversation creation, listing, rename, deletion, and messages
- authenticated history and activity routes
- admin-protected read routes

All protected routes use the bearer token and derive the user identity from
the token instead of trusting a frontend-supplied user ID.

### Frontend integration

- Added `frontend/api_client.py` for authenticated HTTP requests.
- Replaced the 912-line direct database implementation in `frontend/db.py`
  with a compatibility repository whose existing function names remain
  available to the UI.
- Existing pages (`auth`, `mood`, `journal`, `dashboard`, `history`,
  `sidebar`, `admin`, and `chat`) therefore continue using their existing
  function calls while persistence now crosses the REST boundary.
- Removed direct `psycopg2` access and hardcoded PostgreSQL credentials from
  the frontend runtime.
- Updated `frontend/test_db_connection.py` to test FastAPI availability
  instead of opening a database connection directly.
- Replaced the hardcoded FFmpeg path with `FFMPEG_PATH`, `FFPROBE_PATH`,
  `FFMPEG_DIR`, or system discovery through `shutil.which()`.
- Chat now reads the API's classifier fields and displays emotion, stress,
  and depression **model prediction** chips below assistant messages.

## Validation performed

1. Applied `backend/schema.sql` successfully with PostgreSQL 15.
2. Started the FastAPI application and confirmed `GET /` responds.
3. Confirmed unauthenticated `GET /mood` returns `401`.
4. Completed an end-to-end temporary-user test:
   - register;
   - login and receive bearer token;
   - create mood;
   - create journal entry;
   - create conversation;
   - save conversation message;
   - remove the temporary test data.
5. Python compilation was run for `backend/app` and `frontend`.
6. `git diff --check` reported no whitespace errors.

## How to run

### Backend

From the repository root:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

### Frontend

In another terminal:

```powershell
streamlit run frontend/app.py
```

`frontend/api_client.py` defaults to `http://127.0.0.1:8000`. Override it
with `API_URL` when deploying elsewhere.

## Important operational notes

- Install backend dependencies before deployment:

  ```powershell
  python -m pip install -r backend/requirements.txt
  ```

- `backend/.env` contains the local PostgreSQL password and generated JWT
  secret and is ignored by Git. It must exist on each machine.
- The API process must be restarted after backend code changes because the
  launch command does not use `--reload`.
- The current forgot-password route returns the reset code for local FYP
  testing. Before production, replace that response with backend SMTP email
  delivery and never return the code in JSON.
- The classifier chips are screening/model outputs, not clinical diagnoses.

## Remaining follow-up

- Move signup OTP generation and delivery fully into the backend.
- Add automated API tests using `FastAPI.TestClient`.
- Create/secure a dedicated administrator account before demonstrating the
  admin panel.
- Remove or update any unrelated pre-existing working-tree changes before
  committing this integration.
