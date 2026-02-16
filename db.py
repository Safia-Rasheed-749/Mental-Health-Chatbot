import psycopg2
import hashlib

# -----------------------------
# DB CONNECTION
# -----------------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="fyp_chatbot",
        user="postgres",
        password="123456",
        port=5432
    )

# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------------
# USERS
# -----------------------------
def add_user(username, email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s)",
        (username, email, hash_password(password))
    )
    conn.commit()
    cur.close()
    conn.close()

def check_login(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password_hash=%s",
        (email, hash_password(password))
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def update_password(email, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password_hash=%s WHERE email=%s",
        (hash_password(new_password), email)
    )
    conn.commit()
    cur.close()
    conn.close()

# -----------------------------
# MESSAGES
# -----------------------------
def add_message(user_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (%s,%s,%s)",
        (user_id, role, content)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_messages(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content FROM messages WHERE user_id=%s ORDER BY id",
        (user_id,)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# -----------------------------
# MOOD TRACKER
# -----------------------------
def add_mood(user_id, mood):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mood (user_id, mood) VALUES (%s,%s)",
        (user_id, mood)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_moods(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT mood FROM mood WHERE user_id=%s",
        (user_id,)
    )
    result = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return result

# -----------------------------
# JOURNAL
# -----------------------------
def add_journal(user_id, entry):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO journal (user_id, entry) VALUES (%s,%s)",
        (user_id, entry)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_journals(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT entry FROM journal WHERE user_id=%s ORDER BY id DESC",
        (user_id,)
    )
    result = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return result
