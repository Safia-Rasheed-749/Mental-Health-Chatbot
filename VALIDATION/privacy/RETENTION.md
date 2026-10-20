# Privacy, retention, and deletion review

## Current implementation evidence

- `backend/app/services/privacy.py` masks common email, phone, and Pakistan CNIC patterns. This is partial redaction, not de-identification; free text may contain other identifiers.
- Chat, journal, mood, account, activity and audio-related storage paths need a repository-wide retention/deletion review and live database verification.
- The sticky-chat voice control now requires an explicit, unchecked consent checkbox before requesting microphone access. Its visible disclosure says that audio is transcribed locally, transcript text is saved as chat history, optional TTS uses online speech services, and temporary audio files are deleted after processing. This is an implemented notice/guard, not a legal basis or verified retention guarantee.
- Voice audio is held in browser memory during recording, submitted to the Streamlit app only after stopping, converted/transcribed, and temporary WebM/WAV files are removed in a `finally` cleanup path. Transcribed text follows ordinary chat persistence/retention. Optional response audio is held in Streamlit session state for playback. External TTS provider retention/processing terms have not been independently verified.
- Crisis event logging is intended to store matched phrase labels rather than the full message. Application and third-party logs have not yet been audited for PII.

## Operational policy status

| Item | Status |
|---|---|
| Retention duration by data category | Not established; owner decision required |
| User data export | Not verified end-to-end |
| User deletion including backups/logs | Not verified end-to-end |
| Consent UI and server-side consent gate | Implemented; browser/device behavior still requires manual verification |
| Temporary upload cleanup path | Implemented in `frontend/ui/chat.py`; runtime failure-path verification pending |
| TTS provider retention, transcript deletion, session audio clearing | Not verified; owner/provider policy and live deletion tests required |
| Application log PII scan | Pending |
| Backup retention and restore deletion semantics | Pending |
| Encryption at rest/in transit in deployment | Pending deployment-specific verification |

Do not enter real patient/client information into this prototype until a documented policy, lawful basis, access controls, deletion path, and deployment security review are complete.
