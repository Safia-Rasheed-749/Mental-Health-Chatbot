# ========== FORCE FFMPEG PATH ==========
import os
import sys

os.environ["PATH"] = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin" + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffprobe.exe"

from pydub.utils import which
AudioSegment._ffmpeg = which("ffmpeg")
AudioSegment._ffprobe = which("ffprobe")

import streamlit as st
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from db import add_message
from utils.ai_engine import generate_response
import time

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def speak(text):
    tts = gTTS(text=text, lang="en")
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(audio_path)
    st.session_state["audio_file"] = audio_path

def show_chat(user_id):
    # --- Remove top white space (safe, keeps header) ---
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: -0.5rem !important;
        }
        .main .block-container > :first-child {
            margin-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # TITLE
    st.title("💬 Chat with MindCare AI")

    # ---------------- CHAT HISTORY ----------------
    for role, content in st.session_state['chat_history']:
        with st.chat_message(role):
            if role == "assistant":
                st.markdown(
                    f"<div style='font-size:16px; color:#00695c'>{content}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='font-size:16px'>{content}</div>",
                    unsafe_allow_html=True
                )

    # ---------------- AUDIO PLAYER ----------------
    if "audio_file" in st.session_state:
        audio_file = open(st.session_state["audio_file"], "rb").read()
        st.audio(audio_file, format="audio/mp3")
        del st.session_state["audio_file"]

    # ---------------- INPUT BAR ----------------
    st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([6, 1, 1])

    with col1:
        user_text = st.text_input(
            "",
            key="text_input",
            placeholder="Type your message...",
            label_visibility="collapsed"
        )

    with col2:
        audio = mic_recorder(
            start_prompt="🎤",
            stop_prompt="⏹️",
            key="voice_recorder",
            just_once=True
        )

    with col3:
        send_clicked = st.button("➤")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- TEXT INPUT ----------------
    if send_clicked and user_text.strip():
        st.session_state['chat_history'].append(("user", user_text))
        add_message(user_id, "user", user_text)
        context = st.session_state['chat_history'][-5:]
        response = generate_response(user_text, context)
        st.session_state['chat_history'].append(("assistant", response))
        add_message(user_id, "assistant", response)
        st.rerun()

    # ---------------- VOICE INPUT ----------------
    if audio:
        recognizer = sr.Recognizer()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                tmp.write(audio["bytes"])
                tmp_path = tmp.name
            wav_path = tmp_path.replace(".webm", ".wav")
            AudioSegment.from_file(tmp_path).export(wav_path, format="wav")
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                voice_text = recognizer.recognize_google(audio_data)
            st.session_state['chat_history'].append(("user", voice_text))
            add_message(user_id, "user", voice_text)
            context = st.session_state['chat_history'][-5:]
            response = generate_response(voice_text, context)
            st.session_state['chat_history'].append(("assistant", response))
            add_message(user_id, "assistant", response)
            speak(response)
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(f"Speech not recognized. {str(e)}")

    # ---------------- AUTO SCROLL ----------------
    st.markdown("""
    <script>
        var chat = window.parent.document.querySelector('.main');
        chat.scrollTo(0, chat.scrollHeight);
    </script>
    """, unsafe_allow_html=True)

    # ---------------- STYLING ----------------
    st.markdown("""
    <style>
    .stChatMessage {
        border: none !important;
        background: transparent !important;
    }
    .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
        background-color: #f1f8e9 !important;
        border-radius: 12px;
        padding: 10px;
    }
    .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
        background-color: #e0f7fa !important;
        border-radius: 12px;
        padding: 10px;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 10px 20px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    .fixed-bottom div[data-testid="stHorizontalBlock"] {
        border: 2px solid black;
        border-radius: 25px;
        padding: 8px;
        background: white;
    }
    .stTextInput input {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    .fixed-bottom .stButton button {
        border: none !important;
        background: transparent !important;
        font-size: 20px;
    }
    .fixed-bottom .stButton button:hover {
        background: #f0f0f0 !important;
        border-radius: 50%;
    }
    .block-container {
        padding-bottom: 100px;
    }
    </style>
    """, unsafe_allow_html=True)