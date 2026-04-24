import psycopg2
import hashlib
from psycopg2 import pool
from datetime import datetime, timedelta
import secrets

# -----------------------------
# CONNECTION POOL
# -----------------------------
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    10,
    host="localhost",
    database="fyp_chatbot",
    user="postgres",
    password="123456",
    port=5432
)

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
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM users WHERE LOWER(email)=LOWER(%s)", (email,))
        return cur.fetchone() is not None
    except Exception as e:
        print(e)
        return True
    finally:
        cur.close()
        release_connection(conn)


def add_user(username, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        email = email.strip().lower()
        username = username.strip()

        cur.execute("""
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES (%s, %s, %s, %s)
        """, (username, email, hash_password(password), False))

        conn.commit()
        return True, "Account created successfully"

    except Exception as e:
        conn.rollback()
        print(e)
        return False, "Signup failed"

    finally:
        cur.close()
        release_connection(conn)


def check_login(email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, username, email, is_admin
            FROM users
            WHERE LOWER(email)=LOWER(%s)
            AND password_hash=%s
        """, (email.strip().lower(), hash_password(password)))

        return cur.fetchone()

    except Exception as e:
        print(e)
        return None

    finally:
        cur.close()
        release_connection(conn)


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, username, email
            FROM users
            WHERE LOWER(email)=LOWER(%s)
        """, (email,))

        row = cur.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "email": row[2]}
        return None

    finally:
        cur.close()
        release_connection(conn)

# -----------------------------
# PASSWORD RESET (FIX ADDED)
# -----------------------------
def create_reset_token(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        reset_code = ''.join(secrets.choice("0123456789") for _ in range(6))
        expires_at = datetime.now() + timedelta(hours=1)

        cur.execute("""
            INSERT INTO password_reset_tokens (user_id, reset_code, used, expires_at)
            VALUES (%s, %s, %s, %s)
        """, (user_id, reset_code, False, expires_at))

        conn.commit()

        return {
            "reset_code": reset_code,
            "expires_at": expires_at
        }

    finally:
        cur.close()
        release_connection(conn)


def reset_password_with_code(email, reset_code, new_password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.id
            FROM users u
            JOIN password_reset_tokens t ON u.id = t.user_id
            WHERE LOWER(u.email)=LOWER(%s)
            AND t.reset_code=%s
            AND t.used=FALSE
            AND t.expires_at > NOW()
            ORDER BY t.id DESC
            LIMIT 1
        """, (email, reset_code))

        row = cur.fetchone()

        if not row:
            return False, "Invalid or expired reset code"

        user_id = row[0]

        cur.execute("""
            UPDATE users
            SET password_hash=%s
            WHERE id=%s
        """, (hash_password(new_password), user_id))

        cur.execute("""
            UPDATE password_reset_tokens
            SET used=TRUE
            WHERE user_id=%s AND reset_code=%s
        """, (user_id, reset_code))

        conn.commit()
        return True, "Password reset successful"

    finally:
        cur.close()
        release_connection(conn)

# -----------------------------
# MESSAGES
# -----------------------------
def add_message(user_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO messages (user_id, role, content)
            VALUES (%s, %s, %s)
        """, (user_id, role, content))
        conn.commit()
    finally:
        cur.close()
        release_connection(conn)


def get_messages(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT role, content
            FROM messages
            WHERE user_id=%s
            ORDER BY id
        """, (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        release_connection(conn)

# -----------------------------
# MOOD
# -----------------------------
def add_mood(user_id, mood):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO mood (user_id, mood) VALUES (%s,%s)", (user_id, mood))
        conn.commit()
    finally:
        cur.close()
        release_connection(conn)


def get_moods(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT mood FROM mood WHERE user_id=%s", (user_id,))
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
        release_connection(conn)

# -----------------------------
# JOURNAL
# -----------------------------
def add_journal(user_id, entry):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO journal (user_id, entry) VALUES (%s,%s)", (user_id, entry))
        conn.commit()
    finally:
        cur.close()
        release_connection(conn)


def get_journals(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT entry FROM journal WHERE user_id=%s ORDER BY id DESC", (user_id,))
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
        release_connection(conn)

# -----------------------------
# ADMIN
# -----------------------------
def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, username, email, is_admin, created_at
            FROM users
            ORDER BY id
        """)
        rows = cur.fetchall()

        return [
            {
                "id": r[0],
                "username": r[1],
                "email": r[2],
                "is_admin": r[3],
                "created_at": r[4]
            }
            for r in rows
        ]

    finally:
        cur.close()
        release_connection(conn)
        # -----------------------------
# ADMIN COMPATIBILITY FUNCTIONS
# (to match admin.py imports)
# -----------------------------

def get_messages_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE user_id=%s
            ORDER BY id
        """, (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        release_connection(conn)


def get_moods_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT mood, created_at
            FROM mood
            WHERE user_id=%s
            ORDER BY id
        """, (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        release_connection(conn)


def get_journals_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT entry, created_at
            FROM journal
            WHERE user_id=%s
            ORDER BY id DESC
        """, (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        release_connection(conn)