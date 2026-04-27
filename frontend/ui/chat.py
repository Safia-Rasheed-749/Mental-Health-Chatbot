import streamlit as st
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from db import add_message, create_conversation, get_messages_by_conversation
from utils.ai_engine import generate_response
from layout_utils import apply_clean_layout
from pydub import AudioSegment
import time
import base64

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = None

if "last_loaded_chat" not in st.session_state:
    st.session_state["last_loaded_chat"] = None

if "voice_processed" not in st.session_state:
    st.session_state["voice_processed"] = False

if "pending_audio" not in st.session_state:
    st.session_state["pending_audio"] = None

# ---------------- SPEAK & PLAY (using HTML autoplay) ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(path)
    # Encode audio file to base64 for HTML autoplay
    with open(path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.session_state["pending_audio"] = b64

# ---------------- CHAT ----------------
def show_chat(user_id):
    apply_clean_layout(hide_header_completely=False)

    # Play pending audio if exists
    if st.session_state["pending_audio"]:
        st.markdown(
            f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{st.session_state["pending_audio"]}" type="audio/mp3"></audio>',
            unsafe_allow_html=True
        )
        st.session_state["pending_audio"] = None

    st.markdown("""
    <style>
    /* Keep normal Streamlit flow */
    html, body {
        height: 100%;
    }
    /* Page spacing fix */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 90px !important;
        max-width: 100% !important;
    }
    /* Title (centered + larger) */
    .title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        margin-top: 0px;
        margin-bottom: 25px;
        color: #1e293b;
    }
    /* Chat area scrollable */
    .chat-area {
        height: calc(100vh - 200px);
        overflow-y: auto;
        padding-right: 10px;
    }
    .chat-row {
        display: flex;
        margin-bottom: 14px;
    }
    /* User bubble */
    .user-bubble {
        background-color: #dbeafe;
        padding: 10px 14px;
        border-radius: 18px;
        font-size: 15px;
        max-width: 40%;
        word-wrap: break-word;
    }
    /* Assistant bubble */
    .assistant-bubble {
        background-color: #ffffff;
        padding: 14px 18px;
        border-radius: 18px;
        font-size: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        max-width: 85%;
        word-wrap: break-word;
    }
    /* Fixed input bar */
    .input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 10px 15px;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }
    /* Input style */
    div[data-testid="stTextInput"] input {
        border: 2px solid #333 !important;
        border-radius: 20px !important;
        padding: 8px 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">💬 Chat with MindCare AI</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Conversation management
    if not st.session_state.get("conversation_id"):
        st.session_state["conversation_id"] = create_conversation(user_id)

    cid = st.session_state["conversation_id"]

    if st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid

    # Display chat history
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for role, msg in st.session_state["chat_history"]:
        if role == "user":
            st.markdown(f"""
            <div class="chat-row" style="justify-content:flex-end;">
                <div class="user-bubble">👤 {msg}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="assistant-bubble">🧠 {msg}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input bar
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    with st.form(key=f"chat_form_{cid}", clear_on_submit=True):
        col1, col2, col3 = st.columns([10, 1, 1])
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Type your message...",
                label_visibility="collapsed",
                key=f"input_text_{cid}"
            )
        with col2:
            submitted = st.form_submit_button("➤")
        with col3:
            audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key=f"mic_{cid}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Text input handling
    if submitted and user_input.strip():
        st.session_state["voice_processed"] = False  # Reset voice flag

        st.session_state["chat_history"].append(("user", user_input))
        add_message(user_id, "user", user_input, cid)

        response = generate_response(user_input, st.session_state["chat_history"][-5:])

        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)

        speak(response)   # Trigger TTS and store audio in session
        st.rerun()

    # Voice input handling – automatically sent when recording stops
    if audio and not st.session_state["voice_processed"]:
        st.session_state["voice_processed"] = True

        r = sr.Recognizer()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                tmp.write(audio["bytes"])
                path = tmp.name

            wav = path.replace(".webm", ".wav")
            AudioSegment.from_file(path).export(wav, format="wav")

            with sr.AudioFile(wav) as source:
                data = r.record(source)
                text = r.recognize_google(data)

            # Add user message
            st.session_state["chat_history"].append(("user", text))
            add_message(user_id, "user", text, cid)

            # Generate AI response
            response = generate_response(text, st.session_state["chat_history"][-5:])

            # Add assistant message
            st.session_state["chat_history"].append(("assistant", response))
            add_message(user_id, "assistant", response, cid)

            # Speak the response (will be played on next rerun)
            speak(response)

            st.rerun()

        except Exception as e:
            st.error(f"Voice not recognized: {e}")
            st.session_state["voice_processed"] = False  # Allow retry