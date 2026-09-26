"""Thread-safe PostgreSQL connection pool and transaction helper."""

from contextlib import contextmanager
from typing import Iterator

from psycopg2 import pool

from app.core.config import settings

_pool = None


def init_pool():
    global _pool
    if _pool is None:
        _pool = pool.ThreadedConnectionPool(
            settings.db_pool_min,
            settings.db_pool_max,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
        )
    return _pool


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None


@contextmanager
def db_cursor(commit: bool = False) -> Iterator:
    """Yield a cursor and always return the connection to the pool."""
    connection_pool = init_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection_pool.putconn(connection)
