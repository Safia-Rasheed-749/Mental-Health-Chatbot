import streamlit as st
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from db import add_message
from utils.ai_engine import generate_response  # ⭐ our enhanced engine

# ---------------- Initialize session state ----------------
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'rerun' not in st.session_state:
    st.session_state['rerun'] = False


# ---------------- Text-to-Speech ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_file = fp.name
    st.audio(open(audio_file, "rb").read(), format="audio/mp3")


# ---------------- Chat Function ----------------
def show_chat(user_id):

    st.title("💬 Chat with MindCareAI")

    # Container to display chat messages
    chat_container = st.container()

    # ---------------- Text Input ----------------
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Save user message
        st.session_state['chat_history'].append(("user", user_input))
        add_message(user_id, "user", user_input)

        # Prepare context (last 5 messages)
        context = st.session_state['chat_history'][-5:]

        # ⭐ Generate AI response with context
        response = generate_response(user_input, context)

        # Save bot response
        st.session_state['chat_history'].append(("assistant", response))
        add_message(user_id, "assistant", response)

        # Play audio response
        speak(response)

    # ---------------- Voice Input ----------------
    st.markdown("### 🎤 Voice Input")

    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        key="voice_recorder"
    )

    if audio:
        recognizer = sr.Recognizer()
        try:
            # Save recorded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                tmp.write(audio["bytes"])
                tmp_path = tmp.name

            # Convert to WAV
            wav_path = tmp_path.replace(".webm", ".wav")
            AudioSegment.from_file(tmp_path).export(wav_path, format="wav")

            # Speech Recognition
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                voice_text = recognizer.recognize_google(audio_data)

            # Save user voice message
            st.session_state['chat_history'].append(("user", voice_text))
            add_message(user_id, "user", voice_text)

            # Prepare context
            context = st.session_state['chat_history'][-5:]

            # ⭐ Generate AI response with context
            response = generate_response(voice_text, context)

            # Save bot response
            st.session_state['chat_history'].append(("assistant", response))
            add_message(user_id, "assistant", response)

            # Play audio response
            speak(response)

        except Exception:
            st.error("Speech not recognized. Please try again.")

    # ---------------- Display messages ----------------
    for role, content in st.session_state['chat_history']:
        if role == "user":
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(
                        f"<div style='font-size:16px'>{content}</div>",
                        unsafe_allow_html=True
                    )
        else:
            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(
                        f"<div style='font-size:16px; color:#00695c'>{content}</div>",
                        unsafe_allow_html=True
                    )

    # ---------------- Styling ----------------
    st.markdown("""
        <style>
        .stChatMessage > div[data-testid="stMarkdownContainer"] {
            padding: 10px;
            border-radius: 10px;
        }
        .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
            background-color: #f1f8e9;
        }
        .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
            background-color: #e0f7fa;
        }
        </style>
    """, unsafe_allow_html=True)