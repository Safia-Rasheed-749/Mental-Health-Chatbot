import streamlit as st

st.set_page_config(
    page_title="MindCareAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION INIT ----------------
def init_session():
    defaults = {
        "user": None,
        "page": "landing",   # ✅ START HERE ALWAYS
        "current_page": "Dashboard",
        "chat_history": [],
        "demo_messages": [],
        "demo_count": 0,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ---------------- HIDE SIDEBAR NAV ----------------
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- IMPORTS ----------------
from ui.landing import show_landing_page
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar
from ui.demo_chat import show_demo_chat
from ui_pages.about import show_about_page
from ui import dashboard, chat, history, mood, journal
from ui_pages.admin import show_admin_panel

# ---------------- ROUTING FIX ----------------
page = st.session_state.page

# ================= DEMO =================
if page == "demo":
    show_demo_chat()
    st.stop()

# ================= PUBLIC ROUTES =================
if st.session_state.user is None:

    # hide sidebar when not logged in
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none !important; }
            button[kind="header"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    if page == "landing":
        show_landing_page()

    elif page == "about":
        show_about_page()

    elif page == "auth":
        show_auth_page()

    st.stop()

# ================= LOGGED IN AREA =================
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: block !important; }
        button[kind="header"] { display: flex !important; }
    </style>
""", unsafe_allow_html=True)

show_sidebar()

user = st.session_state.user
user_id = user[0]
is_admin = len(user) > 3 and user[3]

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