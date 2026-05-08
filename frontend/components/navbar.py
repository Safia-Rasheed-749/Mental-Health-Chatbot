# components/navbar.py — Professional flat sticky navbar (PURE CSS + STREAMLIT BUTTONS)
import streamlit as st

def render_navbar():
    """Renders a professional flat sticky navbar with Streamlit buttons"""
    
    # Inject CSS for navbar
    st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        header, footer, .stDeployButton {
            display: none !important;
        }
        
        /* Main content padding - adjusted for navbar height */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important;
        }
        
        /* NAVBAR CONTAINER - FIXED AT TOP */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 999999 !important;
            background: white !important;
            border-bottom: 1px solid #e5e7eb !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
            padding: 12px 40px !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        /* Logo styling */
        .navbar-logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .navbar-logo-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #e9d5ff 0%, #ddd6fe 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 2px solid rgba(124, 58, 237, 0.2);
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
            animation: avatarPulse 2s ease-in-out infinite;
        }
        
        @keyframes avatarPulse {
            0%, 100% {
                box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
                transform: scale(1);
            }
            50% {
                box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
                transform: scale(1.05);
            }
        }
        
        .navbar-logo-text-wrapper {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .navbar-logo-text {
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.5px;
            line-height: 1;
        }
        
        .navbar-logo-text .ai-part {
            background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .navbar-tagline {
            font-size: 11px;
            font-weight: 500;
            background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
            line-height: 1;
            text-transform: uppercase;
        }
        
        /* Navigation buttons container - align right with less gap */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) > div:last-child {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            gap: 8px !important;
        }
        
        /* Navigation buttons styling - prevent text wrapping */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button {
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            color: #4b5563 !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            padding: 10px 16px !important;
            transition: all 0.2s ease !important;
            border-radius: 6px !important;
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            min-width: fit-content !important;
            line-height: 1 !important;
            vertical-align: middle !important;
        }
        
        /* Hover effect - NO underline, just background color */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button:hover {
            color: #7c3aed !important;
            background: rgba(124, 58, 237, 0.08) !important;
        }
        
        /* Primary button (Get Started) - same height as others */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button[kind="primary"] {
            color: #7c3aed !important;
            font-weight: 600 !important;
            height: 40px !important;
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            line-height: 1 !important;
            vertical-align: middle !important;
            padding: 10px 16px !important;
            margin: 0 !important;
        }
        
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button[kind="primary"]:hover {
            color: #6366f1 !important;
            background: rgba(99, 102, 241, 0.08) !important;
        }
        
        /* Force all button containers to same height */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) div[data-testid="column"] button {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* Remove button container padding and set equal width */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) div[data-testid="column"] {
            padding: 0 !important;
            min-width: auto !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Make all buttons same width */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) div[data-testid="column"] > div {
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navbar with Streamlit columns - more space for nav buttons on right
    col_logo, col_spacer, col_nav = st.columns([1, 1.5, 1.5])
    
    with col_logo:
        st.markdown('<div class="navbar-container"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="navbar-logo-container">
            <div class="navbar-logo-avatar">🧠</div>
            <div class="navbar-logo-text-wrapper">
                <span class="navbar-logo-text">MindCare<span class="ai-part">AI</span></span>
                <span class="navbar-tagline">Mental Wellness</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_spacer:
        # Empty spacer column
        pass
    
    with col_nav:
        nav_cols = st.columns(5)
        
        with nav_cols[0]:
            if st.button("Home", key="nav_home", type="secondary"):
                st.session_state.page = "landing"
                st.rerun()
        
        with nav_cols[1]:
            if st.button("About", key="nav_about", type="secondary"):
                st.session_state.page = "about"
                st.rerun()
        
        with nav_cols[2]:
            if st.button("Exercises", key="nav_exercises", type="secondary"):
                st.session_state.page = "exercises"
                st.rerun()
        
        with nav_cols[3]:
            if st.button("Games", key="nav_games", type="secondary"):
                st.session_state.page = "games"
                st.rerun()
        
        with nav_cols[4]:
            if st.button("Get Started", key="nav_auth", type="primary"):
                st.session_state.page = "auth"
                st.rerun()
