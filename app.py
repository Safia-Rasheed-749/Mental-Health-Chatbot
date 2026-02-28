import streamlit as st
import os

# ---------------- 1. PAGE CONFIGURATION ----------------
# This MUST be the first Streamlit command in the file
st.set_page_config(
    page_title="MindCareAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- 2. IMPORT UI MODULES ----------------
from ui.landing import show_landing_page
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar

# Note: We import from 'pages' since your file is located there
from pages.about import show_about_page 

# Import dashboard features
from ui import dashboard, chat, history, mood, journal

# ---------------- 3. LOAD CSS ----------------
def load_css():
    """Load the modern, clean styles from assets/style.css."""
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Fallback to default if CSS is missing

load_css()

# ---------------- 4. SESSION INITIALIZATION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ---------------- 5. HIDE SIDEBAR FOR PUBLIC PAGES ----------------
# We only want the sidebar to appear AFTER the user logs in
if st.session_state.user is None:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {display:none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 6. ROUTING LOGIC: PUBLIC ACCESS (Landing, About, Auth)
# =========================================================
if st.session_state.user is None:
    if st.session_state.page == "landing":
        show_landing_page()
    
    elif st.session_state.page == "about":
        # Professional back button to return home
        if st.button("← Back to Home", type="secondary"):
            st.session_state.page = "landing"
            st.rerun()
        show_about_page()
        
    elif st.session_state.page == "auth":
        if st.button("← Back to Home", type="secondary"):
            st.session_state.page = "landing"
            st.rerun()
        show_auth_page()
    
    # Block execution here so the dashboard doesn't load for guests
    st.stop()

# =========================================================
# 7. ROUTING LOGIC: PRIVATE ACCESS (User Logged In)
# =========================================================

# Show the Sidebar for navigation within the app
show_sidebar()
user_id = st.session_state.user[0] # Assumes DB returns [id, name, email]

# Determine which feature to show based on sidebar selection
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