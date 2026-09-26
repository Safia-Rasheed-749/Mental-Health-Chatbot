@echo off
cd /d "%~dp0"
if exist "backend\venv\Scripts\python.exe" (
    "backend\venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
) else (
    python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
)
pause
