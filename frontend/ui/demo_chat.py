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

    st.markdown("""
    <style>
    /* Whole page background */
    .stApp {
        background-color: #EAF4FF !important;
    }

    /* Optional: keep content readable */
    .block-container {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== CSS (SAFE - NO NAVBAR BREAK) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1.8rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER =====
    st.markdown(
        "<h2 style='text-align:center; color:#1E3A5F;' margin-top:25px;'>Try MindCare AI</h2>",
        unsafe_allow_html=True
    )

    # ===== COUNTER =====
    remaining = 5 - st.session_state.demo_msg_count

    if remaining > 0:
        st.markdown(
            f"<div style='text-align:center; color:#4A6FA5;'>✨ {remaining} free messages remaining</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='text-align:center; color:red;'>⚠️ Trial ended</div>",
            unsafe_allow_html=True
        )

    # ===== CHAT DISPLAY =====
    for msg in st.session_state.demo_messages:

        # USER MESSAGE (RIGHT with spacing)
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin:3px 0; padding-right:350px;">
                <div style="
                    background: #F3F4F6;
                    color:Black;
                    padding:1px 1px;
                    border-radius:8px 8px 3px 8px;
                    max-width:48%;
                    margin-right:8px;
                ">
                    {msg["content"]}
                    <div style="font-size:8px; opacity:0.7; margin-top:4px;">
                        {time.strftime("%I:%M %p")}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # BOT MESSAGE (LEFT with spacing)
        else:
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-start; margin:3px 0; padding-left:300px;">
                <div style="
                    background:#F3F4F6;
                    color:#1F2937;
                    padding:1px 1px;
                    border-radius:8px 8px 3px 3px;
                    max-width:48%;
                    margin-left:8px;
                    border:1px solid #E5E7EB;
                ">
                    {msg["content"]}
                    <div style="font-size:8px; color:#9CA3AF; margin-top:2px;">
                        {time.strftime("%I:%M %p")}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ===== INPUT =====
    if remaining > 0:
        user_input = st.chat_input("Type your message...")

        if user_input:

            # USER MESSAGE ADD
            st.session_state.demo_messages.append(
                {"role": "user", "content": user_input}
            )
            st.session_state.demo_msg_count += 1

            # AI RESPONSE
            responses = [
                "🧠  I'm here for you.You can ask anything from me",
                "🧠  Tell me more about it.so i can guide you properly according to your problem",
                "🧠  You're not alone.your Mindcare AI is always with you",
                "🧠  I understand how you feel.Be strong",
                "🧠  I'm listeningyou can sahre your problem so i can guide you according to that"
            ]

            response = random.choice(responses)

            st.session_state.demo_messages.append(
                {"role": "assistant", "content": response}
            )

            # TRIGGER EXACTLY AT 5
            if st.session_state.demo_msg_count == 5:
                st.session_state.trial_ended = True

            st.rerun()

    # ===== UPGRADE POPUP =====
    if st.session_state.trial_ended:

        st.markdown("""
        <style>
        .fixed-upgrade {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            width: 48%;
            max-width: 200px;
            background: #FEF3C7;
            padding: 18px;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            z-index: 9999;
        }
        </style>

        <div class="fixed-upgrade">
            <h4 style="color:#D97706; margin:0;">✨ Trial Complete!</h4>
            <p style="color:#78350F; margin:5px 0 0 0;">
                Sign up for unlimited messages
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚀 Create Free Account", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()