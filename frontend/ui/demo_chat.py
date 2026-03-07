import streamlit as st
import tempfile
import random
from gtts import gTTS
from utils.ai_engine import generate_response

# ---------------- HIDE STREAMLIT DEFAULT ELEMENTS ----------------
st.markdown("""
<style>
    /* Hide Streamlit's default header, footer, and menu */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Hide the deploy button and three dots */
    .stApp header [data-testid="stToolbar"] {display: none !important;}
    .stApp header [data-testid="stDecoration"] {display: none !important;}
    .stApp header [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Remove extra top padding */
    .main > div {
        padding-top: 0rem !important;
    }
    
    /* Back to Home Button Styling */
    .back-home-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    .back-home-btn button {
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
    }
    
    .back-home-btn button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Text-to-Speech (ONLY OUTPUT) ----------------
def speak(text):
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
    except:
        pass

# ---------------- DEMO CHAT PAGE ----------------
def show_demo_chat():
    # BACK TO HOME BUTTON
    st.markdown('<div class="back-home-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_to_home_demo"):
        st.session_state.page = "landing"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom CSS for demo chat
    st.markdown("""
    <style>
    .demo-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
    }
    .demo-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    .counter-badge {
        background: #ff4444;
        color: white;
        padding: 5px 15px;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }
    .limit-box {
        background: #fff3cd;
        border: 2px solid #ffeeba;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin: 40px 0;
    }
    .limit-box h3 {
        color: #856404;
        font-size: 2rem;
        margin-bottom: 20px;
    }
    .limit-box p {
        color: #856404;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    .stChatMessage > div[data-testid="stMarkdownContainer"] {
        padding: 10px;
        border-radius: 10px;
    }
    .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
        background-color: #f1f8e9;
    }
    .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
        background-color: #e0f7fa;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="demo-header">
        <h1>✨ Demo Mode</h1>
        <p>Try 5 free messages with full AI responses</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize demo messages if not exists
    if "demo_messages" not in st.session_state:
        st.session_state.demo_messages = []
        # Add welcome message
        st.session_state.demo_messages.append({
            "role": "assistant", 
            "content": "👋 Hi! You have 5 free messages. Ask me anything about mental health, stress, anxiety, or just chat!"
        })

    # Calculate remaining messages
    user_messages = [m for m in st.session_state.demo_messages if m["role"] == "user"]
    remaining = 5 - len(user_messages)

    # Show counter
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="counter-badge">📨 {remaining} messages remaining</span>
    </div>
    """, unsafe_allow_html=True)

    # Display chat messages
    chat_container = st.container()
    for msg in st.session_state.demo_messages:
        with chat_container:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Check if limit reached
    if remaining <= 0:
        st.markdown("""
        <div class="limit-box">
            <h3>🔒 Limit Reached</h3>
            <p>You've used all 5 free messages! Sign up to continue with unlimited chats.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Sign Up / Login", key="demo_signup", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()
        
        # Stop execution
        st.stop()

    # ONLY TEXT INPUT - NO MIC OPTION
    user_input = st.chat_input("Type your message...")

    # Handle user input
    if user_input:
        # Add user message
        st.session_state.demo_messages.append({"role": "user", "content": user_input})
        
        # Prepare context (last 5 messages)
        context = st.session_state.demo_messages[-5:]
        
        # Generate REAL AI response using same engine as chat.py
        try:
            response = generate_response(user_input, context)
        except:
            # Fallback responses if AI engine fails
            demo_responses = [
                "I understand how you feel. Can you tell me more?",
                "That's interesting. How does that make you feel?",
                "Thanks for sharing. Would you like to talk about it?",
                "I'm here to listen. What's on your mind?",
                "That's a good point. When you sign up, you'll get even better responses!"
            ]
            response = random.choice(demo_responses)
        
        # Add assistant message
        st.session_state.demo_messages.append({"role": "assistant", "content": response})
        
        # Voice OUTPUT only (speak the response)
        speak(response)
        
        # Rerun to update display
        st.rerun()