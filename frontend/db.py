import psycopg2
import hashlib
from psycopg2 import pool
from psycopg2 import errors
import json
from datetime import datetime, timedelta
import secrets

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
        password="123456789",
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
    """
    Returns (id, username, email, is_admin) if successful, else None
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, username, email, is_admin
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
        return cur.rowcount > 0
    except Exception as e:
        print("Password update error:", e)
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def create_reset_token(user_id):
    conn = None
    cur = None
    try:
        reset_code = ''.join(secrets.choice('0123456789') for _ in range(6))
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=1)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE password_reset_tokens 
            SET used = TRUE 
            WHERE user_id = %s AND used = FALSE
            """,
            (user_id,)
        )
        cur.execute(
            """
            INSERT INTO password_reset_tokens 
            (user_id, reset_code, reset_token, expires_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, reset_code, reset_token, expires_at
            """,
            (user_id, reset_code, reset_token, expires_at)
        )
        token_data = cur.fetchone()
        conn.commit()
        return {
            'id': token_data[0],
            'reset_code': token_data[1],
            'reset_token': token_data[2],
            'expires_at': token_data[3]
        }
    except Exception as e:
        print(f"Error creating reset token: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def verify_reset_token(email, reset_code):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.id, u.email
            FROM users u
            JOIN password_reset_tokens t ON u.id = t.user_id
            WHERE LOWER(u.email) = LOWER(%s)
            AND t.reset_code = %s
            AND t.used = FALSE
            AND t.expires_at > NOW()
            ORDER BY t.created_at DESC
            LIMIT 1
            """,
            (email, reset_code)
        )
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error verifying reset token: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def reset_password_with_code(email, reset_code, new_password):
    conn = None
    cur = None
    try:
        user_id = verify_reset_token(email, reset_code)
        if not user_id:
            return False, "Invalid or expired reset code"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE users 
            SET password_hash = %s
            WHERE id = %s
            """,
            (hash_password(new_password), user_id)
        )
        cur.execute(
            """
            UPDATE password_reset_tokens 
            SET used = TRUE 
            WHERE user_id = %s AND reset_code = %s
            """,
            (user_id, reset_code)
        )
        conn.commit()
        return True, "Password reset successfully"
    except Exception as e:
        print(f"Error resetting password: {e}")
        if conn:
            conn.rollback()
        return False, f"Password reset failed: {str(e)}"
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_user_by_email(email):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, username, email
            FROM users
            WHERE LOWER(email) = LOWER(%s)
            """,
            (email,)
        )
        result = cur.fetchone()
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'email': result[2]
            }
        return None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


# -----------------------------
# MESSAGES & CONVERSATIONS
# -----------------------------
def get_or_create_current_conversation(user_id):
    """
    Returns the most recent conversation ID for the user.
    If none exists, creates a new conversation and returns its ID.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Get the latest conversation
        cur.execute(
            "SELECT id FROM conversations WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        row = cur.fetchone()
        if row:
            return row[0]
        # No conversation exists – create one
        cur.execute(
            "INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING id",
            (user_id, "New Chat")
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        print("Error in get_or_create_current_conversation:", e)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def rename_conversation(conversation_id, new_title):
    """Update the title of a conversation (optional)."""
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE conversations SET title = %s WHERE id = %s",
            (new_title, conversation_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Error renaming conversation:", e)
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def add_message(user_id, role, content, conversation_id=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        # If no conversation_id provided, get or create one
        if conversation_id is None:
            conversation_id = get_or_create_current_conversation(user_id)
            if conversation_id is None:
                raise Exception("Could not obtain conversation ID")
        
        cur.execute(
            """
            INSERT INTO messages (user_id, role, content, conversation_id)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, role, content, conversation_id)
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
# CONVERSATIONS
# -----------------------------
def create_conversation(user_id, title="New Chat"):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO conversations (user_id, title)
            VALUES (%s, %s)
            RETURNING id
            """,
            (user_id, title)
        )
        convo_id = cur.fetchone()[0]
        conn.commit()
        return convo_id
    except Exception as e:
        print("Create conversation error:", e)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_conversations(user_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            WHERE user_id=%s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        return cur.fetchall()
    except Exception as e:
        print("Get conversations error:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_messages_by_conversation(conversation_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT role, content
            FROM messages
            WHERE conversation_id=%s
            ORDER BY id
            """,
            (conversation_id,)
        )
        return cur.fetchall()
    except Exception as e:
        print("Get messages by conversation error:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


# -----------------------------
# NEW FUNCTION FOR HISTORY PAGE (all messages with timestamps)
# -----------------------------
def get_all_user_messages(user_id):
    """
    Returns a list of tuples (role, content, created_at, conversation_id)
    for all messages of the user, ordered from oldest to newest.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT role, content, created_at, conversation_id
            FROM messages
            WHERE user_id = %s
            ORDER BY created_at ASC
        """, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print("Error fetching all user messages:", e)
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


# -----------------------------
# ADMIN FUNCTIONS
# -----------------------------
def get_all_users():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, email, is_admin, created_at
            FROM users
            ORDER BY id
        """)
        rows = cur.fetchall()
        users = []
        for row in rows:
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'is_admin': row[3],
                'created_at': row[4] if len(row) > 4 else None
            })
        return users
    except Exception as e:
        print("Error fetching all users:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_messages_by_user(user_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE user_id = %s
            ORDER BY id
        """, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print("Error fetching user messages:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_moods_by_user(user_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT mood, created_at
            FROM mood
            WHERE user_id = %s
            ORDER BY id
        """, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print("Error fetching user moods:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)


def get_journals_by_user(user_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT entry, created_at
            FROM journal
            WHERE user_id = %s
            ORDER BY id DESC
        """, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print("Error fetching user journals:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            release_connection(conn)