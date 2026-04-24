import streamlit as st

st.set_page_config(
    page_title="MindCareAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔴 IMPORTANT: HIDE STREAMLIT AUTO SIDEBAR NAV (App/About/Admin links)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- IMPORT MODULES ----------------
from ui.landing import show_landing_page
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar
from ui.demo_chat import show_demo_chat
from ui_pages.about import show_about_page
from ui import dashboard, chat, history, mood, journal
from ui_pages.admin import show_admin_panel

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "demo_messages" not in st.session_state:
    st.session_state.demo_messages = []

if "demo_count" not in st.session_state:
    st.session_state.demo_count = 0

# ---------------- DEMO PAGE ----------------
if st.session_state.page == "demo":
    show_demo_chat()
    st.stop()

# ---------------- PUBLIC PAGES ----------------
if st.session_state.user is None:

    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none !important; }
            button[kind="header"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.page == "landing":
        show_landing_page()

    elif st.session_state.page == "about":
        show_about_page()

    elif st.session_state.page == "auth":
        show_auth_page()

    st.stop()

# ---------------- LOGGED IN AREA ----------------
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: block !important; }
        button[kind="header"] { display: flex !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
show_sidebar()

# ---------------- USER INFO ----------------
user = st.session_state.user
user_id = user[0]
is_admin = len(user) > 3 and user[3]

# ---------------- ROUTING ----------------
current = st.session_state.current_page

if current == "Dashboard":
    dashboard.show_dashboard()

elif current == "Chat":
    chat.show_chat(user_id)

elif current == "History":
    history.show_history(user_id)

elif current == "Mood Analytics":
    mood.show_mood_analytics(user_id)

elif current == "Journal":
    journal.show_journal(user_id)

elif current == "Admin Panel" and is_admin:
    show_admin_panel()

else:
    dashboard.show_dashboard()