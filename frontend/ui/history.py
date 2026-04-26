# history.py (modified)
import streamlit as st
from db import get_messages
from layout_utils import apply_clean_layout    # add

def show_history(user_id):
    apply_clean_layout(hide_header_completely=False)   # <--- ADDED
    
    st.title("📜 Chat History")
    # ... rest unchanged (no custom padding CSS needed)

    messages = get_messages(user_id)
    if not messages:
        st.info("No chat history found.")
        return

    for role, content in messages:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(f"<div style='font-size:16px'>{content}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant"):
                st.markdown(f"<div style='font-size:16px; color:#00695c'>{content}</div>", unsafe_allow_html=True)

    # Optional styling
    st.markdown("""
        <style>
        .stChatMessage > div[data-testid="stMarkdownContainer"] {
            padding: 10px; border-radius: 10px;
        }
        .stChatMessage-user > div[data-testid="stMarkdownContainer"] {
            background-color: #f1f8e9;
        }
        .stChatMessage-assistant > div[data-testid="stMarkdownContainer"] {
            background-color: #e0f7fa;
        }
        </style>
    """, unsafe_allow_html=True)