# components/navbar.py – Original version (Image 2)
import streamlit as st

def render_navbar():
    st.markdown("""
    <style>
        .nav-container {
            background: linear-gradient(135deg, #9FC6F0, #4F84D9) !important;
            padding: 12px 30px !important;
            border-radius: 60px !important;
            box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3) !important;
            margin: 10px 0 20px 0 !important;   /* top margin reduced to 10px (was maybe larger) */
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 36px;
            font-weight: 700;
            color: #6D9EEB !important;
        }
        .logo-icon {
            font-size: 36px;
        }
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
            width: auto !important;
            cursor: pointer !important;
            white-space: nowrap !important;
            margin: 0 10px !important;
        }
        div.stButton > button:hover {
            background: #6D9EEB !important;
            transform: translateY(-3px) !important;
        }
        button[key^="nav_getstarted"] {
            background: #7C3AED !important;
        }
        button[key^="nav_getstarted"]:hover {
            background: #6D28D9 !important;
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
        }
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("""
        <div class="logo">
            <span class="logo-icon">🧠</span>
            <span>Mind Care AI</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
        with nav_col1:
            if st.button("🏠 Home", key="nav_home_shared"):
                st.session_state.page = "landing"
                st.rerun()
        with nav_col2:
            if st.button("📖 About", key="nav_about_shared"):
                st.session_state.page = "about"
                st.rerun()
        with nav_col3:
            if st.button("📊 Demo", key="nav_demo_shared"):
                st.session_state.page = "demo"
                st.rerun()
        with nav_col4:
            if st.button("🎮 Games", key="nav_games_shared"):
                st.session_state.page = "games"
                st.rerun()
        with nav_col5:
            if st.button("🚀 Get Started", key="nav_getstarted_shared"):
                st.session_state.page = "auth"
                st.rerun()