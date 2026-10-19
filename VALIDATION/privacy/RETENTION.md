# Privacy, retention, and deletion review

## Current implementation evidence

- `backend/app/services/privacy.py` masks common email, phone, and Pakistan CNIC patterns. This is partial redaction, not de-identification; free text may contain other identifiers.
- Chat, journal, mood, account, activity and audio-related storage paths need a repository-wide retention/deletion review and live database verification.
- Crisis event logging is intended to store matched phrase labels rather than the full message. Application and third-party logs have not yet been audited for PII.

## Operational policy status

| Item | Status |
|---|---|
| Retention duration by data category | Not established; owner decision required |
| User data export | Not verified end-to-end |
| User deletion including backups/logs | Not verified end-to-end |
| Audio consent, temporary files, and retention | Not verified end-to-end |
| Application log PII scan | Pending |
| Backup retention and restore deletion semantics | Pending |
| Encryption at rest/in transit in deployment | Pending deployment-specific verification |

Do not enter real patient/client information into this prototype until a documented policy, lawful basis, access controls, deletion path, and deployment security review are complete.
