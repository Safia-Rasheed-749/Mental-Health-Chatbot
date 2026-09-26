# Login Issue Report

## 1. Issue Summary

When the user enters valid login details and clicks **Sign In**, the page does not move to the Dashboard. The frontend reports:

```text
HTTPConnectionPool(host='127.0.0.1', port=8000):
Failed to establish a new connection
```

This means that the Streamlit frontend cannot reach the FastAPI backend at:

```text
http://127.0.0.1:8000
```

The error is not caused by an incorrect email or password.

---

## 2. Application Architecture

The application now uses three services:

```text
Streamlit Frontend → FastAPI Backend → PostgreSQL Database
```

The login request follows this path:

```text
Sign In button
    ↓
frontend/ui/auth.py
    ↓
frontend/db.py
    ↓
frontend/api_client.py
    ↓
POST http://127.0.0.1:8000/auth/login
    ↓
FastAPI authentication route
    ↓
PostgreSQL users table
```

The frontend and backend must both be running.

---

## 3. Root Cause

The frontend was running, but no FastAPI server was listening on port `8000`. Therefore, the login request was refused before the email and password could be checked.

The backend also loads AI and RAG components during startup. This can make startup take longer than one minute. The backend must be allowed to finish loading before the frontend is used.

---

## 4. Changes Implemented

### 4.1 Graceful backend connection error

Updated:

```text
frontend/api_client.py
```

Connection failures now raise a clear `BackendUnavailableError` instead of exposing a full traceback.

### 4.2 Login error handling

Updated:

```text
frontend/ui/auth.py
```

The Sign In button now:

- Redirects valid users to the Dashboard.
- Redirects administrators to the Admin Panel.
- Shows `Invalid email or password` for invalid credentials.
- Shows a backend startup instruction when FastAPI is unavailable.

### 4.3 Delayed AI loading

Updated:

```text
backend/app/api/chat_routes.py
```

The chat AI/RAG service is loaded when `/chat` is requested instead of blocking unrelated authentication startup.

### 4.4 Startup scripts

Added:

```text
start_backend.bat
start_frontend.bat
```

These scripts start the services using the project virtual environments.

---

## 5. Complete Startup Procedure

### Step 1: Start PostgreSQL

Open PowerShell and run:

```powershell
Get-Service postgresql-x64-15
```

The expected status is:

```text
Running
```

If PostgreSQL is stopped, open PowerShell as Administrator and run:

```powershell
Start-Service postgresql-x64-15
```

### Step 2: Open the project folder

```powershell
cd C:\Users\HP\Desktop\Mental-Health-Chatbot
```

### Step 3: Start FastAPI

Use a dedicated PowerShell window:

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Keep this terminal open.

Wait for:

```text
Application startup complete
```

The first startup can take time because the AI components are loaded.

### Step 4: Verify FastAPI

Open a second PowerShell window and run:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

The backend is working if the response contains:

```text
AI Mental Health Chatbot Backend Running Successfully!
```

### Step 5: Start Streamlit

In the second PowerShell window, run:

```powershell
cd C:\Users\HP\Desktop\Mental-Health-Chatbot
.\venv\Scripts\streamlit.exe run frontend\app.py
```

Open the Streamlit URL, normally:

```text
http://localhost:8501
```

### Step 6: Test login

1. Open the login page.
2. Enter an existing registered email.
3. Enter the correct password.
4. Click **Sign In**.
5. Confirm that the Dashboard opens.

Keep both terminals running while using the application.

---

## 6. Quick Startup Using Batch Files

From the project folder, double-click:

```text
start_backend.bat
```

Wait for the backend to finish starting. Then double-click:

```text
start_frontend.bat
```

The backend batch window must remain open.

---

## 7. Troubleshooting

### Chat request times out

Chat uses local Ollama inference in addition to the three classifier models. The default local configuration uses the lighter `llama3.2:1b` model with a bounded response length so it remains responsive on CPU. The model can be changed through `OLLAMA_MODEL` in `backend/.env`.

Ollama must be running and the model must be installed:

```powershell
ollama list
ollama pull llama3.2:1b
```

After changing the model configuration, restart FastAPI. The frontend now displays a readable timeout message instead of crashing Streamlit.

### Password reset returns `Internal Server Error`

Password reset and new account creation require the `bcrypt` package. Install it in the **backend** virtual environment, not only the frontend environment:

```powershell
.\backend\venv\Scripts\python.exe -m pip install bcrypt
```

Then stop and restart FastAPI so it loads the newly installed package:

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

The affected backend error is:

```text
RuntimeError: bcrypt is required for creating new passwords
```

This affects password reset and registration, but not login with an already stored password.

### Backend URL still refuses the connection

Check whether port `8000` is listening:

```powershell
Test-NetConnection 127.0.0.1 -Port 8000
```

Expected result:

```text
TcpTestSucceeded : True
```

If it is `False`, FastAPI has not started successfully. Read the error in the backend terminal.

### Database connection error

Check the values in:

```text
backend\.env
```

The database must exist and PostgreSQL must be running. If the database schema has not been applied, run:

```powershell
psql -U postgres -d fyp_chatbot -f backend\schema.sql
```

### Missing Python packages

Install backend packages:

```powershell
.\backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Install frontend packages:

```powershell
.\venv\Scripts\python.exe -m pip install -r frontend\requirements.txt
```

### Invalid credentials message

If the backend is reachable but login displays:

```text
Invalid email or password.
```

Then the request reached FastAPI successfully, but either:

- The account does not exist.
- The email is incorrect.
- The password is incorrect.

This is different from the `Connection refused` error.

### AI model loading messages

Messages such as the following are normal during startup:

```text
Loading Emotion Tokenizer...
Loading Stress Tokenizer...
Loading Depression Tokenizer...
Initializing RAG Chat Service...
```

Wait until:

```text
Application startup complete
```

---

## 8. Final Verification Checklist

- [ ] PostgreSQL service is running.
- [ ] FastAPI backend is running on port `8000`.
- [ ] `Invoke-RestMethod http://127.0.0.1:8000/` succeeds.
- [ ] Streamlit frontend is running on port `8501`.
- [ ] Both terminal windows remain open.
- [ ] The account exists in the database.
- [ ] Login redirects to the Dashboard or Admin Panel.

## 9. Expected Result

Once the backend and frontend are started in the correct order, valid login details will be accepted and the user will be redirected from the authentication page to the appropriate logged-in page.
