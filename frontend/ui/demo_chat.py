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

    # ===== CSS =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }

        .stApp {
            background-color: white !important;
        }

        /* ===== USER MESSAGE (RIGHT) ===== */
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 12px 0;
        }

        .user-bubble {
            background: lightblue;
            padding: 12px 18px;
            border-radius: 20px 20px 5px 20px;
            max-width: 70%;
            color: #003366;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        /* ===== BOT MESSAGE (LEFT) ===== */
        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin: 12px 0;
        }

        .assistant-bubble {
            background: #f1f3f5;
            padding: 12px 18px;
            border-radius: 20px 20px 20px 5px;
            max-width: 70%;
            color: #333;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .user-icon, .assistant-icon {
            font-size: 18px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }


        /* ===== TRIAL BOX ===== */
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
            padding-right: 200px;
            margin-bottom: 20px;
            background:red;
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

        # ===== CENTERED BUTTON (FIXED) =====
        col1, col2, col3 = st.columns([1,1,1])

        with col2:
            if st.button("🚀 Create Free Account", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

        st.markdown("---")

    # ===== CHAT DISPLAY =====
    for msg in st.session_state.demo_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-bubble">
                    <div class="user-text">{msg["content"]}</div>
                    <div class="user-icon">👤</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="assistant-bubble">
                    <div class="assistant-icon">🧠</div>
                    <div class="assistant-text">{msg["content"]}</div>
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
                " I'm here for you. It's okay to not feel okay sometimes.I'm here for you. It's okay to not feel okay sometimes. Your feelings are valid and it takes strength to talk about them.",
                " Tell me more about it. You're doing better than you think.",
                " You don't have to face this alone. Whatever you're going through, talking helps more than we think. Try breaking your day into tiny steps — one step at a time is still progress.",
                " Be gentle with yourself today "
            ]

            st.session_state.demo_messages.append(
                {"role": "assistant", "content": random.choice(responses)}
            )

            st.rerun()