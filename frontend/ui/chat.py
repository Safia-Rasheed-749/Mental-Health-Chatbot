import requests
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
from gtts import gTTS
from db import add_message, create_conversation, get_messages_by_conversation, log_user_activity
# from utils.ai_engine import generate_response
from layout_utils import apply_clean_layout
import time
import base64

# Import custom React component
from components.sticky_chat import sticky_chat_bar

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

# ── Multi-turn conversation memory helpers ──────────────────────────────────
# build_history_for_api() converts st.session_state["chat_history"] (list of
# tuples) into the API format (list of dicts).  It excludes the last entry
# because that is the current user message, which is sent in the "message" field.

def build_history_for_api(max_turns: int = 3) -> list:
    """
    Build history list for the backend API from st.session_state["chat_history"].

    - Excludes the last entry (current user message already appended to history)
    - Keeps only the last max_turns turns (1 turn = 1 user + 1 assistant = 2 entries)
    - Converts (role, content) tuples to {"role": str, "content": str} dicts
    - Skips malformed entries gracefully

    Returns:
        List of {"role": str, "content": str} dicts, or [] if nothing to send.
    """
    history_list = []
    if "chat_history" not in st.session_state:
        return history_list

    all_messages = st.session_state["chat_history"]

    # Need at least 2 entries: 1 previous + 1 current (which we exclude)
    if len(all_messages) <= 1:
        return history_list

    previous_messages = all_messages[:-1]          # exclude current message

    max_messages   = max_turns * 2                 # each turn = user + assistant
    recent_messages = previous_messages[-max_messages:]

    for entry in recent_messages:
        try:
            role, content = entry
            history_list.append({"role": role, "content": str(content)})
        except (ValueError, TypeError):
            continue  # skip malformed entries

    return history_list


