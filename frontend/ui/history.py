import streamlit as st
from db import get_messages

def show_history(user_id):
    # --- Remove top white space ---
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: -0.5rem !important;
        }
        .main .block-container > :first-child {
            margin-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📜 Chat History")

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