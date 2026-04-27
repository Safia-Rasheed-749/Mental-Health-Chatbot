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

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = None

if "last_loaded_chat" not in st.session_state:
    st.session_state["last_loaded_chat"] = None

# ---------------- SPEAK ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(path)
    st.session_state["audio_file"] = path

# ---------------- STREAM RESPONSE (if you want, but currently not used) ----------------
def stream_response(full_text, placeholder):
    output = ""
    for word in full_text.split():
        output += word + " "
        placeholder.markdown(f"""
        <div style="
            background-color:#ffffff;
            color:#111;
            padding:14px 18px;
            border-radius:18px;
            max-width:100%;
            font-size:18px;
            line-height:1.7;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
            🧠 {output}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)

# ---------------- CHAT ----------------
def show_chat(user_id):
    apply_clean_layout(hide_header_completely=False)

    # ========== FIXED LAYOUT WITH STICKY INPUT ==========
    st.markdown("""
    <style>
    html, body {
        height: 100%;
        overflow: hidden !important;
    }

    /* Remove default Streamlit padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Title fixed at top */
    .title {
        text-align: center;
        font-size: 28px;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    /* Chat area scrollable between title and input */
    .chat-area {
        position: absolute;
        top: 60px;
        bottom: 80px;
        left: 0;
        right: 0;
        overflow-y: auto;
        padding: 10px 15px;
    }

    /* Message row */
    .chat-row {
        display: flex;
        margin-bottom: 14px;
    }

    /* User bubble (light blue) */
    .user-bubble {
        background-color: #dbeafe;
        padding: 10px 14px;
        border-radius: 18px;
        font-size: 15px;
        max-width: 40%;
        word-wrap: break-word;
    }

    /* Assistant bubble (white with shadow) */
    .assistant-bubble {
        background-color: #ffffff;
        padding: 14px 18px;
        border-radius: 18px;
        font-size: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        max-width: 85%;
        word-wrap: break-word;
    }

    /* Sticky input bar at bottom */
    .input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 10px;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }

    /* Dark outline on input field */
    div[data-testid="stTextInput"] input {
        border: 2px solid #333 !important;
        border-radius: 20px !important;
        padding: 8px 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">💬 Chat with MindCare AI</div>', unsafe_allow_html=True)

    # ---------------- CONVERSATION ----------------
    if not st.session_state.get("conversation_id"):
        st.session_state["conversation_id"] = create_conversation(user_id)

    cid = st.session_state["conversation_id"]

    if st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid

    # Chat messages area
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

    # ========== STICKY INPUT BAR WITH FORM ==========
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    # Use a form to automatically clear input after submit
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
            # mic_recorder must be outside the form? Actually it can be inside, but to keep same layout we put inside
            # However mic_recorder is not a form submit button; it's safe to put inside form.
            audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key=f"mic_{cid}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= TEXT SEND =================
    if submitted and user_input.strip():
        st.session_state["chat_history"].append(("user", user_input))
        add_message(user_id, "user", user_input, cid)

        response = generate_response(user_input, st.session_state["chat_history"][-5:])

        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)

        st.rerun()

    # ================= VOICE INPUT =================
    if audio:
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

            st.session_state["chat_history"].append(("user", text))
            add_message(user_id, "user", text, cid)

            response = generate_response(text, st.session_state["chat_history"][-5:])

            st.session_state["chat_history"].append(("assistant", response))
            add_message(user_id, "assistant", response, cid)

            speak(response)
            st.rerun()

        except Exception as e:
            st.error(f"Voice not recognized: {e}")