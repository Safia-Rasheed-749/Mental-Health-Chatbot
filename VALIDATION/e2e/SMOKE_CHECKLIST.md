# Manual end-to-end smoke checklist

Record date, app commit, tester role (not personal name), browser/device, API/database versions, and attach screenshots/log excerpts with PII removed. Do not mark a workflow passed based only on a page rendering.

| Flow | Steps | Evidence to capture | Result |
|---|---|---|---|
| Clean startup | Start PostgreSQL, Ollama, FastAPI, Streamlit from documented setup | Startup logs, `/health`, DB connection and model preflight | NOT RUN |
| Signup/login | Create test account, sign in, sign out, re-authenticate | API status and redacted browser capture | NOT RUN |
| User isolation | Create users A and B; attempt B's mood/journal/conversation IDs using A's token | Expected denied status for every endpoint | NOT RUN |
| Chat | Text turn, history follow-up, crisis phrase, model unavailable, backend unavailable | API payload/status; safe UI errors; no model/debug leakage | NOT RUN |
| Mood | Save mood, reload, read history, test another user | Saved record and access boundary | NOT RUN |
| Journal | Save text/metadata, reload/read, test another user | Persistence and access boundary | NOT RUN |
| Conversation history | Create multiple turns, reload, switch conversation | Correct ordered, scoped history | NOT RUN |
| Account recovery | Request and complete reset using configured SMTP | Redacted delivery evidence and token expiry | NOT RUN |
| Voice (if claimed) | Consent → microphone → transcription → response → audio playback → temp-file cleanup | Device/browser/audio evidence and retention check | NOT RUN |
| Responsive/accessibility | Mobile viewport, keyboard-only, screen reader/axe or Lighthouse | Findings and screenshots | NOT RUN |
| Empty/error states | Empty database, stopped API, stopped DB, missing Ollama tag | User-visible states; no traceback or secret leakage | NOT RUN |

This checklist is a template; the repository has not passed these checks until results are recorded here and dated.
