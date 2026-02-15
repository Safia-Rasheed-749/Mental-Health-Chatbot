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
# ---------------- LOAD CSS ----------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
# ------------------------- gTTS Voice Function -------------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Mental Wellness Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Powered Conversational Assistant For Mental Health Support")

# ==========================================================
# ======================= AUTH =============================
# ==========================================================

if "user" not in st.session_state:

    st.subheader("🔐 Authentication")

    choice = st.radio("Select Action", ["Login", "Sign Up"])

    # ---------------- SIGN UP ----------------
    if choice == "Sign Up":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            try:
                add_user(username, email, password)
                st.success("Account created successfully! Please login.")
                st.rerun()
            except Exception as e:
                st.error("User may already exist.") 
                

    # ---------------- LOGIN ----------------
    if choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = check_login(email, password)

            if user:
                st.session_state["user"] = user
                st.success(f"Welcome {user[1]}!")
                st.rerun()
            else:
                st.error("Incorrect email or password")

    st.stop()

# ==========================================================
# =================== AFTER LOGIN ==========================
# ==========================================================

user_id = st.session_state["user"][0]
username = st.session_state["user"][1]

col1, col2 = st.columns([6,1])
with col1:
    st.success(f"Logged in as: {username}")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()

# ==========================================================
# ======================= CHAT =============================
# ==========================================================

st.subheader("💬 Chat")

messages = get_messages(user_id)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, content in messages:
    if role == "user":
        st.markdown(f'<div class="user-msg">You: {content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">Assistant: {content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
# Input box
user_input = st.text_input("Type your message...")

if st.button("Send Message") and user_input.strip():

    # Save user message
    add_message(user_id, "user", user_input)

    # Simulated AI response (replace later with real model)
    with st.spinner("Assistant is typing..."):
        time.sleep(1.5)
        response = "I hear you. Let’s explore this together."

    # Save assistant response
    add_message(user_id, "assistant", response)

    st.experimental_rerun()  # use experimental_rerun instead of rerun
    st.subheader("🎤 Voice Feature")
st.write("Record your voice or type message in this section.")

# ---------------- Voice Recording ----------------
audio = mic_recorder(
    start_prompt="Start Recording", 
    stop_prompt="Stop Recording", 
    key="voice"
)

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

            # Assistant response
            with st.spinner("Assistant is typing..."):
                import time
                time.sleep(1.5)
                response = "I hear you. Let’s explore this together."
                add_message(user_id, "assistant", response)
                speak(response)  # speak the response
            st.experimental_rerun()
        except:
            st.error("Could not recognize speech.")

# ---------------- Voice Section Typing Option ----------------
voice_text_input = st.text_input("Or type message in Voice section...")

if st.button("Send from Voice Section") and voice_text_input.strip():
    add_message(user_id, "user", voice_text_input)

    # Assistant response
    with st.spinner("Assistant is typing..."):
        import time
        time.sleep(1.5)
        response = "I hear you. Let’s explore this together."
        add_message(user_id, "assistant", response)
        speak(response)  # speak the response
    st.experimental_rerun()




# ==========================================================
# ===================== MOOD TRACKER =======================
# ==========================================================

st.subheader("📊 Mood Tracker")

mood = st.radio(
    "How are you feeling today?",
    ["Happy", "Neutral", "Sad", "Anxious", "Angry"]
)

if st.button("Log Mood"):
    add_mood(user_id, mood)
    st.success("Mood Logged Successfully!")

# Display mood chart
moods = get_moods(user_id)

if moods:
    mood_counts = {m: moods.count(m) for m in set(moods)}

    fig, ax = plt.subplots()
    ax.bar(mood_counts.keys(), mood_counts.values())
    ax.set_title("Mood Overview")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# ==========================================================
# ======================== JOURNAL =========================
# ==========================================================

st.subheader("📝 Journal")

journal_entry = st.text_area("Write your thoughts here...")

if st.button("Save Journal Entry"):
    if journal_entry.strip():
        add_journal(user_id, journal_entry)
        st.success("Journal entry saved!")

# Show last 5 journal entries
journals = get_journals(user_id)

if journals:
    st.write("Recent Entries:")
    for entry in journals[:5]:
        st.write("-", entry)
