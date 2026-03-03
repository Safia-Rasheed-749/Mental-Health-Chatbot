# history.py
import streamlit as st
from db import get_messages

def show_history(user_id):
    st.title("📜 Chat History")

    # Fetch all past messages from DB
    messages = get_messages(user_id)

    if not messages:
        st.info("No chat history found.")
        return

    # Container to display messages
    history_container = st.container()

    # Display messages in chat bubble style
    for role, content in messages:
        if role == "user":
            with history_container:
                with st.chat_message("user"):
                    st.markdown(f"<div style='font-size:16px'>{content}</div>", unsafe_allow_html=True)
        else:
            with history_container:
                with st.chat_message("assistant"):
                    st.markdown(f"<div style='font-size:16px; color:#00695c'>{content}</div>", unsafe_allow_html=True)

    # Optional: Styling to match chat.py
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
