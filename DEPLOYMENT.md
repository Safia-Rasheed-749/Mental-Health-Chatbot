# MindCare AI deployment notes (verification pending)

This is an operator checklist, not a declaration that the project is production-ready. Keep secrets out of source control; configure values in a secret manager or local ignored `.env` file. See `backend/.env.example` for variable names.

## Runtime prerequisites

- Python: use the version recorded in `VALIDATION/baseline/environment.json`; clean-install compatibility has not been demonstrated.
- PostgreSQL: install and provision a dedicated database/user. The client/server versions and restore procedure must be recorded per deployment.
- Ollama: install the service, then run `ollama pull llama3.2:3b` (current code default) or set `OLLAMA_MODEL` to an installed tag. Confirm with `ollama list`; the RAG preflight runner checks the exact tag.
- Install dependencies from backend and frontend requirement files in separate virtual environments where feasible. Current requirements are not fully pinned; `pip freeze` is an environment snapshot, not a lockfile that guarantees cross-platform reproducibility.
- Configure SMTP only if account email flows are enabled. Test recovery and OTP delivery with a non-production account.

## Environment and startup

1. Copy `backend/.env.example` to `backend/.env`; replace placeholders with deployment-specific secrets.
2. Do not use development JWT fallback secrets in production. Set a strong `JWT_SECRET_KEY` and rotate it through an approved procedure.
3. Start PostgreSQL and verify the configured schema/table initialization path. A formal migration/rollback system is not established by this audit.
4. Start Ollama and verify model availability.
5. Start FastAPI and confirm `/health`; note this endpoint is a process liveness check, not proof that PostgreSQL/Ollama are ready.
6. Start Streamlit with `API_URL` pointing at FastAPI.
7. Complete `VALIDATION/e2e/SMOKE_CHECKLIST.md` before accepting users.

## Security and operations still to verify

- TLS termination, secure CORS origins, rate limits, authentication/session expiry and secrets management.
- Database least privilege, backups, encrypted storage, restore rehearsal and data deletion from backups.
- Log retention/redaction, monitoring, incident response, SMTP recovery, and access reviews.
- Clean-machine installation, migrations, model download integrity and hardware capacity.

Until a second operator completes a clean install and restore test with dated evidence, classify deployment readiness as **not verified**. Present the application as a wellness-support prototype, not a clinical service.
