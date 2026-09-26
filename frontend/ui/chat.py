import requests
# ========== FORCE FFMPEG PATH ==========
import os
import sys
from shutil import which

# Set environment variable BEFORE importing pydub
ffmpeg_dir = os.getenv("FFMPEG_DIR")
if ffmpeg_dir and os.path.isdir(ffmpeg_dir):
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Now import pydub and force it to use our path
from pydub import AudioSegment

# Explicitly set the paths
AudioSegment.converter = os.getenv("FFMPEG_PATH") or which("ffmpeg")
AudioSegment.ffprobe = os.getenv("FFPROBE_PATH") or which("ffprobe")

# Force pydub to re-initialize
from pydub.utils import which
AudioSegment._ffmpeg = which("ffmpeg")
AudioSegment._ffprobe = which("ffprobe")

# ========== REST OF IMPORTS ==========
import streamlit as st
import streamlit.components.v1 as components
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
    url = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/") + "/chat"

    payload = {"message": message, "history": history if history else []}

    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        return data  # Return full dict (includes crisis, severity, response, etc.)
    except requests.Timeout:
        return {
            "response": (
                "The local assistant is taking longer than expected to respond. "
                "Please try again in a moment."
            ),
            "crisis": False,
            "severity": None,
        }
    except requests.ConnectionError:
        return {
            "response": "The chat backend is unavailable. Please start FastAPI and try again.",
            "crisis": False,
            "severity": None,
        }
    except requests.HTTPError as exc:
        try:
            detail = exc.response.json().get("detail", "Chat request failed")
        except (ValueError, requests.exceptions.JSONDecodeError):
            detail = (exc.response.text or "Chat request failed").strip()[:300]
        return {
            "response": f"The assistant could not complete this request: {detail}",
            "crisis": False,
            "severity": None,
        }
    except (ValueError, requests.exceptions.JSONDecodeError):
        return {
            "response": "The assistant returned an invalid response. Please try again.",
            "crisis": False,
            "severity": None,
        }


def _insight_chips(data: dict) -> str:
    """Render non-diagnostic model predictions returned by FastAPI."""
    if not data or not data.get("emotion"):
        return ""
    emotion = str(data.get("emotion", "Unknown")).title()
    emotion_conf = float(data.get("emotion_confidence", 0) or 0)
    stress = str(data.get("stress", "Unknown"))
    stress_conf = float(data.get("stress_confidence", 0) or 0)
    depression = str(data.get("depression", "Unknown"))
    depression_conf = float(data.get("depression_confidence", 0) or 0)
    return (
        '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:5px 0 12px 48px;">'
        f'<span style="background:#eef2ff;color:#4338ca;padding:4px 9px;border-radius:12px;font-size:11px;">'
        f'🧠 Emotion: {emotion} ({emotion_conf:.0f}%)</span>'
        f'<span style="background:#fff7ed;color:#c2410c;padding:4px 9px;border-radius:12px;font-size:11px;">'
        f'⚡ Stress: {stress} ({stress_conf:.0f}%)</span>'
        f'<span style="background:#f0fdf4;color:#15803d;padding:4px 9px;border-radius:12px;font-size:11px;">'
        f'🛡️ Depression signal: {depression} ({depression_conf:.0f}%)</span>'
        '</div>'
    )


def _record_trajectory(data: dict) -> None:
    """Store non-clinical per-turn model signals for a session chart."""
    if not data or not data.get("emotion"):
        return
    trajectory = st.session_state.setdefault("emotion_trajectory", [])
    trajectory.append({
        "turn": len(trajectory) + 1,
        "emotion_confidence": float(data.get("emotion_confidence", 0) or 0),
        "stress_confidence": float(data.get("stress_confidence", 0) or 0),
        "depression_confidence": float(data.get("depression_confidence", 0) or 0),
        "emotion": str(data.get("emotion")),
    })


