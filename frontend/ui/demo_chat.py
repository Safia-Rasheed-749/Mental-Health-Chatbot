import streamlit as st
import tempfile
import random
from gtts import gTTS
from utils.ai_engine import generate_response

# ---------------- HIDE STREAMLIT DEFAULT ELEMENTS ----------------
st.markdown("""
<style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stApp header [data-testid="stToolbar"] {display: none !important;}
    .stApp header [data-testid="stDecoration"] {display: none !important;}
    .stApp header [data-testid="stStatusWidget"] {display: none !important;}
    .main > div { padding-top: 0rem !important; }
</style>
""", unsafe_allow_html=True)

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
    # ================= PAGE BACKGROUND: SOFT BLUE =================
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e6f0fa, #b8d4e8) !important;
    }
    .main .block-container {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= BACK TO HOME BUTTON (BLUE, NO HOVER DRAMA) =================
    st.markdown("""
    <style>
    .back-home-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    button[key="back_to_home_demo"] {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 8px 24px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    
    button[key="back_to_home_demo"]:hover {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="back-home-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_to_home_demo"):
        st.session_state.page = "landing"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= REST OF STYLES (POLISHED FOR BLUE BACKGROUND) =================
    st.markdown("""
    <style>
    .demo-header {
        text-align: center;
        padding: 28px 24px;
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(2px);
        border-radius: 32px;
        margin-bottom: 32px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(59,130,246,0.2);
    }
    .demo-header h1 {
        color: #1e3a8a;
        font-size: 2.2rem;
        margin-bottom: 12px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .demo-header p {
        color: #2c3e66;
        font-size: 1rem;
        opacity: 0.9;
    }
    .counter-badge {
        background: #1e40af;
        color: white;
        padding: 6px 20px;
        border-radius: 60px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        margin-top: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .limit-box {
        background: #fffbeb;
        border: 1px solid #fbbf24;
        border-radius: 28px;
        padding: 48px 24px;
        text-align: center;
        margin: 40px 0;
    }
    .limit-box h3 {
        color: #b45309;
        font-size: 1.6rem;
        margin-bottom: 16px;
    }
    .limit-box p {
        color: #92400e;
        font-size: 1rem;
    }
    /* Chat bubbles – soft and modern */
    .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
        background: #e2f0ff;
        border-radius: 24px 24px 8px 24px;
        padding: 12px 20px;
        color: #0b2b42;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid rgba(59,130,246,0.15);
    }
    .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
        background: white;
        border-radius: 24px 24px 24px 8px;
        padding: 12px 20px;
        color: #1e3a5f;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        border: 1px solid rgba(100,116,139,0.1);
    }
    /* Signup button */
    div.stButton > button[key="demo_signup"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 32px !important;
        border-radius: 60px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
        border: none !important;
    }
    div.stButton > button[key="demo_signup"]:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59,130,246,0.4) !important;
    }
    /* Chat input styling */
    .stChatInputContainer {
        background: white;
        border-radius: 60px;
        padding: 4px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .stChatInputContainer textarea {
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="demo-header">
        <h1>✨ Demo Mode</h1>
        <p>Experience AI-powered mental health support with 5 free messages</p>
    </div>
    """, unsafe_allow_html=True)

    if "demo_messages" not in st.session_state:
        st.session_state.demo_messages = []
        st.session_state.demo_messages.append({
            "role": "assistant", 
            "content": "👋 Hello! You have 5 free messages. Ask me anything about mental health, stress, anxiety, or just have a conversation. I'm here to listen and support you."
        })

    user_messages = [m for m in st.session_state.demo_messages if m["role"] == "user"]
    remaining = 5 - len(user_messages)

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="counter-badge">📨 {remaining} message{'' if remaining == 1 else 's'} remaining</span>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()
    for msg in st.session_state.demo_messages:
        with chat_container:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if remaining <= 0:
        st.markdown("""
        <div class="limit-box">
            <h3>🔒 Demo Limit Reached</h3>
            <p>You've used all 5 free messages. Sign up to continue with unlimited chats and save your conversation history.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Sign Up / Login", key="demo_signup", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()
        st.stop()

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.demo_messages.append({"role": "user", "content": user_input})
        context = st.session_state.demo_messages[-5:]
        try:
            response = generate_response(user_input, context)
        except:
            demo_responses = [
                "I understand how you feel. Can you tell me more?",
                "That's interesting. How does that make you feel?",
                "Thanks for sharing. Would you like to talk about it?",
                "I'm here to listen. What's on your mind?",
                "That's a good point. When you sign up, you'll get even better responses!"
            ]
            response = random.choice(demo_responses)
        st.session_state.demo_messages.append({"role": "assistant", "content": response})
        speak(response)
        st.rerun()