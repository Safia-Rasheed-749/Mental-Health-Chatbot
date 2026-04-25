# components/navbar.py
import streamlit as st

def render_navbar():
    """
    Renders the same styled navigation bar on any page.
    Manages page switching via session_state.
    """
    # Navbar HTML/CSS – identical to what you already have
    st.markdown("""
    <style>
        /* Remove ALL default padding from top */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        section.main > div {
            padding-top: 0rem !important;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #ffffff, #eaf6fb, #d6ecf7);
        }
        header, #MainMenu, footer {visibility: hidden;}
        .stApp {
            margin-top: -80px !important;
        }
        .nav-container {
            background: purple !important;
            padding: 12px 30px !important;
            border-radius: 60px !important;
            box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3) !important;
            margin: 10px 0 30px 0 !important;
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
        /* Shared navbar button style */
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
            box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3) !important;
        }
        button[key^="nav_getstarted"] {
            background: purple !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            padding: 6px 22px !important;
        }
        button[key^="nav_getstarted"]:hover {
            background: #ff4444 !important;
        }
        button[key^="nav_games"] {
            background: linear-gradient(135deg, #A8E6CF, #3B82F6) !important;
        }
        button[key^="nav_games"]:hover {
            background: #3B82F6 !important;
        }
        .stColumn {
            display: flex;
            justify-content: center;
            gap: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Layout: logo on left, buttons on right
    col1, col2 = st.columns([1, 1.2])  # Increased right column width for 4 buttons
    
    with col1:
        st.markdown("""
            <div class="logo">
                <span class="logo-icon">🧠</span>
                <span>Mind Care AI</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Now 4 buttons: Home, Games, About, Get Started
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 1, 1, 1])
        
        with nav_col1:
            if st.button("🏠 Home", key="nav_home_shared", use_container_width=False):
                st.session_state.page = "landing"
                st.rerun()
        with nav_col2:
            if st.button("📖 About", key="nav_about_shared", use_container_width=False):
                st.session_state.page = "about"
                st.rerun()
        with nav_col3:
            if st.button("📖 Demo", key="nav_demo_shared", use_container_width=False):
                st.session_state.page = "demo"
                st.rerun()
        with nav_col4:
            if st.button("🎮 Games", key="nav_games_shared", use_container_width=False):
                st.session_state.page = "games"
                st.rerun()
        with nav_col5:
            if st.button("🚀 Get Started", key="nav_getstarted_shared", use_container_width=False):
                st.session_state.page = "auth"
                st.rerun()