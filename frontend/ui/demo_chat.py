import streamlit as st
import random

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

    # ===== CSS (ORIGINAL PAGE STYLE + NEW CHAT BUBBLES) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }

        .stApp {
            background-color: #f6f7fb !important;
        }

        /* ===== NEW CHAT BUBBLE STYLES (FROM CHAT.PY) ===== */
        .chat-row {
            display: flex;
            margin-bottom: 24px;
            animation: msgFadeIn 0.35s ease;
        }
        @keyframes msgFadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ── USER BUBBLE (GRADIENT PURPLE) ── */
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

        /* ── AI BUBBLE (WHITE WITH AVATAR) ── */
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

        /* ===== ORIGINAL TRIAL BOX STYLING ===== */
        .trial-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 22px 18px;
            border-radius: 16px;
            text-align: center;
            margin-top: 30px;
            margin-bottom: 20px;
            color: white;
        }

        .trial-title {
            font-size: 22px;
            font-weight: bold;
        }

        .trial-counter {
            font-size: 18px;
            margin-top: 10px;
            color: #FFE66D;
            font-weight: 600;
        }

        .trial-complete-container {
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== LOGIC =====
    remaining = 5 - st.session_state.demo_msg_count
    if remaining <= 0:
        st.session_state.trial_ended = True

    # ===== TRIAL BOX =====
    if not st.session_state.trial_ended:
        st.markdown(f"""
        <div class="trial-box">
            <div class="trial-title">🤖 Try MindCare AI</div>
            <div class="trial-counter">✨ {remaining} Free messages left ✨</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="trial-complete-container">
            <h3>✨ Trial Complete!</h3>
            <p>Create an account for unlimited access</p>
        </div>
        """, unsafe_allow_html=True)

        # ===== CENTERED BUTTON =====
        col1, col2, col3 = st.columns([1,1,1])

        with col2:
            if st.button("🚀 Create Free Account", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

        st.markdown("---")

    # ===== CHAT DISPLAY (NEW BUBBLE STYLE) =====
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

            responses = [
                "I'm here for you. It's okay to not feel okay sometimes. Your feelings are valid and it takes strength to talk about them.",
                "Tell me more about it. You're doing better than you think.",
                "You don't have to face this alone. Whatever you're going through, talking helps more than we think. Try breaking your day into tiny steps — one step at a time is still progress.",
                "Be gentle with yourself today. You deserve compassion and care."
            ]

            st.session_state.demo_messages.append(
                {"role": "assistant", "content": random.choice(responses)}
            )

            st.rerun()
