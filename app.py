import psycopg2
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
from gtts import gTTS
import base64
import streamlit as st
import time
import matplotlib.pyplot as plt
from db import (
    add_user,
    check_login,
    get_messages,
    add_message,
    add_mood,
    get_moods,
    add_journal,
    get_journals
)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "chat"

# ---------------- CSS ----------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# ---------------- VOICE / TTS ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Mental Wellness GPT", page_icon="🧠", layout="wide")

# ======================= AUTH =======================
if st.session_state["user"] is None:
    st.title("🧠 Mental Wellness GPT Assistant")
    st.subheader("🔐 Authentication")
    choice = st.radio("Select Action", ["Login", "Sign Up"])

    if choice == "Sign Up":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Create Account"):
            try:
                add_user(username, email, password)
                st.success("Account created! Please login.")
                st.rerun()
            except psycopg2.errors.UniqueViolation:
                st.error("User already exists.")
            except Exception as e:
                st.error(f"Error: {e}")

    if choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = check_login(email, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Incorrect email or password")
    st.stop()

# ======================= AFTER LOGIN =======================
user_id = st.session_state["user"][0]
username = st.session_state["user"][1]

# ================= SIDEBAR =================
st.sidebar.title(f"Hello, {username}!")
st.sidebar.markdown("### Menu")
if st.sidebar.button("Chat"):
    st.session_state["page"] = "chat"
    st.rerun()
if st.sidebar.button("Dashboard"):
    st.session_state["page"] = "dashboard"
    st.rerun()
if st.sidebar.button("Logout"):
    del st.session_state["user"]
    st.rerun()

# ================= MAIN AREA =================
if st.session_state["page"] == "chat":
    st.title("💬 Chat Assistant")

    # Display chat messages
    messages = get_messages(user_id)
    for role, content in messages[-10:]:
        if role == "user":
            st.markdown(f'<div class="user-msg">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{content}</div>', unsafe_allow_html=True)

    # Text input
    user_input = st.text_input("Type your message here...")
    if st.button("Send Message") and user_input.strip():
        add_message(user_id, "user", user_input)
        with st.spinner("Assistant is typing..."):
            time.sleep(1.5)
            response = "I hear you. Let's explore this together."
            add_message(user_id, "assistant", response)
            speak(response)
        st.rerun()

    # Voice input
    st.subheader("🎤 Voice Feature")
    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key="voice")
    if audio:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio["bytes"])
            wav_path = tmp.name
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                voice_text = recognizer.recognize_google(audio_data)
                add_message(user_id, "user", voice_text)
                with st.spinner("Assistant is typing..."):
                    time.sleep(1.5)
                    response = "I hear you. Let's explore this together."
                    add_message(user_id, "assistant", response)
                    speak(response)
                st.rerun()
            except:
                st.error("Could not recognize speech")

    # Convert chat text to speech
    st.subheader("🔊 Convert Text to Sound")
    text_to_speak = st.text_area("Enter text to convert to audio")
    if st.button("Convert to Speech") and text_to_speak.strip():
        speak(text_to_speak)

# ================= DASHBOARD =================
elif st.session_state["page"] == "dashboard":
    st.title("📊 Dashboard")
    tabs = st.tabs(["Previous Chats", "Mood Tracker", "Journal"])

    # Previous Chats Tab
    with tabs[0]:
        st.subheader("Previous Chats")
        messages = get_messages(user_id)
        for role, content in messages:
            if role == "user":
                st.markdown(f'<div class="user-msg">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">{content}</div>', unsafe_allow_html=True)

    # Mood Tracker Tab
    with tabs[1]:
        st.subheader("Mood Tracker")
        mood = st.radio("How are you feeling today?", ["Happy", "Neutral", "Sad", "Anxious", "Angry"])
        if st.button("Log Mood"):
            add_mood(user_id, mood)
            st.success("Mood logged successfully!")
        moods = get_moods(user_id)
        if moods:
            mood_counts = {m: moods.count(m) for m in set(moods)}
            fig, ax = plt.subplots()
            ax.bar(mood_counts.keys(), mood_counts.values())
            ax.set_ylabel("Count")
            ax.set_title("Mood Overview")
            st.pyplot(fig)

    # Journal Tab
    with tabs[2]:
        st.subheader("Journal")
        journal_entry = st.text_area("Write your thoughts here...")
        if st.button("Save Journal Entry") and journal_entry.strip():
            add_journal(user_id, journal_entry)
            st.success("Journal entry saved!")
        journals = get_journals(user_id)
        if journals:
            st.subheader("Recent Entries")
            for entry in journals[-5:]:
                st.write("-", entry)
