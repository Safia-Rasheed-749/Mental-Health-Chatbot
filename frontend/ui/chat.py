# frontend/ui/chat.py
"""Chat UI module for MindCare AI.
Provides a `show_chat(user_id)` function that renders the chat interface.
All UI logic is encapsulated inside this function so that `frontend/app.py`
can call `chat.show_chat(user_id)` without encountering an AttributeError.
"""

import os
import sys
import time
import base64
import tempfile
import requests
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from db import add_message, create_conversation, get_messages_by_conversation, log_user_activity
from layout_utils import apply_clean_layout
from components.sticky_chat import sticky_chat_bar

# Force ffmpeg path for pydub
os.environ["PATH"] = r"C:\\ffmpeg\\ffmpeg-8.1-essentials_build\\bin" + os.pathsep + os.environ.get("PATH", "")
from pydub import AudioSegment
AudioSegment.converter = r"C:\\ffmpeg\\ffmpeg-8.1-essentials_build\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\\ffmpeg\\ffmpeg-8.1-essentials_build\\bin\\ffprobe.exe"
from pydub.utils import which
AudioSegment._ffmpeg = which("ffmpeg")
AudioSegment._ffprobe = which("ffprobe")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def speak_and_auto_play(text: str) -> None:
    """Convert *text* to speech, store as base64, and auto‑play via HTML audio.
    The generated base64 data is kept in ``st.session_state['auto_play_audio']``
    and cleared after rendering.
    """
    tts = gTTS(text=text, lang="en")
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(audio_path)
    with open(audio_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()
    st.session_state["auto_play_audio"] = audio_base64
    try:
        os.unlink(audio_path)
    except Exception:
        pass

def generate_response_from_backend(message: str) -> dict:
    """POST *message* to the FastAPI backend and return the full JSON payload.
    Expected keys: ``response``, ``emotion``, ``emotion_confidence``, ``stress``,
    ``stress_confidence``, ``depression``, ``depression_confidence``.
    """
    url = "http://127.0.0.1:8000/chat"
    resp = requests.post(url, json={"message": message}, timeout=300)
    resp.raise_for_status()
    return resp.json()

def render_signal_chips(payload: dict) -> str:
    """Return HTML for AI‑signal chips and disclaimer based on *payload*.
    The helper formats confidence values as percentages.
    """
    def fmt(val):
        try:
            v = float(val)
            if 0 <= v <= 1:
                return f"{int(v*100)}%"
            return str(val)
        except Exception:
            return str(val)
    chips = []
    if payload.get("emotion"):
        chips.append(f'<span class="chip">Emotion: {payload["emotion"]} {fmt(payload.get("emotion_confidence"))}</span>')
    if payload.get("stress"):
        chips.append(f'<span class="chip">Stress: {payload["stress"]} {fmt(payload.get("stress_confidence"))}</span>')
    if payload.get("depression"):
        chips.append(f'<span class="chip">Depression: {payload["depression"]} {fmt(payload.get("depression_confidence"))}</span>')
    chip_html = " ".join(chips)
    disclaimer = "<div class=\"disclaimer\">These AI signals are not a medical diagnosis.</div>"
    style = "<style>.chip{background:#f0f0f0;color:#333;padding:4px 8px;border-radius:8px;margin-right:4px;font-size:12px;}.disclaimer{font-size:12px;color:#777;margin-top:4px;}</style>"
    return style + f"<div class=\"chips\">{chip_html}</div>{disclaimer}"

# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def show_chat(user_id: str) -> None:
    """Render the full chat UI for *user_id*.
    This function contains the original module‑level UI logic, now wrapped
    inside a callable so that ``frontend/app.py`` can invoke ``chat.show_chat``
    without raising an ``AttributeError``.
    """
    # Initialise session state variables if they do not exist
    for key, default in [
        ("chat_history", []),
        ("conversation_id", None),
        ("last_loaded_chat", None),
        ("voice_processed_key", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # Apply layout cleanup (original call was at module top)
    apply_clean_layout(hide_header_completely=False)

    # -------------------------------------------------------------------
    # CSS & header rendering (trimmed for brevity – original CSS retained)
    # -------------------------------------------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        .stAppDeployButton {display:none;}
        #MainMenu {visibility:hidden !important;}
        footer {visibility:hidden !important;}
        header {background:transparent !important;box-shadow:none !important;visibility:visible !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="chat-header">
            <div class="chat-header-avatar">🧠</div>
            <div class="chat-header-text">
                <h1>MindCare AI</h1>
                <p>Your personal mental wellness companion</p>
            </div>
            <div class="chat-header-status"><div class="status-dot"></div>Available</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Auto‑play audio if pending
    if "auto_play_audio" in st.session_state:
        audio_base64 = st.session_state["auto_play_audio"]
        st.markdown(
            f"""
            <audio autoplay style=\"display:none;\">
                <source src=\"data:audio/mp3;base64,{audio_base64}\" type=\"audio/mpeg\">
            </audio>
            <script>document.querySelector('audio').play();</script>
            """,
            unsafe_allow_html=True,
        )
        del st.session_state["auto_play_audio"]

    # -------------------------------------------------------------------
    # Conversation handling
    # -------------------------------------------------------------------
    cid = st.session_state.get("conversation_id")
    if cid and st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid

    # -------------------------------------------------------------------
    # Message list rendering
    # -------------------------------------------------------------------
    st.markdown('<div class="chat-area" id="chat-messages">', unsafe_allow_html=True)
    if not st.session_state["chat_history"]:
        st.markdown(
            """
            <div class="empty-state">
                <span class="empty-state-icon">🌿</span>
                <h3>Hello, I'm here for you</h3>
                <p>Feel free to share anything on your mind.<br>This is a safe, judgment‑free space.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for role, msg in st.session_state["chat_history"]:
            if role == "user":
                st.markdown(
                    f"""
                    <div class="chat-row" style="justify-content:flex-end;">
                        <div class="user-bubble">{msg}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-row" style="justify-content:flex-start;">
                        <div class="ai-bubble-wrap">
                            <div class="ai-avatar">🧠</div>
                            <div class="assistant-bubble">{msg}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # -------------------------------------------------------------------
    # Phase 2a – AI thinking (call backend)
    # -------------------------------------------------------------------
    if st.session_state.get("_ai_thinking"):
        st.markdown(
            """
            <div class="chat-row" style="justify-content:flex-start;">
                <div class="ai-bubble-wrap">
                    <div class="ai-avatar">🧠</div>
                    <div class="assistant-bubble" style="padding:14px 18px;min-width:70px;">
                        <div class="thinking-dots"><span></span><span></span><span></span></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        pending = st.session_state.pop("_ai_thinking")
        pending_type = pending["type"]
        pending_text = pending["text"]
        payload = generate_response_from_backend(pending_text)
        response_text = payload.get("response", "")
        st.session_state["_ai_typing"] = {"type": pending_type, "payload": payload, "response": response_text}
        st.rerun()

    # -------------------------------------------------------------------
    # Phase 2b – typewriter effect + signal chips
    # -------------------------------------------------------------------
    elif st.session_state.get("_ai_typing"):
        import html as _html
        data = st.session_state.pop("_ai_typing")
        pending_type = data["type"]
        payload = data.get("payload", {})
        response = data["response"]
        safe = _html.escape(response)
        slot = st.empty()
        for i in range(1, len(safe) + 1):
            slot.markdown(
                f'<div class="chat-row" style="justify-content:flex-start;">'
                f'<div class="ai-bubble-wrap">'
                f'<div class="ai-avatar">🧠</div>'
                f'<div class="assistant-bubble" style="white-space:pre-wrap;">{safe[:i]}'
                f'<span style="display:inline-block;width:2px;height:1em;background:#8b5cf6;margin-left:1px;vertical-align:text-bottom;animation:cur 0.6s step-end infinite;"></span>'
                f'</div></div></div>'
                f'<style>@keyframes cur{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>',
                unsafe_allow_html=True,
            )
            time.sleep(0.01)
        slot.markdown(
            f'<div class="chat-row" style="justify-content:flex-start;">'
            f'<div class="ai-bubble-wrap">'
            f'<div class="ai-avatar">🧠</div>'
            f'<div class="assistant-bubble">{safe_response}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)
        st.markdown(render_signal_chips(payload), unsafe_allow_html=True)
        if pending_type == "voice":
            speak_and_auto_play(response)
        st.session_state["component_key_timestamp"] = time.time()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Auto‑scroll (identical to original implementation)
    # -------------------------------------------------------------------
    msg_count = len(st.session_state["chat_history"])
    st.markdown(
        f"""
        <script>
        (function(){{
            var key = 'sc_{msg_count}';
            if(window._sc === key) return;
            window._sc = key;
            function sc(){{
                try{{
                    var p = window.parent;
                    var el = p.document.querySelector('[data-testid=\"stAppViewContainer\"]');
                    if(!el) el = p.document.querySelector('section.main');
                    if(!el) el = p.document.documentElement;
                    if(el) el.scrollTop = el.scrollHeight + 9999;
                }}catch(e){{}}
            }}
            sc(); setTimeout(sc,120); setTimeout(sc,400); setTimeout(sc,800);
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------
    # Sticky chat bar component
    # -------------------------------------------------------------------
    if "component_key_timestamp" not in st.session_state:
        st.session_state["component_key_timestamp"] = time.time()
    component_key = f"chat_input_{cid if cid else 'new'}_{st.session_state['component_key_timestamp']}"
    component_input = sticky_chat_bar(key=component_key)
    user_input = quick_input or component_input

    # -------------------------------------------------------------------
    # Input handling (text or audio)
    # -------------------------------------------------------------------
    if user_input and not st.session_state.get("_ai_thinking") and not st.session_state.get("_ai_typing"):
        if not cid:
            cid = create_conversation(user_id)
            st.session_state["conversation_id"] = cid
            st.session_state["last_loaded_chat"] = cid
        if user_input["type"] == "text":
            text = user_input["data"]
            st.session_state["chat_history"].append(("user", text))
            add_message(user_id, "user", text, cid)
            try:
                log_user_activity(user_id, "Send Message", "Chat", f"Message: {text[:50]}...")
            except Exception as e:
                print(f"Activity logging error: {e}")
            st.session_state["component_key_timestamp"] = time.time()
            st.session_state["_ai_thinking"] = {"type": "text", "text": text}
            st.rerun()
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
                    except Exception:
                        pass
                    st.session_state["component_key_timestamp"] = time.time()
                    st.session_state["_ai_thinking"] = {"type": "voice", "text": voice_text}
                    st.rerun()
                else:
                    st.warning("Could not recognize speech. Please try again.")
            except sr.UnknownValueError:
                st.warning("Sorry, I couldn't understand that. Please speak clearly.")
            except Exception as e:
                st.error(f"Voice error: {str(e)}")

    # End of show_chat
