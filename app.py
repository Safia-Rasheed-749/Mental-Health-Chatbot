import streamlit as st
import psycopg2
import re
import time
from gtts import gTTS
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import tempfile
from pydub import AudioSegment
import matplotlib.pyplot as plt

from db import (
    add_user,
    check_login,
    add_message,
    get_messages,
    add_mood,
    get_moods,
    add_journal,
    get_journals,
    update_password
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mental Wellness Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD CSS ----------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- PASSWORD VALIDATION ----------------
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    return True

# ---------------- TEXT TO SPEECH ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    st.audio("response.mp3")

# ---------------- SESSION INIT ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# =========================
# 🔐 AUTHENTICATION SECTION
# =========================
if st.session_state["user"] is None:

    st.title("🧠 AI Mental Wellness Assistant")
    st.subheader("Secure Login & Registration")

    auth_choice = st.radio(
        "Select Action",
        ["Login", "Sign Up", "Forgot Password"]
    )

    # -------- SIGN UP --------
    if auth_choice == "Sign Up":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if not is_valid_password(password):
            st.warning("⚠ Password must be at least 8 characters and contain at least one number.")

        else:
            success, message = add_user(username, email, password)

            if success:
                st.success(message)
            else:
                st.error(message)

    # -------- LOGIN --------
    elif auth_choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = check_login(email, password)
            if user:
                st.session_state["user"] = user
                st.success(f"Welcome {user[1]}!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    # -------- FORGOT PASSWORD --------
    elif auth_choice == "Forgot Password":
        email_reset = st.text_input("Enter your registered email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if not is_valid_password(new_pass):
                st.warning("Password must be at least 8 characters and contain a number.")
            else:
                try:
                    update_password(email_reset, new_pass)
                    st.success("Password updated successfully! Please login.")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.stop()

# =========================
# 🏠 AFTER LOGIN
# =========================

user_id = st.session_state["user"][0]
username = st.session_state["user"][1]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(f"### 👋 Welcome, {username}")
    st.divider()

    menu = st.radio(
        "Navigation",
        ["Dashboard", "Chat", "History", "Mood Analytics", "Journal"]
    )

    st.divider()

    if st.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

# =========================
# 📊 DASHBOARD
# =========================
if menu == "Dashboard":
    st.title("Your AI Mental Wellness Companion")
    st.markdown("""
    ✔ Emotion-aware AI Conversations  
    ✔ Voice Interaction Support  
    ✔ Mood Tracking & Journaling  
    ✔ Secure & Private Data Storage  
    """)

# =========================
# 💬 CHAT SECTION
# =========================
elif menu == "Chat":

    st.title("Chat with AI Assistant")

    messages = get_messages(user_id)

    # Display chat history in ChatGPT style
    for role, content in messages:
        if role == "user":
            with st.chat_message("user"):
                st.write(content)
        else:
            with st.chat_message("assistant"):
                st.write(content)

    # Text Chat Input
    user_input = st.chat_input("Type your message...")

    if user_input:
        add_message(user_id, "user", user_input)

        response = "I hear you. Let's explore this together."
        add_message(user_id, "assistant", response)

        speak(response)
        st.rerun()

    # Voice Recording
    st.markdown("### 🎤 Voice Input")
    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        key="voice_recorder"
    )

    if audio:
        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio["bytes"])
            tmp_path = tmp.name

        wav_path = tmp_path.replace(".webm", ".wav")
        sound = AudioSegment.from_file(tmp_path)
        sound.export(wav_path, format="wav")

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                voice_text = recognizer.recognize_google(audio_data)

                add_message(user_id, "user", voice_text)

                response = "I hear you. Let's explore this together."
                add_message(user_id, "assistant", response)

                speak(response)
                st.rerun()

            except Exception:
                st.error("Speech not recognized. Please try again.")

# =========================
# 📂 CHAT HISTORY
# =========================
elif menu == "History":
    st.title("Chat History")
    chats = get_messages(user_id)
    for role, content in chats:
        st.write(f"{role.upper()}: {content}")

# =========================
# 📈 MOOD ANALYTICS
# =========================
elif menu == "Mood Analytics":
    st.title("Mood Tracker")

    mood = st.radio(
        "How are you feeling today?",
        ["Happy", "Neutral", "Sad", "Anxious", "Angry"]
    )

    if st.button("Log Mood"):
        add_mood(user_id, mood)
        st.success("Mood logged successfully!")

    moods = get_moods(user_id)

    if moods:
        mood_counts = {m: moods.count(m) for m in set(moods)}
        fig, ax = plt.subplots()
        ax.bar(mood_counts.keys(), mood_counts.values())
        ax.set_title("Mood Overview")
        ax.set_ylabel("Count")
        st.pyplot(fig)

# =========================
# 📝 JOURNAL
# =========================
elif menu == "Journal":
    st.title("Personal Journal")

    entry = st.text_area("Write your thoughts here...")

    if st.button("Save Entry"):
        if entry.strip():
            add_journal(user_id, entry)
            st.success("Journal entry saved successfully.")

    journals = get_journals(user_id)
    if journals:
        st.subheader("Recent Entries")
        for j in journals[:5]:
            st.write("-", j)
