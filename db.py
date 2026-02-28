import psycopg2
import hashlib
from psycopg2 import pool
from psycopg2 import errors
# -----------------------------
# CONNECTION POOL
# -----------------------------
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,
        10,
        host="localhost",
        database="fyp_chatbot",
        user="postgres",
        password="1234567890",
        port=5432
    )
except Exception as e:
    print("Error creating connection pool:", e)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# USERS
# -----------------------------
def user_exists(email):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(%s)",
            (email,)
        )

        return cur.fetchone() is not None

    except Exception as e:
        print("User exists check error:", e)
        return True

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


import psycopg2
from psycopg2 import errors
def add_user(username, email, password):

    conn = None
    cur = None

    try:
        conn = get_connection()

        if conn is None:
            return False, "Database connection failed."

        cur = conn.cursor()

        email = email.strip().lower()
        username = username.strip()

        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (username, email, hash_password(password))
        )

        conn.commit()

        return True, "Account created successfully. Please login."

    except psycopg2.errors.UniqueViolation:
        if conn:
            conn.rollback()
        return False, "This email is already registered."

    except Exception as e:
        if conn:
            conn.rollback()
        print("Signup error:", e)
        return False, "Signup failed."

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def check_login(email, password):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, username, email
            FROM users
            WHERE LOWER(email)=LOWER(%s)
            AND password_hash=%s
            """,
            (email, hash_password(password))
        )

        return cur.fetchone()

    except Exception as e:
        print("Login error:", e)
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def update_password(email, new_password):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE users
            SET password_hash=%s
            WHERE LOWER(email)=LOWER(%s)
            """,
            (hash_password(new_password), email)
        )

        conn.commit()

        if cur.rowcount == 0:
            return False

        return True

    except Exception as e:
        print("Password update error:", e)
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


# -----------------------------
# MESSAGES
# -----------------------------
def add_message(user_id, role, content):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (%s, %s, %s)
            """,
            (user_id, role, content)
        )

        conn.commit()

    except Exception as e:
        print("Add message error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_messages(user_id):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id=%s
            ORDER BY id
            """,
            (user_id,)
        )

        return cur.fetchall()

    except Exception as e:
        print("Get messages error:", e)
        return []

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


# -----------------------------
# MOOD TRACKER
# -----------------------------
def add_mood(user_id, mood):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO mood (user_id, mood)
            VALUES (%s, %s)
            """,
            (user_id, mood)
        )

        conn.commit()

    except Exception as e:
        print("Add mood error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_moods(user_id):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT mood
            FROM mood
            WHERE user_id=%s
            """,
            (user_id,)
        )

        return [row[0] for row in cur.fetchall()]

    except Exception as e:
        print("Get moods error:", e)
        return []

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


# -----------------------------
# JOURNAL
# -----------------------------
def add_journal(user_id, entry):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO journal (user_id, entry)
            VALUES (%s, %s)
            """,
            (user_id, entry)
        )

        conn.commit()

    except Exception as e:
        print("Add journal error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_journals(user_id):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT entry
            FROM journal
            WHERE user_id=%s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        return [row[0] for row in cur.fetchall()]

    except Exception as e:
        print("Get journals error:", e)
        return []

    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)