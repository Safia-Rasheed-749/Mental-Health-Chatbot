import streamlit as st
import requests

# =====================================================
# Backend API Call
# =====================================================

BACKEND_URL = "http://127.0.0.1:8000/chat"

_FALLBACK_RESPONSES = [
    "I'm here for you. It's okay to not feel okay sometimes. Your feelings are valid.",
    "Tell me more about what's on your mind. You're not alone in this.",
    "You don't have to face this alone. Whatever you're going through, I'm here to listen.",
    "Be gentle with yourself today. You deserve compassion and care.",
]

def get_demo_response(message: str) -> str:
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": message},
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "I'm here to listen. Can you tell me more?")

    except requests.exceptions.ConnectionError:
        return (
            "I'm here for you. "
            "(Note: AI service is starting up — please try again in a moment.)"
        )
    except requests.exceptions.Timeout:
        return (
            "I'm taking a little longer than usual to respond. "
            "Please send your message again."
        )
    except Exception:
        import random
        return random.choice(_FALLBACK_RESPONSES)

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

    # ===== CSS (CLEAN PROFESSIONAL LOOK) =====
    st.markdown("""
    <style>
        /* ===== FONT ===== */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ===== HIDE STREAMLIT CHROME ===== */
        header, footer, .stDeployButton {
            display: none !important;
        }

        /* ===== PAGE BACKGROUND ===== */
        .stApp {
            background: #f8fafc !important;
        }

        /* ===== CONTAINER ===== */
        .block-container {
            max-width: 820px !important;
            margin: 0 auto !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }

        /* ===== TOP BAR ===== */
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0 18px 0;
            border-bottom: 1px solid #eef2f7;
            margin-bottom: 8px;
        }
        .topbar-brand {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            letter-spacing: -0.2px;
        }
        .topbar-brand span {
            font-weight: 400;
            color: #94a3b8;
            font-size: 12px;
            margin-left: 6px;
        }

        /* ===== HOME BUTTON (subtle outline) ===== */
        div[data-testid="stButton"] > button {
            background: #ffffff !important;
            color: #475569 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            padding: 6px 14px !important;
            box-shadow: 0 1px 2px rgba(15,23,42,0.04) !important;
            transition: all 0.15s ease !important;
        }
        div[data-testid="stButton"] > button:hover {
            background: #f8fafc !important;
            border-color: #cbd5e1 !important;
            color: #1e293b !important;
            transform: none !important;
            box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
        }

        /* ===== PRIMARY BUTTON (Create Free Account) ===== */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: #ffffff !important;
            border: none !important;
        }

        /* ===== CHAT BUBBLES ===== */
        @keyframes msgFadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 16px 0;
            animation: msgFadeIn 0.3s ease;
        }
        .user-bubble {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #ffffff;
            padding: 11px 16px;
            border-radius: 18px 18px 4px 18px;
            font-size: 14px;
            line-height: 1.55;
            max-width: 72%;
            word-wrap: break-word;
            box-shadow: 0 2px 8px rgba(99,102,241,0.20);
        }

        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin: 16px 0;
            animation: msgFadeIn 0.3s ease;
        }
        .ai-bubble-wrap {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            max-width: 78%;
        }
        .ai-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            flex-shrink: 0;
            box-shadow: 0 1px 4px rgba(99,102,241,0.25);
            margin-top: 2px;
        }
        .assistant-bubble {
            background: #ffffff;
            color: #1e293b;
            padding: 12px 16px;
            border-radius: 4px 18px 18px 18px;
            font-size: 14px;
            line-height: 1.65;
            word-wrap: break-word;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05), 0 1px 2px rgba(15,23,42,0.03);
            border: 1px solid #f1f5f9;
        }

        /* ===== TRIAL BOX (softer) ===== */
        .trial-box {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            padding: 20px 18px;
            border-radius: 14px;
            text-align: center;
            margin: 20px 0 16px 0;
            color: white;
            box-shadow: 0 4px 16px rgba(99,102,241,0.18);
        }
        .trial-title {
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.2px;
        }
        .trial-counter {
            color: #ffffff;
            background: rgba(255,255,255,0.18);
            padding: 5px 12px;
            border-radius: 999px;
            display: inline-block;
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0.2px;
            margin-top: 8px;
        }

        /* ===== TRIAL COMPLETE CARD ===== */
        .trial-complete-container {
            text-align: center;
            background: #ffffff;
            color: #1e293b;
            margin: 20px 0;
            padding: 24px 20px;
            border-radius: 14px;
            border: 1px solid #eef2f7;
            box-shadow: 0 2px 8px rgba(15,23,42,0.04);
        }
        .trial-complete-container h3 {
            margin: 0 0 6px 0;
            font-size: 18px;
            font-weight: 600;
        }
        .trial-complete-container p {
            margin: 0;
            color: #64748b;
            font-size: 14px;
        }

        /* ===== CHAT INPUT (no red ring) ===== */
        div[data-testid="stChatInput"] {
            background-color: #ffffff !important;
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(15,23,42,0.04) !important;
        }
        div[data-testid="stChatInput"]:focus-within {
            border-color: #a5b4fc !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
        }
        div[data-testid="stChatInput"] textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #94a3b8 !important;
        }

        /* ===== SUBTLE HR ===== */
        hr {
            border: none !important;
            border-top: 1px solid #eef2f7 !important;
            margin: 16px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== TOP BAR =====
    # Brand on left, Home button on right — but Streamlit columns
    # align vertically, so we use a flex container with st.button
    # positioned via column ratio.
    brand_col, home_col = st.columns([5, 1])
    with brand_col:
        st.markdown(
            "<div class='topbar-brand'>🧠 MindCare AI"
            "<span>· Demo</span></div>",
            unsafe_allow_html=True,
        )
    with home_col:
        if st.button("← Home", use_container_width=True, key="home_btn"):
            st.session_state.page = "home"
            st.rerun()

    # Thin divider under top bar
    st.markdown(
        "<div style='border-bottom:1px solid #eef2f7;margin-bottom:14px;'></div>",
        unsafe_allow_html=True,
    )

    # ===== LOGIC =====
    remaining = 5 - st.session_state.demo_msg_count
    if remaining <= 0:
        st.session_state.trial_ended = True

    # ===== TRIAL BOX =====
    if not st.session_state.trial_ended:
        st.markdown(f"""
        <div class="trial-box">
            <div class="trial-title">✨ Try MindCare AI</div>
            <div class="trial-counter">{remaining} free messages left</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="trial-complete-container">
            <h3>✨ Trial Complete</h3>
            <p>Create an account for unlimited access</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Create Free Account", use_container_width=True, type="primary", key="create_acc"):
                st.session_state.page = "auth"
                st.rerun()

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
        user_input = st.chat_input("How can I help you?")

        if user_input:
            st.session_state.demo_messages.append(
                {"role": "user", "content": user_input}
            )
            st.session_state.demo_msg_count += 1

            with st.spinner("MindCare AI is thinking..."):
                ai_response = get_demo_response(user_input)

            st.session_state.demo_messages.append(
                {"role": "assistant", "content": ai_response}
            )

            st.rerun()