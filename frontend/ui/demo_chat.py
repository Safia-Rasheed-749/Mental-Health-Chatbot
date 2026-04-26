import streamlit as st
import tempfile
import random
from gtts import gTTS
from utils.ai_engine import generate_response
from layout_utils import apply_clean_layout

def speak(text):
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
    except:
        pass

def show_demo_chat():
    apply_clean_layout(hide_header_completely=True)
    
    # Top spacer to separate from navbar
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
    </script>
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #ffffff, #eaf6fb, #d6ecf7);
        }
        .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
            background: #e2f0ff !important;
            border-radius: 24px 24px 8px 24px !important;
            padding: 12px 18px !important;
            color: #0b2b42 !important;
            border: 1px solid rgba(59,130,246,0.2) !important;
        }
        .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
            background: white !important;
            border-radius: 24px 24px 24px 8px !important;
            padding: 12px 18px !important;
            color: #1e3a5f !important;
            border: 1px solid rgba(100,116,139,0.1) !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
        }
        /* Increase spacing below the badge */
        .message-badge {
            text-align: center;
            margin-bottom: 30px !important;
        }
        .custom-chat-input {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            align-items: center;
        }
        .custom-chat-input input {
            flex: 1;
            padding: 12px 16px;
            border-radius: 60px;
            border: 1px solid #cbd5e1;
            background: white;
            font-size: 1rem;
            outline: none;
        }
        .custom-chat-input button {
            background: linear-gradient(135deg, #4F84D9, #1E40AF);
            color: white;
            border: none;
            border-radius: 60px;
            padding: 12px 24px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 28px 24px; background: rgba(255,255,255,0.94); border-radius: 32px; margin: 20px 0 30px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.05); border: 1px solid rgba(59,130,246,0.2);">
        <h1 style="color: #1e3a8a; font-size: 2.2rem; margin-bottom: 8px; font-weight: 800;">✨ Try MindCare AI</h1>
        <p style="color: #334155; font-size: 1rem;">Experience compassionate, AI‑powered support – 5 free messages</p>
    </div>
    """, unsafe_allow_html=True)

    if "demo_messages" not in st.session_state:
        st.session_state.demo_messages = [{
            "role": "assistant",
            "content": "👋 Hello! You have 5 free messages. Ask me anything about stress, anxiety, or just talk – I'm here to listen and support you."
        }]

    user_msgs = [m for m in st.session_state.demo_messages if m["role"] == "user"]
    remaining = 5 - len(user_msgs)

    st.markdown(f"""
    <div class="message-badge">
        <span style="background: linear-gradient(135deg, #4F84D9, #1E40AF); color: white; padding: 8px 24px; border-radius: 60px; font-size: 0.9rem; font-weight: 600; display: inline-block;">📨 {remaining} message{'' if remaining == 1 else 's'} remaining</span>
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    chat_container = st.container()
    for msg in st.session_state.demo_messages:
        with chat_container:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if remaining <= 0:
        st.markdown("""
        <div style="background: #fffbeb; border: 1px solid #fbbf24; border-radius: 28px; padding: 50px 24px; text-align: center; margin: 40px 0;">
            <h3 style="color: #b45309; font-size: 1.6rem; margin-bottom: 12px;">🔒 Demo Limit Reached</h3>
            <p style="color: #92400e; font-size: 1rem;">You've used all 5 free messages. Sign up to continue unlimited chats and save your history.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Sign Up / Login", key="demo_signup", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()
        st.stop()

    # Chat input form
    with st.form(key="demo_chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed")
        with col_send:
            submitted = st.form_submit_button("Send", use_container_width=True)
        
        if submitted and user_input and user_input.strip():
            st.session_state.demo_messages.append({"role": "user", "content": user_input})
            try:
                response = generate_response(user_input, st.session_state.demo_messages[-5:])
            except:
                demo_fallbacks = [
                    "I hear you. Could you tell me a bit more about that?",
                    "Thank you for sharing. How does that make you feel?",
                    "That's completely valid. Would you like to explore some coping strategies?",
                    "I'm here for you. What would be most helpful right now?",
                    "It takes courage to talk about this. You're doing great."
                ]
                response = random.choice(demo_fallbacks)
            st.session_state.demo_messages.append({"role": "assistant", "content": response})
            speak(response)
            st.rerun()

if __name__ == "__main__":
    show_demo_chat()