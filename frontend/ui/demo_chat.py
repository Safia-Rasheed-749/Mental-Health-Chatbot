import streamlit as st
import random
import time

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
        # ===== CSS (SAFE - NO NAVBAR BREAK) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== CSS =====
    st.markdown("""
    <style>

        .stApp {
            background-color: white !important;
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
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        }

        .trial-title {
            font-size: 22px;
            font-weight: bold;
        }

        .trial-counter {
            font-size: 18px;
            margin-top: 30px;
            color: #FFE66D;
            font-weight: 600;
        }

        /* ===== TRIAL COMPLETE ===== */
        .trial-complete-container {
            padding: 15px 20px;
            margin: 20px 0;
            border-bottom: 1px solid #eee;
            text-align: center;
        }

        /* ===== CHAT UI ===== */
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 10px 0;

        }

        .user-bubble {
            background: lightblue;
            padding: 1px 5px;
            max-width: 20%;
            padding-right: 100px;
            border-radius: 30px;

        }

        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin: 10px 0;
        }

        .assistant-bubble {
            background: white;
            padding: 4px 5px;
            max-width: 80%;
            padding-left: 150px
        }

        
    </style>
    """, unsafe_allow_html=True)

    # ===== LOGIC =====
    remaining = 5 - st.session_state.demo_msg_count
    if remaining <= 0:
        st.session_state.trial_ended = True

    # ===== TOP BOX =====
    if not st.session_state.trial_ended:
        st.markdown(f"""
        <div class="trial-box">
            <div class="trial-title">🤖 Try MindCare AI</div>
            <div class="trial-counter">✨ {remaining} Free Trial messages ✨</div>
            <div style="font-size: 12px; margin-top: 10px;">
                Professional mental health support
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="trial-complete-container">
            <h2 style="color:#333; margin:0;">✨ Trial Complete! ✨</h2>
            <p style="color:#666; font-size:14px;">
                You've used all 5 free messages. Create an account for unlimited access!
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1.5])
        with col1:
            if st.button("🚀 Create Free Account"):
                st.session_state.page = "auth"
                st.rerun()

        st.markdown("---")

    # ===== CHAT DISPLAY =====
    for msg in st.session_state.demo_messages:
        current_time = time.strftime("%I:%M %p")

        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-bubble">
                    {msg["content"]}
                    <div class="time" style="text-align:right;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="assistant-bubble">
                    {msg["content"]}
                    <div class="time"></div>
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
                "🧠 I'm here for you.Its okay to not feel okay sometimes. Your feelings are valid and it takes strength to talk about them.",
                "🧠 Tell me more about it.Mental health ups and downs are part of being human. Youre doing better than you think just by reaching out.",
                "🧠 MindCare AI is always with you.Whatever youre going through, you dont have to face it alone. Talking helps more than we think.Try breaking your day into tiny steps — just focus on the next 10 minutes. One step at a time is still progress.",
                "🧠 Your mind deserves the same care you would give a close friend. Be gentle with yourself today.If your thoughts feel too heavy, try writing them down or stepping outside for 5 minutes of fresh air.",
            ]


            st.session_state.demo_messages.append(
                {"role": "assistant", "content": random.choice(responses)}
            )

            st.rerun()