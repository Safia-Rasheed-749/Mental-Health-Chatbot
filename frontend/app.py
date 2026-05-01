# app.py
import streamlit as st
import streamlit.components.v1 as components  # ADDED for scroll fix
from components.navbar import render_navbar
from layout_utils import apply_clean_layout

st.set_page_config(
    page_title="MindCareAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= GLOBAL CSS =================
st.markdown("""
<style>
    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        height: 2.875rem !important;
    }

    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    .main .block-container {
        padding-top: 0.5rem !important;
    }

    button[kind="header"] {
        display: flex !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= SCROLL FIX =================
components.html(
    """
    <script>
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        scrollToTop();

        const observer = new MutationObserver(scrollToTop);
        observer.observe(document.body, { childList: true, subtree: true });

        window.addEventListener('popstate', scrollToTop);
    </script>
    """,
    height=0,
    scrolling=False
)

# ================= SESSION INIT =================
def init_session():
    defaults = {
        "user": None,
        "page": "landing",
        "current_page": "Dashboard",
        "chat_history": [],
        "demo_messages": [],
        "demo_count": 0,
        "last_loaded_chat": None,   # ← add this
        "conversation_id": None,    # ← add this (used in chat/history)
        "history_selected": None,   # ← optional, for history page
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_session()

# ================= IMPORTS =================
from ui.landing import show_landing_page
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar
from ui.demo_chat import show_demo_chat
from ui_pages.about import show_about_page
from ui import dashboard, chat, history, mood, journal
from ui_pages.admin import show_admin_panel
from ui.games import show_aesthetic_game_selector

# ================= PUBLIC PAGES =================
public_pages_list = ["landing", "games", "demo", "auth", "about"]

# ================= CLEAN LAYOUT FOR PUBLIC =================
if st.session_state.get("page") in public_pages_list:
    apply_clean_layout(hide_header_completely=True)
    render_navbar()

# ================= SYNC FIX (IMPORTANT) =================
# Keep BOTH systems aligned safely (prevents dashboard bug)
if st.session_state.current_page is None:
    st.session_state.current_page = "Dashboard"

# ================= DEMO ROUTE =================
if st.session_state.page == "demo":
    show_demo_chat()
    st.stop()

# ================= PUBLIC ROUTING =================
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

    elif st.session_state.page == "games":
        st.session_state["games_from_sidebar"] = False
        st.session_state["public_game_mode"] = True
        show_aesthetic_game_selector()

    elif st.session_state.page == "auth":
        show_auth_page()

    else:
        st.session_state.page = "landing"
        st.rerun()

    st.stop()

# ================= LOGGED IN AREA =================
apply_clean_layout(hide_header_completely=False)

# Keep sidebar collapse/expand icon always visible for logged-in users
st.markdown("""
<style>
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 9999 !important;
}
</style>
""", unsafe_allow_html=True)

user = st.session_state.user
user_id = user[0]
is_admin = len(user) > 3 and user[3]

current = st.session_state.get("current_page", "Dashboard")

# ================= SIDEBAR CONTROL =================
if current != "Admin Panel":
    show_sidebar(user_id, current)
else:
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none !important; }
            button[kind="header"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

# ================= FINAL ROUTING (FIXED) =================
# IMPORTANT: ONLY current_page drives navigation now

# ================= SAFE ROUTER =================

# FORCE DEFAULT
# ================= SAFE ROUTER WITH QUERY PARAM FALLBACK =================
# Ensure a default
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# Priority: URL query param > session state
if st.query_params.get("page"):
    current = st.query_params["page"]
    st.session_state.current_page = current
    # Clear the param after using it to avoid sticky navigation
    st.query_params.clear()
else:
    current = st.session_state["current_page"]


# ================= ROUTING =================

if current == "Dashboard":
    dashboard.show_dashboard()

elif current == "Chat":
    chat.show_chat(user_id)

elif current == "Mood Analytics":
    mood.show_mood_analytics(user_id)

elif current == "Journal":
    journal.show_journal(user_id)

elif current == "Games":
    st.session_state["games_from_sidebar"] = True
    st.session_state["public_game_mode"] = False
    show_aesthetic_game_selector()

elif current == "Admin Panel" and is_admin:
    show_admin_panel()

else:
    st.session_state["current_page"] = "Dashboard"
    dashboard.show_dashboard()