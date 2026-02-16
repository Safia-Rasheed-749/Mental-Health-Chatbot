import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ")

st.title("About This Project")

st.markdown("""
## AI-Powered Conversational Assistant for Mental Health Support

This system is developed as a Final Year Project for BS Computer Science at  
National University of Modern Languages (NUML), Islamabad.

### Core Features
- Emotion-aware conversation
- Mood tracking & journaling
- Voice interaction (Speech-to-Text & TTS)
- Crisis detection system
- Secure PostgreSQL storage

### Technologies Used
- Streamlit (Frontend)
- FastAPI (Backend – upcoming phase)
- PostgreSQL
- Transformer-based emotion detection
- RAG architecture (planned phase)

### Developed By
- Safia Rasheed  
- Maria Akram  
- Shamsa Akram  

### Supervisor
Faisal Hussain
""")