def generate_response_from_backend(message: str, history: list = None) -> dict:
    url = "http://127.0.0.1:8000/chat"

    payload = {"message": message, "history": history if history else []}

    response = requests.post(
        url,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data  # Return full dict (includes crisis, severity, response, etc.)
# ---------------- CHAT ----------------
def show_chat(user_id):
    apply_clean_layout(hide_header_completely=False)

    st.markdown("""
    <style>
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stAppDeployButton {
        display: none;  /* Hide "Deploy" button */
    }  
    #MainMenu { 
        visibility: hidden !important;  /* Hide hamburger menu */
    }
    footer { 
        visibility: hidden !important;  /* Hide "Made with Streamlit" footer */
    }
    header {
        background: transparent !important;  /* Transparent header for clean look */
        box-shadow: none !important;
        visibility: visible !important;  /* Keep header visible for sidebar toggle */
    }
    
    /* ═══════════════════════════════════════════════════════════════
       SIDEBAR TOGGLE BUTTON STYLING
       Purpose: Make sidebar toggle button visible and styled
       Location: Top-left corner when sidebar is collapsed
       Color: Gradient blue-purple (#6366f1 to #8b5cf6)
       Same gradient used in: auth.py buttons, dashboard.py cards
       Controlled by: Streamlit's built-in sidebar component
    ═══════════════════════════════════════════════════════════════ */
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;  /* Brand gradient */
        color: white !important;
        border-radius: 0 8px 8px 0 !important;  /* Rounded right side only */
        padding: 8px !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;  /* Subtle shadow */
        transition: all 0.2s ease !important;  /* Smooth animation */
    }
    
    [data-testid="collapsedControl"]:hover {
        transform: translateX(2px) !important;  /* Slide right on hover */
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;  /* Stronger shadow on hover */
    }

    /*page background color */
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 45%, #F5F3FF 100%) !important;
        /* #F8FAFC = Very light gray-blue (start) */
        /* #EEF4FF = Light blue (middle) */
        /* #F5F3FF = Light purple (end) */
    }
    
    /* ── SMOOTH PAGE TRANSITIONS ── */
    .stApp {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    /* ── MAIN CONTAINER ── */
    .main {
        padding-bottom: 100px !important;
    }
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }
     /* Banner color */
    /* ── HEADER BANNER ── */
    .chat-header {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(91,141,239,0.28);
        border-radius: 20px;
        margin: 10px 0 15px 0;
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
        50% { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
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
        50% { opacity: 0.4; }
    }

    /* ── CHAT MESSAGES AREA ── */
    .chat-area {
        padding: 10px 24px 20px 24px;
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
        to { opacity: 1; transform: translateY(0); }
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
        50% { transform: translateY(-8px); }
    }
    /* page content styling that is in center*/
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
        animation: thinkingBounce 1.4s infinite ease-in-out;
        display: inline-block;
    }
    .thinking-dots span:nth-child(1) { animation-delay: 0s; }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes thinkingBounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* ── AUDIO ── */
    audio { display: none !important; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }
    
    /* ── REACT COMPONENT STICKY POSITIONING ── */
    /* Target the component wrapper directly */
    [data-testid="stCustomComponentV1"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999999 !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        transition: left 0.3s ease, width 0.3s ease !important;
    }
    
    /* Adjust for sidebar on desktop */
    @media (min-width: 768px) {
        /* When sidebar is visible */
        section[data-testid="stSidebar"]:not([aria-expanded="false"]) ~ div [data-testid="stCustomComponentV1"] {
            left: 260px !important;
            width: calc(100% - 260px) !important;
        }
        
        /* When sidebar is hidden */
        section[data-testid="stSidebar"][aria-expanded="false"] ~ div [data-testid="stCustomComponentV1"] {
            left: 0 !important;
            width: 100% !important;
        }
    }
    
    /* Make iframe full width and proper height */
    [data-testid="stCustomComponentV1"] iframe {
        width: 100% !important;
        height: 80px !important;
        border: none !important;
        display: block !important;
    }

    </style>
    """, unsafe_allow_html=True)

   
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-avatar">🧠</div>
        <div class="chat-header-text">
            <h1>MindCare AI</h1>
            <p>Your personal mental wellness companion</p>
        </div>
        <div class="chat-header-status">
            <div class="status-dot"></div>
            Available
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
    st.markdown('<div class="chat-area" id="chat-messages">', unsafe_allow_html=True)
    # hello i am here for you content */
    if not st.session_state["chat_history"]:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-state-icon">🌿</span>
            <h3>Hello, I'm here for you</h3>
            <p>Feel free to share anything on your mind.<br>This is a safe, judgment-free space.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, (role, msg) in enumerate(st.session_state["chat_history"]):
            if role == "user":
                st.markdown(f"""
                <div class="chat-row" style="justify-content:flex-end;">
                    <div class="user-bubble">{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # ── PERSISTENT CRISIS BANNER ──
                crisis_meta = st.session_state.get("_crisis_metadata", {}).get(idx)
                if crisis_meta and crisis_meta.get("crisis"):
                    _sev = crisis_meta.get("severity")
                    _severity_styles = {
                        "HIGH":   {"bg": "#dc2626", "border": "#991b1b", "label": "🚨 URGENT — Please reach out for help now"},
                        "MEDIUM": {"bg": "#ea580c", "border": "#9a3412", "label": "⚠️ We're concerned — Please talk to someone"},
                        "LOW":    {"bg": "#ca8a04", "border": "#854d0e", "label": "💛 Please take care — Support is available"},
                    }
                    _style = _severity_styles.get(_sev, _severity_styles["HIGH"])
                    st.markdown(
                        f'<div style="background:{_style["bg"]};color:#ffffff;'
                        f'padding:10px 16px;border-radius:10px;margin-bottom:21px;'
                        f'font-weight:600;font-size:13px;border-left:4px solid {_style["border"]};'
                        f'box-shadow:0 4px 12px rgba(220,38,38,0.25);'
                        f'display:flex;align-items:center;gap:8px;">'
                        f'<span style="font-size:14px;">{_style["label"]}</span>'
                        f'<span style="margin-left:auto;font-size:10px;background:rgba(255,255,255,0.25);'
                        f'padding:3px 8px;border-radius:10px;font-weight:500;">SUPPORT</span></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(f"""
                <div class="chat-row" style="justify-content:flex-start;">
                    <div class="ai-bubble-wrap">
                        <div class="ai-avatar">🧠</div>
                        <div class="assistant-bubble">{msg}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # PHASE 2a — show dots, call AI, store response, rerun
    # ══════════════════════════════════════════════════════
    if st.session_state.get("_ai_thinking"):
        st.markdown("""
        <div class="chat-row" style="justify-content:flex-start;">
            <div class="ai-bubble-wrap">
                <div class="ai-avatar">🧠</div>
                <div class="assistant-bubble" style="padding:14px 18px;min-width:70px;">
                    <div class="thinking-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pending      = st.session_state.pop("_ai_thinking")
        pending_type = pending["type"]
        pending_text = pending["text"]

        # response = generate_response(pending_text, st.session_state["chat_history"][-5:])
        # Build history from previous turns (excludes current message) and send to API
        history_for_api = build_history_for_api(max_turns=3)
        response_data = generate_response_from_backend(pending_text, history=history_for_api)
        st.session_state["_ai_typing"] = {
            "type":     pending_type,
            "response": response_data["response"],
            "crisis":   response_data.get("crisis", False),
            "severity": response_data.get("severity"),
        }
        st.rerun()

    # ══════════════════════════════════════════════════════
    # PHASE 2b — typewriter: one character at a time
    # ══════════════════════════════════════════════════════
    elif st.session_state.get("_ai_typing"):
        import html as _html
        data         = st.session_state.pop("_ai_typing")
        pending_type = data["type"]
        response     = data["response"]
        data_crisis  = data.get("crisis", False)
        data_severity = data.get("severity")
        safe         = _html.escape(response)

        # ── CRISIS BANNER — rendered BEFORE slot so it always sits above the message ──
        if data_crisis:
            _severity_colors = {"HIGH": "#dc2626", "MEDIUM": "#ea580c", "LOW": "#ca8a04"}
            _severity_borders = {"HIGH": "#991b1b", "MEDIUM": "#9a3412", "LOW": "#854d0e"}
            _severity_labels  = {
                "HIGH":   "🚨 URGENT — Please reach out for help now",
                "MEDIUM": "⚠️ We're concerned — Please talk to someone",
                "LOW":    "💛 Please take care — Support is available",
            }
            banner_color  = _severity_colors.get(data_severity, "#dc2626")
            banner_border = _severity_borders.get(data_severity, "#991b1b")
            banner_label  = _severity_labels.get(data_severity, _severity_labels["HIGH"])
            st.markdown(
                f'<div style="background:{banner_color};color:#ffffff;'
                f'padding:10px 16px;border-radius:10px;margin-bottom:21px;'
                f'font-weight:600;font-size:13px;border-left:4px solid {banner_border};'
                f'box-shadow:0 4px 12px rgba(220,38,38,0.25);'
                f'display:flex;align-items:center;gap:8px;">'
                f'<span style="font-size:14px;">{banner_label}</span>'
                f'<span style="margin-left:auto;font-size:10px;background:rgba(255,255,255,0.25);'
                f'padding:3px 8px;border-radius:10px;font-weight:500;">SUPPORT</span></div>',
                unsafe_allow_html=True,
            )

        # slot declared AFTER banner so typewriter text renders below the banner
        slot = st.empty()

        for i in range(1, len(safe) + 1):
            slot.markdown(
                f'<div class="chat-row" style="justify-content:flex-start;">'
                f'<div class="ai-bubble-wrap">'
                f'<div class="ai-avatar">🧠</div>'
                f'<div class="assistant-bubble" style="white-space:pre-wrap;">{safe[:i]}'
                f'<span style="display:inline-block;width:2px;height:1em;background:#8b5cf6;'
                f'margin-left:1px;vertical-align:text-bottom;'
                f'animation:cur 0.6s step-end infinite;"></span>'
                f'</div></div></div>'
                f'<style>@keyframes cur{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>',
                unsafe_allow_html=True,
            )
            time.sleep(0.01)

        slot.markdown(
            f'<div class="chat-row" style="justify-content:flex-start;">'
            f'<div class="ai-bubble-wrap">'
            f'<div class="ai-avatar">🧠</div>'
            f'<div class="assistant-bubble" style="white-space:pre-wrap;">{safe}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        message_index = len(st.session_state["chat_history"])
        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)

        # Persist crisis metadata keyed by message index so the history loop
        # can re-render the banner after st.rerun() clears the typewriter slot.
        if "_crisis_metadata" not in st.session_state:
            st.session_state["_crisis_metadata"] = {}
        st.session_state["_crisis_metadata"][message_index] = {
            "crisis":   data_crisis,
            "severity": data_severity,
        }

        if pending_type == "voice":
            speak_and_auto_play(response)

        st.session_state["component_key_timestamp"] = time.time()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── AUTO-SCROLL via parent frame ──
    # st.markdown scripts run in the main Streamlit iframe and CAN access window.parent
    msg_count = len(st.session_state["chat_history"])
    st.markdown(f"""
    <script>
    (function(){{
        var key = 'sc_{msg_count}';
        if(window._sc === key) return;
        window._sc = key;
        function sc(){{
            try{{
                var p = window.parent;
                var el = p.document.querySelector('[data-testid="stAppViewContainer"]');
                if(!el) el = p.document.querySelector('section.main');
                if(!el) el = p.document.documentElement;
                if(el) el.scrollTop = el.scrollHeight + 9999;
            }}catch(e){{}}
        }}
        sc(); setTimeout(sc,120); setTimeout(sc,400); setTimeout(sc,800);
    }})();
    </script>
    """, unsafe_allow_html=True)

    # ===== REACT COMPONENT - STICKY CHAT BAR =====
    # Use timestamp in key to force component reset after each message
    if "component_key_timestamp" not in st.session_state:
        st.session_state["component_key_timestamp"] = time.time()
    
    component_key = f"chat_input_{cid if cid else 'new'}_{st.session_state['component_key_timestamp']}"
    user_input = sticky_chat_bar(key=component_key)

    # ================= HANDLE INPUT FROM REACT COMPONENT =================
    # Guard: skip if we're already in a thinking/typing phase
    if user_input and not st.session_state.get("_ai_thinking") and not st.session_state.get("_ai_typing"):
        # Create conversation on first message
        if not cid:
            cid = create_conversation(user_id)
            st.session_state["conversation_id"] = cid
            st.session_state["last_loaded_chat"] = cid
            st.session_state["_crisis_metadata"] = {}  # reset on new conversation

        # ===== TEXT MESSAGE =====
        if user_input["type"] == "text":
            text = user_input["data"]

            st.session_state["chat_history"].append(("user", text))
            add_message(user_id, "user", text, cid)

            try:
                log_user_activity(user_id, "Send Message", "Chat", f"Message: {text[:50]}...")
            except Exception as e:
                print(f"Activity logging error: {e}")

            # Reset component key NOW so Phase 2a gets a blank input field
            st.session_state["component_key_timestamp"] = time.time()
            st.session_state["_ai_thinking"] = {"type": "text", "text": text}
            st.rerun()

        # ===== AUDIO MESSAGE =====
        elif user_input["type"] == "audio":
            audio_bytes = bytes(user_input["data"])
            recognizer = sr.Recognizer()
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                    tmp.write(audio_bytes)
                    webm_path = tmp.name

                wav_path = webm_path.replace(".webm", ".wav")
                audio_segment = AudioSegment.from_file(webm_path, format="webm")
                audio_segment.export(wav_path, format="wav")

                with sr.AudioFile(wav_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    voice_text = recognizer.recognize_google(audio_data)

                if voice_text.strip():
                    st.session_state["chat_history"].append(("user", voice_text))
                    add_message(user_id, "user", voice_text, cid)

                    try:
                        os.unlink(webm_path)
                        os.unlink(wav_path)
                    except:
                        pass

                    # Reset component key NOW so Phase 2a gets a blank input field
                    st.session_state["component_key_timestamp"] = time.time()
                    st.session_state["_ai_thinking"] = {"type": "voice", "text": voice_text}
                    st.rerun()
                else:
                    st.warning("Could not recognize speech. Please try again.")

            except sr.UnknownValueError:
                st.warning("Sorry, I couldn't understand that. Please speak clearly.")
            except Exception as e:
                st.error(f"Voice error: {str(e)}")
