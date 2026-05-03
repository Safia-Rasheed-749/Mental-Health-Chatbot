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
from db import add_message, create_conversation, get_messages_by_conversation, log_user_activity
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

    # ========== REDESIGNED CSS ==========
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── HIDE CLUTTER ── */
    .stDeployButton { display: none !important; }
    #MainMenu       { visibility: hidden !important; }
    footer          { visibility: hidden !important; }
    header {
        background: transparent !important;
        box-shadow: none !important;
        visibility: visible !important;
    }

    /* ── PAGE BACKGROUND ── */
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 45%, #F5F3FF 100%) !important;
        height: 100%;
    }

    /* ── BLOCK CONTAINER ── */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }

    /* ── HEADER BANNER ── */
    .chat-header {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(91,141,239,0.28);
        border-radius: 20px;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    .chat-header-avatar {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        border: 2px solid rgba(255,255,255,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.12);
        animation: headerPulse 3s ease-in-out infinite;
    }
    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(255,255,255,0.12); }
        50%       { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
    }
    .chat-header-text h1 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    .chat-header-text p {
        margin: 2px 0 0;
        font-size: 18px;
        color: rgba(255,255,255,0.78);
        font-weight: 400;
    }
    .chat-header-status {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: rgba(255,255,255,0.85);
        font-weight: 500;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 6px #4ade80;
        animation: statusBlink 2s ease-in-out infinite;
    }
    @keyframes statusBlink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }

    /* ── CHAT MESSAGES AREA ── */
    .chat-area {
        padding: 20px 16px 10px;
        min-height: 60px;
        max-height: calc(100vh - 320px);
        overflow-y: auto;
        scroll-behavior: smooth;
    }

    /* ── MESSAGE ROWS ── */
    .chat-row {
        display: flex;
        margin-bottom: 24px;
        animation: msgFadeIn 0.35s ease;
    }
    @keyframes msgFadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── USER BUBBLE ── */
    .user-bubble {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff;
        padding: 11px 16px;
        border-radius: 20px 20px 4px 20px;
        font-size: 14px;
        line-height: 1.55;
        max-width: 68%;
        word-wrap: break-word;
        box-shadow: 0 4px 14px rgba(99,102,241,0.30);
    }

    /* ── AI BUBBLE ── */
    .ai-bubble-wrap {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        max-width: 82%;
    }
    .ai-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        box-shadow: 0 2px 10px rgba(99,102,241,0.35);
        margin-top: 2px;
    }
    .assistant-bubble {
        background: #ffffff;
        color: #1e293b;
        padding: 12px 16px;
        border-radius: 4px 20px 20px 20px;
        font-size: 14px;
        line-height: 1.65;
        word-wrap: break-word;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 3px solid #8b5cf6;
    }

    /* ── EMPTY STATE ── */
    .empty-state {
        text-align: center;
        padding: 60px 20px 40px;
        color: #64748b;
    }
    .empty-state-icon {
        font-size: 56px;
        margin-bottom: 16px;
        display: block;
        animation: floatIcon 3s ease-in-out infinite;
    }
    @keyframes floatIcon {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-8px); }
    }
    .empty-state h3 {
        font-size: 20px;
        font-weight: 700;
        color: #4338ca;
        margin: 0 0 8px;
    }
    .empty-state p {
        font-size: 14px;
        color: #94a3b8;
        margin: 0;
        line-height: 1.6;
    }

    /* ── STICKY INPUT BAR ── */
    .input-bar-wrapper {
        position: fixed;
        bottom: 0;
        left: 280px;          /* sidebar width */
        right: 0;
        z-index: 1000;
        background: rgba(238,242,255,0.92);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-top: 1px solid rgba(99,102,241,0.18);
        padding: 12px 20px 14px;
        box-shadow: 0 -4px 24px rgba(99,102,241,0.10);
    }

    /* ── INPUT FIELD ── */
    .input-bar-wrapper div[data-testid="stTextInput"] input {
        border: 2px solid rgba(99,102,241,0.35) !important;
        border-radius: 24px !important;
        padding: 10px 18px !important;
        font-size: 14px !important;
        background: #ffffff !important;
        color: #1e293b !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    }
    .input-bar-wrapper div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        outline: none !important;
    }
    .input-bar-wrapper div[data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
    }

    /* ── SEND BUTTON ── */
    .input-bar-wrapper .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        padding: 0 !important;
        border: none !important;
        font-size: 18px !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.40) !important;
        transition: transform 0.18s, box-shadow 0.18s !important;
    }
    .input-bar-wrapper .stButton > button:hover {
        transform: scale(1.08) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.55) !important;
    }

    /* ── MIC BUTTON (streamlit_mic_recorder renders a button) ── */
    .input-bar-wrapper div[data-testid="stCustomComponentV1"] button,
    .input-bar-wrapper iframe {
        border-radius: 50% !important;
    }
    /* Style the mic recorder container */
    .mic-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    /* Pulse ring around mic area */
    .mic-pulse-ring {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10b981, #34d399);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 14px rgba(16,185,129,0.40);
        animation: micPulse 2.5s ease-in-out infinite;
        cursor: pointer;
        position: relative;
    }
    .mic-pulse-ring::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: rgba(16,185,129,0.30);
        animation: micRing 2.5s ease-in-out infinite;
    }
    @keyframes micPulse {
        0%, 100% { box-shadow: 0 4px 14px rgba(16,185,129,0.40); }
        50%       { box-shadow: 0 4px 22px rgba(16,185,129,0.65); }
    }
    @keyframes micRing {
        0%   { transform: scale(1);   opacity: 0.6; }
        100% { transform: scale(1.6); opacity: 0; }
    }

    /* ── THINKING DOTS ── */
    .thinking-dots {
        display: inline-flex;
        gap: 5px;
        align-items: center;
        padding: 4px 0;
    }
    .thinking-dots span {
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }
    .thinking-dots span:nth-child(1) { animation-delay: 0s; }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30%            { transform: translateY(-9px); }
    }

    /* ── AUDIO ── */
    audio { display: none !important; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar       { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }

    </style>
    """, unsafe_allow_html=True)

    # ── HEADER BANNER ──
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-avatar">🧠</div>
        <div class="chat-header-text">
            <h1>MindCare AI</h1>
            <p>Your personal mental wellness companion</p>
        </div>
        <div class="chat-header-status">
            <div class="status-dot"></div>
            Online
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    # Don't create conversation until user sends first message
    cid = st.session_state.get("conversation_id")

    if cid and st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid

    # ── MESSAGES ──
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)

    if not st.session_state["chat_history"]:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-state-icon">🌿</span>
            <h3>Hello, I'm here for you</h3>
            <p>Feel free to share anything on your mind.<br>This is a safe, judgment-free space.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
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
                    <div class="ai-bubble-wrap">
                        <div class="ai-avatar">🧠</div>
                        <div class="assistant-bubble">{msg}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── AUTO-SCROLL TO BOTTOM (STRONG VERSION) ──
    st.markdown("""
    <script>
        function scrollToBottom() {
            // Scroll chat area
            const chatArea = document.querySelector('.chat-area');
            if (chatArea) {
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            // Scroll main window
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }
        
        // Scroll immediately
        setTimeout(scrollToBottom, 100);
        
        // Keep trying to scroll (for dynamic content)
        let scrollInterval = setInterval(function() {
            const chatArea = document.querySelector('.chat-area');
            if (chatArea && chatArea.scrollHeight > chatArea.clientHeight) {
                scrollToBottom();
            }
        }, 500);
        
        // Stop interval after 10 seconds
        setTimeout(function() {
            clearInterval(scrollInterval);
        }, 10000);
    </script>
    """, unsafe_allow_html=True)

    # ── STICKY INPUT BAR ──
    st.markdown('<div class="input-bar-wrapper">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([10, 1, 1])

    with col1:
        # Use a dynamic key that changes after each message to clear input
        input_key = f"text_input_{cid if cid else 'new'}_{len(st.session_state['chat_history'])}"
        user_input = st.text_input(
            "",
            placeholder="Share what's on your mind...",
            label_visibility="collapsed",
            key=input_key
        )

    with col2:
        send_clicked = st.button("➤", key=f"send_btn_{cid if cid else 'new'}")
        

    with col3:
        # Custom styled mic button wrapper
        st.markdown("""
        <style>
        /* Mic button custom styling */
        div[data-testid="stCustomComponentV1"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        div[data-testid="stCustomComponentV1"] button {
            width: 44px !important;
            height: 44px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #10b981, #34d399) !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(16,185,129,0.40) !important;
            transition: all 0.2s !important;
            animation: micPulseBtn 2.5s ease-in-out infinite !important;
        }
        div[data-testid="stCustomComponentV1"] button:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 6px 20px rgba(16,185,129,0.55) !important;
        }
        @keyframes micPulseBtn {
            0%, 100% { box-shadow: 0 4px 14px rgba(16,185,129,0.40); }
            50%       { box-shadow: 0 4px 22px rgba(16,185,129,0.65), 0 0 0 8px rgba(16,185,129,0.15); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        audio = mic_recorder(
            start_prompt="🎙️",
            stop_prompt="⏹️",
            key=f"voice_rec_{cid if cid else 'new'}",
            just_once=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= TEXT SEND WITH TYPING ANIMATION =================
    if send_clicked and user_input.strip():
        # Create conversation on first message
        if not cid:
            cid = create_conversation(user_id)
            st.session_state["conversation_id"] = cid
            st.session_state["last_loaded_chat"] = cid
        
        st.session_state["chat_history"].append(("user", user_input))
        add_message(user_id, "user", user_input, cid)
        # ✅ ADD ACTIVITY LOGGING HERE (CORRECT PLACE)
        try:
            log_user_activity(
                user_id,  # Use the parameter, not session_state
                "Send Message", 
                "Chat", 
                f"Message: {user_input[:50]}..."  # Use user_input variable
            )
        except Exception as e:
            print(f"Activity logging error: {e}")  # Don't break the chat if logging fails

        # Show bouncing dots FIRST
        dots_placeholder = st.empty()
        dots_placeholder.markdown("""
        <div class="chat-row" style="justify-content:flex-start;">
            <div class="ai-bubble-wrap">
                <div class="ai-avatar">🧠</div>
                <div class="assistant-bubble">
                    <div class="thinking-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Get response from AI
        response = generate_response(user_input, st.session_state["chat_history"][-5:])
        
        # Remove bouncing dots
        dots_placeholder.empty()
        
        # Create placeholder for typing animation
        response_placeholder = st.empty()
        
        # Character by character typing with proper word rendering
        full_response = ""
        for i in range(len(response)):
            full_response = response[:i+1]  # Take characters one by one
            response_placeholder.markdown(f"""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="ai-bubble-wrap">
                    <div class="ai-avatar">🧠</div>
                    <div class="assistant-bubble">{full_response}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.01)  # 20ms per character
       # Save to session and database

        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)
                # Auto-scroll to bottom
        st.markdown("""
        <script>
            setTimeout(function() {
                const chatArea = document.querySelector('.chat-area');
                if(chatArea) chatArea.scrollTop = chatArea.scrollHeight;
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }, 50);
        </script>
        """, unsafe_allow_html=True)
        
        st.rerun()

    # ================= PROCESS VOICE INPUT =================
    if audio:
        if "voice_processed_key" not in st.session_state:
            st.session_state["voice_processed_key"] = None
        voice_key = f"{cid if cid else 'new'}_{len(st.session_state['chat_history'])}"

        if st.session_state["voice_processed_key"] != voice_key:
            st.session_state["voice_processed_key"] = voice_key
            
            # Create conversation on first message
            if not cid:
                cid = create_conversation(user_id)
                st.session_state["conversation_id"] = cid
                st.session_state["last_loaded_chat"] = cid

            response_placeholder = st.empty()
            response_placeholder.markdown("""
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="ai-bubble-wrap">
                    <div class="ai-avatar">🧠</div>
                    <div class="assistant-bubble">
                        <div class="thinking-dots">
                            <span></span><span></span><span></span>
                        </div>
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