def _show_exercise_recommendation(data: dict, key_suffix: str = "live", container=None) -> None:
    if data.get("stress") != "Stress" or float(data.get("stress_confidence", 0) or 0) < 80:
        return
    target = container if container is not None else st
    target.markdown("""
    <div class="exercise-prompt">
        <div class="exercise-prompt-icon">✦</div>
        <div>
            <div class="exercise-prompt-title">A gentle reset may help</div>
            <div class="exercise-prompt-copy">Your message contains a high stress signal. You can try a short guided breathing exercise whenever you feel ready.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    action_columns = target.columns([1, 1.5, 1])
    with action_columns[1]:
        with st.container(key=f"exercise_action_{key_suffix}"):
            if st.button(
                "✦  Try a breathing exercise",
                key=f"exercise_{key_suffix}",
                use_container_width=True,
            ):
                st.session_state["current_page"] = "Exercises"
                st.session_state["page"] = "exercises"
                st.query_params["page"] = "Exercises"
                st.rerun()
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
        padding-bottom: 112px !important;
    }
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 112px !important;
        max-width: 100% !important;
    }
    /* ── SAFETY BANNER ── */
    .chat-disclaimer {
        display: flex;
        align-items: center;
        gap: 9px;
        width: 100%;
        margin: 0 0 12px;
        padding: 10px 14px;
        border: 1px solid #ddd6fe;
        border-radius: 10px;
        background: linear-gradient(100deg, #f5f3ff 0%, #f8f7ff 100%);
        color: #51466f;
        font-size: 12px;
        box-sizing: border-box;
        line-height: 1.45;
    }
    .chat-disclaimer b { color: #5b3fa6; }
    .chat-disclaimer-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #e9e3ff;
        color: #674db5;
        font-size: 14px;
        flex: 0 0 auto;
    }
    .chat-status-row {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 6px;
        min-height: 24px;
        margin: 0 2px 6px;
        color: #64748b;
        font-size: 12px;
        font-weight: 600;
    }
    .exercise-prompt {
        display:flex;
        align-items:flex-start;
        gap:10px;
        margin: 4px 0 0 44px;
        padding: 11px 13px;
        border: 1px solid rgba(16,185,129,0.22);
        border-radius: 13px;
        background: linear-gradient(135deg, #f0fdf9, #f0f9ff);
        color:#475569;
    }
    .exercise-prompt-icon {
        display:flex;
        align-items:center;
        justify-content:center;
        width:25px;
        height:25px;
        border-radius:50%;
        background:#d1fae5;
        color:#059669;
        flex:0 0 auto;
    }
    .exercise-prompt-title { color:#065f46; font-size:12px; font-weight:800; }
    .exercise-prompt-copy { margin-top:2px; font-size:11px; line-height:1.45; }
    [class*="st-key-exercise_action_"] {
        margin: 14px auto 12px !important;
    }
    [class*="st-key-exercise_action_"] button {
        min-height: 38px !important;
        padding: 7px 14px !important;
        border: 1px solid #d8d2f2 !important;
        border-radius: 20px !important;
        background: #f5f3ff !important;
        color: #5145a8 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-align: center !important;
        box-shadow: 0 2px 8px rgba(81,69,168,.08) !important;
    }
    [class*="st-key-exercise_action_"] button:hover {
        background: #ede9fe !important;
        border-color: #b9adeb !important;
        color: #43358f !important;
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
        padding: 10px 24px 12px 24px;
        scroll-behavior: smooth;
        scroll-margin-bottom: 12px;
    }

    /* Streamlit's keyed container becomes the only scrolling surface. */
    .st-key-chat_messages {
        border: none !important;
        border-radius: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        margin: 0 !important;
        min-height: 0 !important;
    }
    .st-key-chat_messages [data-testid="stVerticalBlock"] {
        padding: 4px 8px 12px !important;
        gap: 16px !important;
    }
    .st-key-chat_messages [data-testid="stVerticalBlockBorderWrapper"] {
        border: 0 !important;
        background: transparent !important;
    }
    .st-key-chat_messages [data-testid="stVerticalBlock"] {
        gap: 14px !important;
    }
    .st-key-chat_messages [data-testid="stElementContainer"] {
        margin: 0 !important;
    }

    /* ── MESSAGE ROWS ── */
    .chat-row {
        display: flex;
        margin: 0 !important;
        padding: 4px 0 12px;
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
        max-width: min(72%, 760px);
        word-wrap: break-word;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
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
        overflow-wrap: anywhere;
    }
    
    
    /* ── EMPTY STATE ── */
    .empty-state {
        text-align: center;
        padding: 38px 20px 28px;
        color: #64748b;
    }
    .empty-state-icon {
        width: 54px;
        height: 54px;
        margin: 0 auto 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #c4b5fd;
        border-radius: 16px;
        background: #f5f3ff;
        color: #6d5bd0;
        font-size: 24px;
        font-weight: 700;
    }
    .empty-state h3 {
        font-size: 20px;
        font-weight: 700;
        color: #4338ca;
        margin: 0 0 8px;
    }
    .empty-state p {
        font-size: 14px;
        color: #4a5568;
        margin: 0;
        line-height: 1.6;
    }
    .quick-start-label {
        margin: 20px 0 9px;
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .st-key-quick_start button {
        min-height: 56px !important;
        padding: 12px 16px !important;
        border: 1px solid rgba(99,102,241,.16) !important;
        border-radius: 14px !important;
        background: linear-gradient(145deg, rgba(255,255,255,.96), rgba(245,243,255,.88)) !important;
        color: #3f4662 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        white-space: normal !important;
        box-shadow: 0 3px 10px rgba(51,65,85,.045) !important;
        backdrop-filter: blur(8px) !important;
        transition: transform .18s ease, background .18s ease, box-shadow .18s ease, border-color .18s ease !important;
    }
    .st-key-quick_start button:hover {
        background: linear-gradient(145deg, #ffffff, #f0edff) !important;
        border-color: #aaa0e9 !important;
        color: #4f46a5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 18px rgba(99,102,241,.12) !important;
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
        background: rgba(246,247,251,0.82) !important;
        backdrop-filter: blur(14px) !important;
        border-top: none !important;
        padding: 6px 12px 8px !important;
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
        height: 82px !important;
        border: none !important;
        display: block !important;
    }

    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-disclaimer">
        <span class="chat-disclaimer-icon">!</span>
        <span><b>Wellness support, not medical care.</b> MindCare AI is not a doctor or crisis hotline. In an emergency, contact local emergency services or a qualified professional.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-status-row">
        <span class="status-dot"></span>
        <span>MindCare AI is available</span>
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

    # ── MESSAGES: this keyed Streamlit container is the only scrollable area ──
    message_container = st.container(height=560, key="chat_messages")
    with message_container:
        if not st.session_state["chat_history"]:
            st.markdown("""
            <div class="empty-state">
                <span class="empty-state-icon">🧠</span>
                <h3>Hello, I'm here for you</h3>
                <p>Share what is on your mind in this private, judgment-free space.</p>
            </div>
            """, unsafe_allow_html=True)
            quick_input = None
            with st.container(key="quick_start"):
                st.markdown('<div class="quick-start-label">You can start with</div>', unsafe_allow_html=True)
                quick_cols = st.columns(3)
                quick_prompts = [
                    ("◌  I feel anxious", {"type": "text", "data": "I feel anxious"}),
                    ("〰  Try a breathing exercise", {"type": "navigate", "page": "Exercises"}),
                    ("◉  Help me track my mood", {"type": "navigate", "page": "Mood Analytics"}),
                ]
                for column, (label, action) in zip(quick_cols, quick_prompts):
                    with column:
                        if st.button(label, key=f"quick_{label}", use_container_width=True):
                            quick_input = action
        else:
            quick_input = None
            for idx, (role, msg) in enumerate(st.session_state["chat_history"]):
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-row" style="justify-content:flex-end;">
                        <div class="user-bubble">{msg}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
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
                            <div class="ai-avatar">✦</div>
                            <div class="assistant-bubble">{msg}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    insight = st.session_state.get("_insight_metadata", {}).get(idx)
                    if insight and not (crisis_meta and crisis_meta.get("crisis")):
                        st.markdown(_insight_chips(insight), unsafe_allow_html=True)
                        _show_exercise_recommendation(insight, key_suffix=f"history_{idx}")

    # ══════════════════════════════════════════════════════
    # PHASE 2a — show dots, call AI, store response, rerun
    # ══════════════════════════════════════════════════════
    if st.session_state.get("_ai_thinking"):
        message_container.markdown("""
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
            "insights": response_data,
        }
        st.rerun()

    # ══════════════════════════════════════════════════════
    # PHASE 2b — typewriter: one character at a time
    # ══════════════════════════════════════════════════════
    elif st.session_state.get("_ai_typing"):
        data         = st.session_state.pop("_ai_typing")
        pending_type = data["type"]
        response     = data["response"]
        data_crisis  = data.get("crisis", False)
        data_severity = data.get("severity")
        insight_data = data.get("insights", {})

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
            message_container.markdown(
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

        import html as _html
        safe_response = _html.escape(response).replace("\n", "<br>")
        message_container.markdown(
            f'<div class="chat-row" style="justify-content:flex-start;">'
            f'<div class="ai-bubble-wrap">'
            f'<div class="ai-avatar">🧠</div>'
            f'<div class="assistant-bubble">{safe_response}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        if not data_crisis:
            message_container.markdown(_insight_chips(insight_data), unsafe_allow_html=True)
            _record_trajectory(insight_data)
            _show_exercise_recommendation(
                insight_data,
                key_suffix="live",
                container=message_container,
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
        if "_insight_metadata" not in st.session_state:
            st.session_state["_insight_metadata"] = {}
        st.session_state["_insight_metadata"][message_index] = insight_data

        trajectory = st.session_state.get("emotion_trajectory", [])
        if trajectory:
            import pandas as pd
            message_container.caption("Session model signals (not a clinical measurement)")
            message_container.line_chart(pd.DataFrame(trajectory).set_index("turn")[["emotion_confidence", "stress_confidence", "depression_confidence"]])

        if pending_type == "voice":
            speak_and_auto_play(response)

        st.session_state["component_key_timestamp"] = time.time()
        st.rerun()

    # Add an anchor as the last item in the fixed-height Streamlit container.
    # The JS bridge scrolls the container's native overflow element to this anchor.
    msg_count = len(st.session_state["chat_history"])
    message_container.markdown(
        f'<div class="chat-scroll-anchor" data-message-count="{msg_count}"></div>',
        unsafe_allow_html=True,
    )
    components.html(f"""
    <script>
    (function(){{
        function scrollToLatest(){{
            try{{
                var doc = window.parent.document;
                var root = doc.querySelector('.st-key-chat_messages');
                if(!root) return false;
                var anchor = root.querySelector('.chat-scroll-anchor');
                var node = anchor ? anchor.parentElement : root;
                while(node && node !== root.parentElement){{
                    var style = window.parent.getComputedStyle(node);
                    var canScroll = /(auto|scroll)/.test(style.overflowY)
                        && node.scrollHeight > node.clientHeight + 2;
                    if(canScroll){{
                        node.scrollTop = node.scrollHeight;
                        node.scrollTo({{top: node.scrollHeight, behavior: 'smooth'}});
                        return true;
                    }}
                    node = node.parentElement;
                }}
                return false;
            }}catch(e){{ return false; }}
        }}
        function install(){{
            var root;
            try{{ root = window.parent.document.querySelector('.st-key-chat_messages'); }}catch(e){{ return; }}
            if(!root) return;
            scrollToLatest();
            if(!root._mindcareScrollObserver){{
                root._mindcareScrollObserver = new MutationObserver(function(){{
                    requestAnimationFrame(scrollToLatest);
                }});
                root._mindcareScrollObserver.observe(root, {{childList:true, subtree:true, characterData:true}});
            }}
        }}
        for(var attempt=0; attempt<15; attempt++) setTimeout(install, attempt*120);
        setTimeout(scrollToLatest, 2000);
    }})();
    </script>
    """, height=0, scrolling=False)

    # ===== REACT COMPONENT - STICKY CHAT BAR =====
    # Use timestamp in key to force component reset after each message
    if "component_key_timestamp" not in st.session_state:
        st.session_state["component_key_timestamp"] = time.time()
    
    component_key = f"chat_input_{cid if cid else 'new'}_{st.session_state['component_key_timestamp']}"
    component_input = sticky_chat_bar(key=component_key)
    user_input = quick_input or component_input

    # ================= HANDLE INPUT FROM REACT COMPONENT =================
    # Guard: skip if we're already in a thinking/typing phase
    if user_input and not st.session_state.get("_ai_thinking") and not st.session_state.get("_ai_typing"):
        if user_input.get("type") == "navigate":
            destination = user_input["page"]
            st.session_state["current_page"] = destination
            st.query_params["page"] = destination
            st.rerun()

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
