# ========== FORCE FFMPEG PATH ==========
import os
import sys

# Set environment variable BEFORE importing pydub
os.environ["PATH"] = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin" + os.pathsep + os.environ.get("PATH", "")

# Now import pydub and force it to use our path
from pydub import AudioSegment

# Explicitly set the paths
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffprobe.exe"

# Force pydub to re-initialize
from pydub.utils import which
AudioSegment._ffmpeg = which("ffmpeg")
AudioSegment._ffprobe = which("ffprobe")

# ========== REST OF IMPORTS ==========
import streamlit as st
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from db import add_message, create_conversation, get_messages_by_conversation
from utils.ai_engine import generate_response
from layout_utils import apply_clean_layout
import time
import base64

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = None

if "last_loaded_chat" not in st.session_state:
    st.session_state["last_loaded_chat"] = None

if "voice_processed_key" not in st.session_state:
    st.session_state["voice_processed_key"] = None

# ---------------- SPEAK WITH AUTO-PLAY ----------------
def speak_and_auto_play(text):
    """Convert text to speech and auto-play using HTML5 audio"""
    tts = gTTS(text=text, lang="en")
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(audio_path)
    
    # Read audio file and convert to base64 for embedding
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # Store in session for auto-play
    st.session_state["auto_play_audio"] = audio_base64
    
    # Cleanup
    try:
        os.unlink(audio_path)
    except:
        pass

