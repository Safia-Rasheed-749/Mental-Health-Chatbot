# PostgreSQL Connection Pool Report

## Overview

The backend uses `psycopg2.pool.ThreadedConnectionPool` to reuse PostgreSQL connections across requests/threads instead of opening a new database connection for every operation.

## Pool lifecycle

1. **Application startup:** `backend/app/main.py` calls `init_pool()` from the FastAPI lifespan startup handler.
2. **Pool creation:** `backend/app/database/connection.py` creates the pool once and stores it in the module-level `_pool` variable. Connection settings come from `backend/app/core/config.py`.
3. **Acquire and return:** `db_cursor()` obtains a connection with `getconn()`, yields a cursor for the database operation, then closes the cursor and returns the connection with `putconn()`.
4. **Transaction handling:** When called with `commit=True`, `db_cursor()` commits after a successful operation. If an exception occurs, it rolls back and re-raises the exception.
5. **Application shutdown:** FastAPI calls `close_pool()`, which closes all pooled connections and clears `_pool`.

## Configuration

These environment variables configure the database and pool:
/
| Variable | Default | Purpose |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL server host |
| `DB_PORT` | `5432` | PostgreSQL server port |
| `DB_NAME` | `fyp_chatbot` | Database name |
| `DB_USER` | `postgres` | Database username |
| `DB_PASSWORD` | Empty | Database password |
| `DB_POOL_MIN` | `1` | Minimum connections opened for the pool |
| `DB_POOL_MAX` | `10` | Maximum connections allowed in the pool |

The settings are loaded from `backend/.env` (or the process environment). Each teammate should configure their own local `backend/.env` with the credentials appropriate to their database setup. Do not commit real credentials or include them in reports; keep the `.env` file private and out of version control.

## Relevant source files

- `backend/app/database/connection.py` — pool creation, cursor helper, and cleanup.
- `backend/app/core/config.py` — environment-based settings and defaults.
- `backend/app/main.py` — startup and shutdown lifecycle hooks.

## Notes

The current pool is created lazily if `db_cursor()` is called before startup initialization. The configured minimum and maximum are per running backend process, so deployments with multiple worker processes can use up to `DB_POOL_MAX` connections per process. Ensure the PostgreSQL server's connection limit accounts for the total workers and other clients.
