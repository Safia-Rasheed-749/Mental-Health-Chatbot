import streamlit as st

def show_dashboard():
    # Page title
    st.title("Your AI Mental Wellness Companion 🧠")
    
    # Info cards with calm styling
    st.markdown(
        """
        <div style='display:flex; gap:20px; flex-wrap: wrap;'>
            <div style='flex:1; background-color:#e0f7fa; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
                <h3>✔ Emotion-aware AI Conversations</h3>
                <p>Engage in AI-powered chats that understand your mood.</p>
            </div>
            <div style='flex:1; background-color:#e0f7fa; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
                <h3>✔ Voice Interaction Support</h3>
                <p>Talk to your AI companion using voice for a more natural experience.</p>
            </div>
            <div style='flex:1; background-color:#e0f7fa; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
                <h3>✔ Mood Tracking & Journaling</h3>
                <p>Monitor your mood trends and maintain a private journal.</p>
            </div>
            <div style='flex:1; background-color:#e0f7fa; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
                <h3>✔ Secure & Private Data Storage</h3>
                <p>Your data remains private and encrypted at all times.</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )