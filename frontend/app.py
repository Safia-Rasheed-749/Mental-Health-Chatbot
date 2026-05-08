# app.py
import streamlit as st
import streamlit.components.v1 as components  # ADDED for scroll fix
from components.navbar import render_navbar
from layout_utils import apply_clean_layout, apply_professional_design_system

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

    /* Header: fully transparent, stays in normal flow so collapsedControl stays positioned correctly */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
        border-bottom: none !important;
    }

    /* Sidebar collapse/expand arrow — always fully visible */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 99999 !important;
    }

    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Block container: no top padding since header is out of flow */
    .main .block-container {
        padding-top: 0 !important;
    }

    button[kind="header"] {
        display: flex !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= SCROLL FIX (parent frame + debounce — Streamlit runs in iframe) =================
components.html(
    """
    <script>
        (function () {
            var t = null;
            function scrollToTop() {
                try {
                    var p = window.parent && window.parent !== window ? window.parent : window;
                    var d = p.document;
                    p.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                    if (d.documentElement) d.documentElement.scrollTop = 0;
                    if (d.body) d.body.scrollTop = 0;
                    var view = d.querySelector('[data-testid="stAppViewContainer"]');
                    if (view) view.scrollTop = 0;
                    var main = d.querySelector('section.main');
                    if (main) main.scrollTop = 0;
                    var inner = d.querySelector('.main .block-container');
                    if (inner && inner.parentElement) inner.parentElement.scrollTop = 0;
                } catch (e) {
                    try { window.scrollTo({ top: 0, left: 0, behavior: 'auto' }); } catch (e2) {}
                }
            }
            function debounced() {
                if (t) clearTimeout(t);
                t = setTimeout(scrollToTop, 80);
            }
            scrollToTop();
            if (window.parent && window.parent !== window) {
                try {
                    var obs = new MutationObserver(debounced);
                    obs.observe(window.parent.document.body, { childList: true, subtree: true });
                } catch (e) {}
            }
            window.addEventListener('popstate', scrollToTop);
        })();
    </script>
    """,
    height=0,
    scrolling=False
)

# ── SIDEBAR TOGGLE BUTTON STYLER (must target parent frame — st.markdown CSS can't reach it) ──
components.html(
    """
    <script>
    (function() {
        function styleToggle() {
            try {
                var doc = window.parent.document;
                // Inject a <style> tag into the parent document once
                if (doc.getElementById('kiro-toggle-style')) return;
                var style = doc.createElement('style');
                style.id = 'kiro-toggle-style';
                style.textContent = `
                    [data-testid="collapsedControl"] button {
                        background: linear-gradient(135deg, #5B8DEF, #7C9DF5) !important;
                        border-radius: 50% !important;
                        width: 32px !important;
                        height: 32px !important;
                        min-width: 32px !important;
                        min-height: 32px !important;
                        border: none !important;
                        box-shadow: 0 2px 10px rgba(91,141,239,0.55) !important;
                        padding: 6px !important;
                        transition: all 0.2s ease !important;
                        display: flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                    }
                    [data-testid="collapsedControl"] button:hover {
                        background: linear-gradient(135deg, #4a7de0, #6b8ef0) !important;
                        box-shadow: 0 4px 16px rgba(91,141,239,0.75) !important;
                        transform: scale(1.1) !important;
                    }
                    [data-testid="collapsedControl"] button svg {
                        fill: #ffffff !important;
                        stroke: #ffffff !important;
                        color: #ffffff !important;
                    }
                    [data-testid="collapsedControl"] button svg path {
                        fill: #ffffff !important;
                        stroke: #ffffff !important;
                    }
                `;
                doc.head.appendChild(style);
            } catch(e) {}
        }
        styleToggle();
        setTimeout(styleToggle, 300);
        setTimeout(styleToggle, 800);
        // Re-apply on DOM changes (Streamlit reruns remove injected styles)
        try {
            new MutationObserver(function() {
                var doc = window.parent.document;
                if (!doc.getElementById('kiro-toggle-style')) styleToggle();
            }).observe(window.parent.document.body, { childList: true, subtree: true });
        } catch(e) {}
    })();
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
from ui.exercises import show_exercises_page  # <-- Make sure this import is correct
from ui.auth import show_auth_page
from ui.sidebar import show_sidebar
from ui.demo_chat import show_demo_chat
from ui_pages.about import show_about_page
from ui import dashboard, chat, mood, journal
from ui_pages.admin import show_admin_panel
from ui.games import show_aesthetic_game_selector

# ================= PUBLIC PAGES =================
public_pages_list = ["landing", "games", "exercises", "auth", "about"]

# ================= CLEAN LAYOUT FOR PUBLIC =================
if st.session_state.get("page") in public_pages_list:
    apply_clean_layout(hide_header_completely=True)
    apply_professional_design_system()
    render_navbar()

# ================= SYNC FIX (IMPORTANT) =================
# Keep BOTH systems aligned safely (prevents dashboard bug)
if st.session_state.current_page is None:
    st.session_state.current_page = "Dashboard"

# ================= DEMO ROUTE =================
if st.session_state.page == "demo":
    apply_clean_layout(hide_header_completely=True)
    apply_professional_design_system()
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
    elif st.session_state.page == "exercises":  # <-- Match this with button
        show_exercises_page()

    elif st.session_state.page == "about":
        show_about_page()

    elif st.session_state.page == "games":
        st.session_state["games_from_sidebar"] = False
        st.session_state["public_game_mode"] = True
        # Reset to home only on fresh navigation (not on reruns during gameplay)
        if st.session_state.get("_games_nav_trigger") != "public":
            st.session_state["game_screen"] = "home"
            st.session_state["game_active"] = False
            st.session_state["is_playing_seq"] = False
            st.session_state["waiting"] = False
        st.session_state["_games_nav_trigger"] = "public"
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

# ================= SAFE ROUTER WITH QUERY PARAM FALLBACK =================
# Ensure a default
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# Use query param only if it differs from current session state (first arrival)
# Do NOT clear it with st.query_params.clear() — that triggers an extra rerun
qp = st.query_params.get("page")
if qp and qp != st.session_state.get("current_page"):
    st.session_state["current_page"] = qp

current = st.session_state["current_page"]

# Shared light theme for all logged-in pages except Admin (admin keeps dark UI in admin.py)
if not (current == "Admin Panel" and is_admin):
    apply_professional_design_system()


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
    # Reset to home only on fresh navigation (not on reruns during gameplay)
    if st.session_state.get("_games_nav_trigger") != "sidebar":
        st.session_state["game_screen"] = "home"
        st.session_state["game_active"] = False
        st.session_state["is_playing_seq"] = False
        st.session_state["waiting"] = False
    st.session_state["_games_nav_trigger"] = "sidebar"
    show_aesthetic_game_selector()

elif current == "Admin Panel" and is_admin:
    show_admin_panel()

else:
    st.session_state["current_page"] = "Dashboard"
    dashboard.show_dashboard()