# ---------------- CHAT ----------------
def show_chat(user_id):
    apply_clean_layout(hide_header_completely=False)

        # ========== COMPLETE CSS FIX - STRICTLY STICKY BOTTOM ==========
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    header, footer, .stDeployButton {
        display: none !important;
    }
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
    
    /* Title fixed at top */
    .chat-title {
        text-align: center;
        font-size: 24px;
        font-weight: 600;
        padding: 15px;
        background: #EAF3FF;
        border-bottom: 2px solid #4A6FA5;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
    }
    
    /* Chat area - scrollable */
    .chat-area {
        # position: fixed;
        # top: 65px;
        # bottom: 75px;
        # left: 0;
        # right: 0;
        # overflow-y: auto;
        # padding: 15px 20px;
        # background: #F5F7FB;
        height: calc(100vh - 130px);
        overflow-y: auto;
        padding-right: 10px;
        scroll-behavior: smooth;  /* Add smooth scrolling */

    }
    
    /* Message row */
    .chat-row {
        display: flex;
        margin-bottom: 15px;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User bubble */
    .user-bubble {
        background: #4A6FA5;
        color: white;
        padding: 10px 16px;
        border-radius: 20px;
        font-size: 14px;
        max-width: 70%;
        word-wrap: break-word;
        border-bottom-right-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Assistant bubble */
    .assistant-bubble {
        background: white;
        color: #1E3A5F;
        padding: 14px 16px;
        border-radius: 20px;
        font-size: 14px;
        max-width: 85%;
        word-wrap: break-word;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Fixed input bar at bottom */
    .input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        # right: 0;
        #background: #EAF3FF;
        width: 100%;
        background: white;
        padding: 10px 15px;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }
    
    /* Input field styling */
    div[data-testid="stTextInput"] input {
         border: 2px solid #333 !important;
        border-radius: 20px !important;
        padding: 8px 15px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        outline: none !important;
        border-color: #3D5A8C !important;
    }
    
    /* Send button styling */
    .stButton > button {
        background: #4A6FA5 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        padding: 0 !important;
        border: none !important;
        font-size: 18px !important;
    }
    
    .stButton > button:hover {
        background: #3D5A8C !important;
        transform: scale(1.02);
    }
    
    /* Hide default audio player */
    audio {
        display: none !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #E8EEF2;
    }
    ::-webkit-scrollbar-thumb {
        background: #4A6FA5;
        border-radius: 3px;
    }
    
    /* Thinking indicator */
    .thinking-dots {
        display: inline-flex;
        gap: 4px;
    }
    .thinking-dots span {
        width: 8px;
        height: 8px;
        background: #4A6FA5;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }
    .thinking-dots span:nth-child(1) { animation-delay: 0s; }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="chat-title">💬 Chat with MindCare AI</div>', unsafe_allow_html=True)

    # Auto-play audio using JavaScript (hidden)
    if "auto_play_audio" in st.session_state:
        audio_base64 = st.session_state["auto_play_audio"]
        st.markdown(f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
        </audio>
        <script>
            // Force autoplay
            document.querySelector('audio').play();
        </script>
        """, unsafe_allow_html=True)
        del st.session_state["auto_play_audio"]

    # ---------------- CONVERSATION ----------------
    if not st.session_state.get("conversation_id"):
        st.session_state["conversation_id"] = create_conversation(user_id)

    cid = st.session_state["conversation_id"]

    if st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid

    # Display chat messages
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for role, msg in st.session_state["chat_history"]:
        if role == "user":
            st.markdown(f"""
            <div class="chat-row" style="justify-content:flex-end;">
                <div class="user-bubble">{msg}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="assistant-bubble">🧠 {msg}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ========== STRICTLY STICKY INPUT BAR ==========
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    
    # Create row with input, send button, and voice button
    col1, col2, col3 = st.columns([10, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Type your message...",
            label_visibility="collapsed",
            key=f"text_input_{cid}"
        )
    
    with col2:
        send_clicked = st.button("➤", key=f"send_btn_{cid}")
    
    with col3:
        audio = mic_recorder(
            start_prompt="🎤", 
            stop_prompt="⏹️", 
            key=f"voice_rec_{cid}",
            just_once=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

        # ================= TEXT SEND WITH TYPING ANIMATION =================
    if send_clicked and user_input.strip():
        # Save user message
        st.session_state["chat_history"].append(("user", user_input))
        add_message(user_id, "user", user_input, cid)

        # Create placeholder for typing animation
        typing_placeholder = st.empty()
        
        # Show typing indicator with correct CSS
        typing_placeholder.markdown("""
        <div class="chat-row" style="justify-content:flex-start;">
            <div class="assistant-bubble" style="background:#E8EEF2;">
                🧠 <span class="thinking-dots">
                    <span></span><span></span><span></span>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate AI response
        response = generate_response(user_input, st.session_state["chat_history"][-5:])
        
        # Remove typing indicator
        typing_placeholder.empty()
        
        # Create placeholder for streaming response
        response_placeholder = st.empty()
        
        # Stream the response word by word
        output = ""
        for word in response.split():
            output += word + " "
            response_placeholder.markdown(f"""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="assistant-bubble">🧠 {output}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.03)  # Typing speed
        
        # Save final response
        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)
        
        st.rerun()

    # ================= PROCESS VOICE INPUT =================
    if audio:
        if "voice_processed_key" not in st.session_state:
            st.session_state["voice_processed_key"] = None
        voice_key = f"{cid}_{len(st.session_state['chat_history'])}"
        
        if st.session_state["voice_processed_key"] != voice_key:
            st.session_state["voice_processed_key"] = voice_key
            
            response_placeholder = st.empty()
            response_placeholder.markdown("""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="assistant-bubble" style="background:#E8EEF2;">
                    <div class="thinking-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            recognizer = sr.Recognizer()
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                    tmp.write(audio["bytes"])
                    webm_path = tmp.name
                
                wav_path = webm_path.replace(".webm", ".wav")
                audio_segment = AudioSegment.from_file(webm_path, format="webm")
                audio_segment.export(wav_path, format="wav")
                
                with sr.AudioFile(wav_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    voice_text = recognizer.recognize_google(audio_data)
                
                if voice_text.strip():
                    response_placeholder.empty()
                    
                    # Add user message
                    st.session_state["chat_history"].append(("user", voice_text))
                    add_message(user_id, "user", voice_text, cid)
                    
                    # Generate response
                    response = generate_response(voice_text, st.session_state["chat_history"][-5:])
                    
                    # Add assistant response
                    st.session_state["chat_history"].append(("assistant", response))
                    add_message(user_id, "assistant", response, cid)
                    
                    # Speak with auto-play
                    speak_and_auto_play(response)
                    
                    # Cleanup
                    try:
                        os.unlink(webm_path)
                        os.unlink(wav_path)
                    except:
                        pass
                    
                    st.rerun()
                else:
                    response_placeholder.empty()
                    st.warning("Could not recognize speech. Please try again.")
                    
            except sr.UnknownValueError:
                response_placeholder.empty()
                st.warning("Sorry, I couldn't understand that. Please speak clearly.")
            except Exception as e:
                response_placeholder.empty()
                st.error(f"Voice error: {str(e)}")