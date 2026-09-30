# -*- coding: utf-8 -*-
import streamlit as st
import os
import requests


def generate_demo_response(message: str, history: list) -> str:
    """Use the same FastAPI /chat endpoint as the full Chat page."""
    url = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/") + "/chat"
    try:
        response = requests.post(
            url,
            json={"message": message, "history": history},
            timeout=180,
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("response")
        if not isinstance(answer, str) or not answer.strip():
            return "I couldn't generate a response just now. Please try again."
        return answer
    except requests.Timeout:
        return "The assistant is taking longer than expected. Please try again in a moment."
    except requests.ConnectionError:
        return "The chat backend is unavailable. Please try again shortly."
    except requests.HTTPError as exc:
        try:
            detail = exc.response.json().get("detail", "Chat request failed")
        except (ValueError, AttributeError):
            detail = "Chat request failed"
        return f"The assistant could not complete this request: {detail}"
    except (ValueError, requests.RequestException):
        return "The assistant returned an invalid response. Please try again."

def show_demo_chat():

    # ===== INITIALIZATION =====
    if "demo_messages" not in st.session_state:
        st.session_state.demo_messages = [
            {"role": "assistant", "content": "👋 Welcome! How can I support you today?"}
        ]

    if "demo_msg_count" not in st.session_state:
        st.session_state.demo_msg_count = 0

    if "trial_ended" not in st.session_state:
        st.session_state.trial_ended = False

    # ===== DEMO PAGE PRESENTATION =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding: 0.15rem 2rem 7rem !important;
            max-width: 1040px !important;
        }
        div[data-testid="stAppViewBlockContainer"] { padding-top: .15rem !important; }
        .stApp {
            background: radial-gradient(ellipse at 12% 0%, rgba(196,181,253,.24), transparent 38%),
                        linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
            color: #1E293B;
        }

        .chat-row {
            display: flex;
            margin-bottom: 24px;
            animation: msgFadeIn 0.35s ease;
        }
        @keyframes msgFadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 18px 0;
        }
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

        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin: 18px 0;
        }

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
        .trial-counter {
            display: inline-block;
            font-size: 13px;
            margin: 2px auto 16px;
            padding: 7px 14px;
            border: 1px solid rgba(99,102,241,.15);
            border-radius: 999px;
            background: rgba(99,102,241,.09);
            color: #5B4ACB;
            font-weight: 600;
        }
        .starter-heading { margin: 0 0 12px; color: #64748B; font-size: 13px; font-weight: 600; text-align:center; }
        .st-key-demo_starter_prompts [data-testid="stHorizontalBlock"] { gap: 10px; }
        .st-key-demo_starter_prompts button {
            background: rgba(255,255,255,.85) !important;
            color: #4A5568 !important;
            border: 1px solid rgba(99,102,241,.12) !important;
            border-radius: 14px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            box-shadow: 0 3px 12px rgba(99,102,241,.04) !important;
            min-height: 54px;
            white-space: normal !important;
        }
        .st-key-demo_starter_prompts button:hover {
            background: #fff !important;
            border-color: #6366F1 !important;
            box-shadow: 0 8px 20px rgba(99,102,241,.12) !important;
            transform: translateY(-2px) !important;
        }
        [data-testid="stDialog"]::backdrop { background: rgba(30,41,59,.28); backdrop-filter: blur(8px); }
        [data-testid="stDialog"] > div { border: 1px solid rgba(99,102,241,.16); border-radius: 22px; }
        [data-testid="stDialog"] [data-testid="stMarkdownContainer"] p { color: #475569; line-height: 1.6; }
        [data-testid="stDialog"] .stButton > button { width: 100%; min-height: 44px; }
       .stButton > button {
            background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
            color: #fff !important;
            border: 1px solid rgba(99,102,241,.18) !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            box-shadow: 0 5px 14px rgba(99,102,241,.18) !important;
            transition: transform .2s ease, box-shadow .2s ease, filter .2s ease !important;
        }
        .stButton > button:hover {
            filter: brightness(1.04) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 22px rgba(99,102,241,.25) !important;
        }
        /* Compact top-left back arrow. */
        .st-key-demo_back_arrow .stButton > button {
            background: rgba(255,255,255,.78) !important;
            color: #4F46E5 !important;
            border-color: rgba(99,102,241,.2) !important;
            border-radius: 50% !important;
            width: 38px;
            height: 38px;
            padding: 0 !important;
            font-size: 20px !important;
        }
        div[data-testid="stChatInput"] {
            width: 100% !important;
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            background: transparent !important;
            padding: 0 0 10px !important;
            margin: 0 auto 12px !important;
            min-height: auto !important;
        }
        div[data-testid="stChatInput"] > div {
            width: 100% !important;
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 28px !important;
            box-shadow: 0 4px 12px rgba(99,102,241,.08) !important;
            max-width: 1000px !important;
            margin: 0 auto !important;
        }
        div[data-testid="stBottom"],
        div[data-testid="stBottomBlockContainer"],
        div[data-testid="stBottom"] > div {
            background: transparent !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-bottom: 0 !important;
            min-height: auto !important;
            box-shadow: none !important;
        }
        .main .block-container {
            max-width: 1100px !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 80px !important;
        }
        div[data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #1E293B !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder { color: #94A3B8 !important; }
        div[data-testid="stChatInput"] button {
            background: #6366F1 !important;
            color: #fff !important;
            border-radius: 50% !important;
        }
        div[data-testid="stChatInput"] button:hover { background: #4F46E5 !important; }
        /* Streamlit versions with speech input expose a microphone button here. */
        div[data-testid="stChatInput"] button[aria-label*="voice" i],
        div[data-testid="stChatInput"] button[aria-label*="microphone" i],
        div[data-testid="stChatInput"] button[title*="voice" i],
        div[data-testid="stChatInput"] button[title*="microphone" i],
        div[data-testid="stChatInput"] button[aria-label*="audio" i],
        div[data-testid="stChatInput"] button[title*="audio" i] {
            display: none !important;
        }
        @media (max-width: 640px) {
            .main .block-container { padding: 0.1rem 1rem 80px !important; }
            .user-bubble { max-width: 88%; }
        }
    </style>
    """, unsafe_allow_html=True)
    # ===== TOP-LEFT BACK ARROW =====
    with st.container(key="demo_back_arrow"):
        if st.button("←", key="top_left_back_arrow", help="Back to Home"):
            st.session_state.page = "home"
            st.rerun()

    # ===== LOGIC =====
    remaining = 5 - st.session_state.demo_msg_count
    if remaining <= 0:
        st.session_state.trial_ended = True

    if not st.session_state.trial_ended:
        st.markdown(
            f'<div class="trial-counter">✨ {remaining} Free messages left ✨</div>',
            unsafe_allow_html=True,
        )
    else:
        @st.dialog("You've Used All 5 Free Messages! 🎉")
        def show_trial_modal():
            st.write("Unlock unlimited chats, personalized mood tracking, and digital journaling by creating a free account.")
            if st.button("Sign Up for Unlimited Access", key="demo_signup", type="primary", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "signup"
                st.rerun()
            if st.button("Already have an account? Log In", key="demo_login", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "login"
                st.rerun()
        show_trial_modal()

    # ===== QUICK STARTER PROMPTS =====
    if not st.session_state.trial_ended and st.session_state.demo_msg_count == 0:
        with st.container(key="demo_starter_prompts"):
            st.markdown('<p class="starter-heading">Not sure where to start? Try one of these</p>', unsafe_allow_html=True)
            prompts = [
                "I am feeling anxious.",
                "Give me some tips to overcome anxiety.",
                "I am feeling lonely today.",
            ]
            prompt_cols = st.columns(3)
            selected_prompt = None
            for prompt_index, (prompt_col, prompt) in enumerate(zip(prompt_cols, prompts)):
                with prompt_col:
                    if st.button(prompt, key=f"demo_starter_{prompt_index}", use_container_width=True):
                        selected_prompt = prompt

    # ===== CHAT DISPLAY =====
    for msg in st.session_state.demo_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="ai-bubble-wrap">
                    <div class="ai-avatar">🧠</div>
                    <div class="assistant-bubble">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ===== INPUT =====
    if not st.session_state.trial_ended:
        user_input = selected_prompt if 'selected_prompt' in locals() and selected_prompt else st.chat_input("Share what's on your mind...", key="demo_chat_input")

        if user_input:
            st.session_state.demo_messages.append(
                {"role": "user", "content": user_input}
            )
            st.session_state.demo_msg_count += 1

            history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.demo_messages[:-1]
                if msg.get("role") in ("user", "assistant")
            ][-6:]
            st.session_state.demo_messages.append(
                {"role": "assistant", "content": generate_demo_response(user_input, history)}
            )

            st.rerun()
