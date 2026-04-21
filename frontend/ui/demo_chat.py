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
    # ================= BACK TO HOME BUTTON - EXACT MATCH TO AUTH.PY =================
    # Target the button by its key to avoid any CSS conflicts
    st.markdown("""
    <style>
    /* Fixed position container */
    .back-home-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    /* Target button with key="back_to_home_demo" specifically */
    button[kind="secondary"][data-testid="baseButton-secondary"] {
        /* Reset any inherited styles */
        all: initial;
    }
    
    /* Use the exact key selector */
    button[key="back_to_home_demo"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        width: auto !important;
        min-width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: normal !important;
        height: auto !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    button[key="back_to_home_demo"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px -10px #4A90E2 !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important; /* No color change */
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="back-home-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_to_home_demo"):
        st.session_state.page = "landing"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Rest of demo page styling (unchanged, professional)
    st.markdown("""
    <style>
    .demo-header {
        text-align: center;
        padding: 24px;
        background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #94a3b8;
    }
    .demo-header h1 {
        color: #0f172a;
        font-size: 2.5rem;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .demo-header p {
        color: #1e293b;
        font-size: 1rem;
    }
    .counter-badge {
        background: #475569;
        color: #f1f5f9;
        padding: 6px 18px;
        border-radius: 40px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .limit-box {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin: 40px 0;
    }
    .limit-box h3 {
        color: #92400e;
        font-size: 1.8rem;
        margin-bottom: 20px;
    }
    .limit-box p {
        color: #92400e;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    .stChatMessage {
        margin: 12px 0;
    }
    .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
        background-color: #e2e8f0;
        border-radius: 20px;
        padding: 12px 18px;
        color: #0f172a;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
        background-color: #dbeafe;
        border-radius: 20px;
        padding: 12px 18px;
        color: #1e3a8a;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    div.stButton > button[key="demo_signup"] {
        background: linear-gradient(135deg, #B8D9FF, #6D9EEB) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 8px 28px !important;
        border-radius: 40px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        border: none !important;
    }
    div.stButton > button[key="demo_signup"]:hover {
        background: #6D9EEB !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(109, 158, 235, 0.3) !important;
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