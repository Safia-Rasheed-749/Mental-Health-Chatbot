# components/navbar.py
import streamlit as st

def render_navbar():
    """
    Renders a consistent, edge-to-top navigation bar on any page.
    Call this function as the very first thing in your page script.
    """
    # Global CSS to remove ALL default top white space from Streamlit
    st.markdown("""
    <style>
        /* 1. Remove padding/margins from the outermost containers */
        html, body, [data-testid="stAppViewContainer"], 
        .main, .block-container, section.main > div {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 2. Remove default top padding from the block container */
        .main .block-container {
            padding-top: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* 3. Make the root app container start at the very top */
        .stApp {
            margin-top: 0 !important;
        }

        /* 4. Hide Streamlit's default header, menu, footer */
        header, #MainMenu, footer {
            visibility: hidden;
            height: 0;
        }

        /* 5. Background gradient (consistent across pages) */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #ffffff, #eaf6fb, #d6ecf7);
        }

        /* 6. Navbar container style — sits flush at the top */
        .nav-container {
            background: purple !important;
            padding: 12px 30px !important;
            border-radius: 60px !important;
            box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3) !important;
            margin: 0 0 30px 0 !important;   /* no top margin, only bottom margin */
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from { transform: translateY(-100px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Logo styling */
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 36px;
            font-weight: 700;
            color: #6D9EEB !important;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .logo-icon {
            font-size: 36px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        }

        /* Navbar button styles (shared) */
        div.stButton > button {
            all: unset !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: linear-gradient(135deg, #9FC6F0, #4F84D9) !important;
            color: white !important;
            font-weight: 500 !important;
            padding: 6px 18px !important;
            border-radius: 40px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            min-width: auto !important;
            cursor: pointer !important;
            line-height: normal !important;
            height: auto !important;
            white-space: nowrap !important;
            margin: 0 10px !important;
        }
        div.stButton > button:hover {
            background: #6D9EEB !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        }
        button[key^="nav_getstarted"] {
            background: purple !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            padding: 6px 22px !important;
        }
        button[key^="nav_getstarted"]:hover {
            background: #ff4444 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Layout: logo left, buttons right
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
            <div class="logo">
                <span class="logo-icon">🧠</span>
                <span>Mind Care AI</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1.2])
        with nav_col1:
            if st.button("🏠 Home", key="nav_home_shared", use_container_width=False):
                st.session_state.page = "landing"
                st.rerun()
        with nav_col2:
            if st.button("📖 About", key="nav_about_shared", use_container_width=False):
                st.session_state.page = "about"
                st.rerun()
        with nav_col3:
            if st.button("🚀 Demo", key="nav_demo_shared", use_container_width=False):
                # Reset demo state when going to demo page
                st.session_state.demo_messages = []
                st.session_state.demo_count = 0
                st.session_state.page = "demo"
                st.rerun()
        with nav_col4:
            if st.button("🚀 Get Started", key="nav_getstarted_shared", use_container_width=False):
                st.session_state.page = "auth"
                st.rerun()