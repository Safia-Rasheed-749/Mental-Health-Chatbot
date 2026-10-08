# -*- coding: utf-8 -*-
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
    /* Global spacing standards */
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    div[data-testid="stForm"] { gap: 1.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; margin-bottom: 20px; }
    .stExpander { margin-bottom: 24px; border-radius: 10px; }
    div[data-testid="stTextInput"], div[data-testid="stSelectbox"], div[data-testid="stTextArea"] { margin-bottom: 12px; }

    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Keep Streamlit's native header controls above page content when enabled.
       z-index MUST stay below the sidebar (Streamlit theme: sidebar = header+1
       = 999991). At 999999 the fixed header + its stToolbar band [0,16,764,28]
       painted ABOVE the sidebar and swallowed every real click on the sidebar's
       collapse arrow (stSidebarCollapseButton sits at [203,14,36,32]) — so the
       sidebar could never be collapsed. 999990 keeps the header above normal
       page content (z auto) but below the sidebar. */
    header[data-testid="stHeader"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        z-index: 999990 !important;
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 100%) !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1) !important;
        /* Belt & suspenders: the header must not swallow clicks meant for
           content underneath it either; only its own controls stay interactive. */
        pointer-events: none !important;
    }
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] a,
    header[data-testid="stHeader"] [role="button"] {
        pointer-events: auto !important;
    }

    /* The visible app navbar is a custom Streamlit row, not the native header.
       Match it globally and reserve space beneath it on every navbar page. */
    div[data-testid="stHorizontalBlock"]:has(.navbar-container) {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        z-index: 999999 !important;
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 100%) !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    /* Sidebar collapse/expand toggles — always fully visible (Streamlit 1.54+).
       The old [data-testid="collapsedControl"] selector no longer exists. */
    /* Collapse arrow: inside the sidebar header (sidebar expanded). */
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    /* Expand arrow: inside the fixed header (sidebar collapsed). */
    [data-testid="stExpandSidebarButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 1000000 !important;
    }

    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    button[kind="header"] {
        display: flex !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= NAVIGATION SCROLL RESET (parent document) =================
components.html(
    """
    <script>
        (function installNavigationScrollReset() {
            try {
                var parentWindow = window.parent && window.parent !== window ? window.parent : window;
                var doc = parentWindow.document;
                if (parentWindow.__mindcareNavigationScrollReset) return;
                parentWindow.__mindcareNavigationScrollReset = true;

                function scrollToTop() {
                    parentWindow.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                    if (doc.documentElement) doc.documentElement.scrollTop = 0;
                    if (doc.body) doc.body.scrollTop = 0;
                    [
                        doc.querySelector('[data-testid="stAppViewContainer"]'),
                        doc.querySelector('section.main'),
                        doc.querySelector('.main'),
                        doc.querySelector('.main .block-container')?.parentElement
                    ].forEach(function (container) {
                        if (container) container.scrollTop = 0;
                    });
                }

                var navLabels = ['home', 'about', 'exercises', 'games', 'get started'];
                doc.addEventListener('click', function (event) {
                    var button = event.target && event.target.closest
                        ? event.target.closest('button') : null;
                    if (!button) return;
                    var label = (button.innerText || button.getAttribute('aria-label') || '')
                        .replace(/\s+/g, ' ').trim().toLowerCase();
                    var inNavbar = !!button.closest('div[data-testid="stHorizontalBlock"]:has(.navbar-container)');
                    if (!inNavbar && navLabels.indexOf(label) === -1) return;

                    scrollToTop();
                    parentWindow.setTimeout(scrollToTop, 80);
                    parentWindow.setTimeout(scrollToTop, 240);
                }, true);

                parentWindow.addEventListener('popstate', scrollToTop);
            } catch (error) {
                try { window.scrollTo({ top: 0, left: 0, behavior: 'auto' }); } catch (ignored) {}
            }
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
                    /* Keep the Streamlit 1.54+ sidebar toggles persistently
                       visible and blended with the light sidebar theme. */
                    [data-testid="stSidebarCollapseButton"],
                    [data-testid="stExpandSidebarButton"] {
                        visibility: visible !important;
                        opacity: 1 !important;
                        display: flex !important;
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
public_navbar_active = (
    st.session_state.get("user") is None
    and st.session_state.get("page") in public_pages_list
)

# ================= CLEAN LAYOUT FOR PUBLIC =================
if public_navbar_active:
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
        # Reset to home screen when navigating from navbar (fresh navigation)
        # Check if this is a fresh navigation (navbar click) or a rerun during gameplay
        if st.session_state.get("_games_nav_trigger") != "public":
            st.session_state["game_screen"] = "home"
            st.session_state["game_active"] = False
            st.session_state["is_playing_seq"] = False
            st.session_state["waiting"] = False
            st.session_state["game_sequence"] = []
            st.session_state["player_index"] = 0
            st.session_state["game_level"] = 1
            st.session_state["game_score"] = 0
            st.session_state["game_message"] = ""
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

# Authentication/public pages retain the branded header above. Once signed in,
# remove only its blue-purple fill and shadow; keep Streamlit's header controls.
st.markdown("""
<style>
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.navbar-container) {
        background: transparent !important;
        box-shadow: none !important;
    }
    .mindcare-disclaimer-footer {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1000;
        padding: 7px 16px;
        text-align: center;
        color: #64748b;
        background: rgba(248, 250, 252, 0.94);
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        font: 12px/1.4 'Segoe UI', sans-serif;
        pointer-events: none;
    }
    section.main .block-container { padding-bottom: 3.5rem !important; }
</style>
""", unsafe_allow_html=True)
st.markdown(
    '<div class="mindcare-disclaimer-footer">MindCareAI is an AI support tool, not a substitute for professional clinical advice or medical treatment.</div>',
    unsafe_allow_html=True,
)

# Keep sidebar collapse/expand toggles always visible for logged-in users
st.markdown("""
<style>
/* Streamlit 1.54+: the collapse arrow lives in the sidebar header,
   the expand arrow lives in the fixed header when the sidebar is collapsed.
   The legacy [data-testid="collapsedControl"] selector no longer exists. */
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="stExpandSidebarButton"] {
    z-index: 1000000 !important;
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

elif current == "Exercises":
    show_exercises_page()

elif current == "History":
    # Legacy URLs/session state redirect to Chat; history lives in its sidebar recents.
    st.session_state["current_page"] = "Chat"
    st.query_params["page"] = "Chat"
    st.rerun()

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
