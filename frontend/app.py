import streamlit as st
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindCareAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- IMPORT MODULES ----------------
from ui.landing import show_landing_page
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar
from ui.demo_chat import show_demo_chat
from pages.about import show_about_page
from ui import dashboard, chat, history, mood, journal

# ---------------- CSS ----------------
def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ⭐⭐ CHAT HISTORY INITIALIZATION ⭐⭐
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ⭐ DEMO SESSION VARIABLES
if "demo_messages" not in st.session_state:
    st.session_state.demo_messages = []

if "demo_count" not in st.session_state:
    st.session_state.demo_count = 0

# ---------------- HIDE SIDEBAR FOR PUBLIC ----------------
if st.session_state.user is None:
    st.markdown(
        """
        <style>
        /* Hide sidebar but keep it in DOM to avoid state issues */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* Also hide the collapse button when sidebar is hidden */
        button[kind="header"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# =========================================================
# ROUTING LOGIC
# =========================================================

# ⭐⭐ DEMO PAGE (Accessible without login) ⭐⭐
if st.session_state.page == "demo":
    show_demo_chat()
    st.stop()

# PUBLIC PAGES (No login required)
if st.session_state.user is None:
    if st.session_state.page == "landing":
        show_landing_page()
    elif st.session_state.page == "about":
        show_about_page()
    elif st.session_state.page == "auth":
        show_auth_page()
    st.stop()

# PRIVATE PAGES (Login required)
show_sidebar()
try:
    user_id = st.session_state.user[0]
except (TypeError, IndexError, KeyError):
    st.error("User data corrupted. Please login again.")
    st.session_state.user = None
    st.rerun()
    st.stop()
# ⭐ NO SUCCESS MESSAGES - DIRECT DASHBOARD ⭐
current_view = st.session_state.current_page

if current_view == "Dashboard":
    dashboard.show_dashboard()
elif current_view == "Chat":
    chat.show_chat(user_id)
elif current_view == "History":
    history.show_history(user_id)
elif current_view == "Mood Analytics":
    mood.show_mood_analytics(user_id)
elif current_view == "Journal":
    journal.show_journal(user_id)
else:
    dashboard.show_dashboard()