# Baseline snapshot — Issue 0

**Captured:** 2026-10-19  
**Purpose:** Record the repository revision and available local environment before further remediation.

## Repository state

- Current branch at capture: `main`
- `HEAD`: `63af4671f1fcb4ce1a51de3839feceaa3e596b16`
- Intended tag: `baseline-pre-fix-20261019` — **not created**
- Worktree: **dirty**. It contains modified, deleted, and untracked files, including unrelated frontend, classifier, and backend work.
- No commit or push was performed. Creating a commit/tag now would include changes without confirmed ownership and scope.

This is a record of the existing `HEAD`, not a frozen clean baseline. To complete the requested tagged baseline, the owner must review and explicitly approve which existing changes belong in the snapshot, then commit/tag that reviewed state.

## Local environment observed

- Python: `3.10.9`
- PostgreSQL client (`psql`): unavailable on `PATH`; PostgreSQL server version/status not verified.
- Ollama: `0.40.6`
- Ollama models observed:
  - `llama3.2:3b` — ID `a80c4f17acd5`
  - `llama3.2:1b` — ID `baf6a787fdff`
- Python packages: captured with `python -m pip freeze` from the `backend` directory into `VALIDATION/baseline/pip-freeze.txt` during baseline capture. This reflects the active environment, not independently verified backend and frontend lockfiles.

## Completion status

| Baseline item | Status |
|---|---|
| Record existing commit | Done — hash above |
| Record Python/Ollama/model list | Done |
| Record PostgreSQL version | Blocked — `psql` unavailable; server version unknown |
| Freeze environment dependencies | Partial — backend interpreter `pip freeze` is captured; separate reproducible lockfiles not established |
| Create baseline branch | Not done — requires reviewed clean snapshot |
| Create baseline tag | Not done — worktree is dirty |
| Push tag | Not done — no tag created and remote push requires owner authorization |

Do not treat this artifact as proof that the current dirty worktree is reproducible. No existing changes were discarded or staged.
