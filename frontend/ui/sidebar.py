import streamlit as st

def init_sidebar_state():
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True


def show_sidebar():

    init_sidebar_state()

    # ✅ FIX: minimal safe CSS (NO width override)
    st.markdown("""
        <style>
        /* Ensure sidebar is visible */
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }

        /* Hide default navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Fix collapse button */
        button[kind="header"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        /* 🔥 IMPORTANT: Fix button text clipping */
        section[data-testid="stSidebar"] .stButton button {
            width: 100% !important;
            white-space: nowrap !important;
            overflow: visible !important;
        }

        </style>
    """, unsafe_allow_html=True)

    if "user" not in st.session_state or st.session_state.user is None:
        st.error("Please login first")
        return False

    try:
        username = st.session_state.user[1] if len(st.session_state.user) > 1 else "User"
    except:
        username = "User"

    with st.sidebar:
        st.markdown("## 🧠 MindCare AI")
        st.write(f"Welcome **{username}**")

        st.markdown("---")

        menu_options = ["Dashboard", "Chat", "History", "Mood Analytics", "Journal"]

        current_page = st.session_state.get("current_page", "Dashboard")

        if current_page not in menu_options:
            current_page = "Dashboard"
            st.session_state.current_page = current_page

        default_index = menu_options.index(current_page)

        menu = st.radio(
            "Navigation",
            menu_options,
            index=default_index,
            key="sidebar_navigation"
        )

        if menu != st.session_state.current_page:
            st.session_state.current_page = menu
            st.rerun()

        st.markdown("---")

        # ✅ KEEP NORMAL BUTTON (no width hacks here)
        if st.button("🚪 Logout", type="primary"):
            logout_and_cleanup()
            st.rerun()
            return False

    return True


def logout_and_cleanup():
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.session_state.page = "landing"

    keys_to_clear = ['chat_history', 'demo_messages', 'demo_count']
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state[key] = [] if key == 'chat_history' else ([] if 'messages' in key else 0)

    st.session_state.sidebar_visible = False