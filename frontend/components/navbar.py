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
        /* ═══════════════════════════════════════════════════════════════
           NAVBAR BACKGROUND COLOR - EASY CUSTOMIZATION
           ═══════════════════════════════════════════════════════════
           
           🎨 CURRENT: Soft purple gradient (RECOMMENDED - Best theme match)
           - Start: #a78bfa (Light purple)
           - End: #c4b5fd (Lighter purple)
           
           💡 HOW TO CHANGE:
           Replace the gradient colors below with your preferred colors
           
           🌈 COLOR PRESETS:
           
           OPTION 1 - Soft Purple (Current - RECOMMENDED):
           background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%) !important;
           
           OPTION 2 - Blue-Purple Blend:
           background: linear-gradient(135deg, #8b7dd8 0%, #c77dbb 100%) !important;
           
           OPTION 3 - Calm Blue:
           background: linear-gradient(135deg, #93c5fd 0%, #a5b4fc 100%) !important;
           
           OPTION 4 - Pure White:
           background: white !important;
           
           ═══════════════════════════════════════════════════════════════ */
        
        /* NAVBAR CONTAINER - FIXED AT TOP */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 999999 !important;
            
            /* 🎨 NAVBAR BACKGROUND - Soft purple (best theme match) */
            background: linear-gradient(90deg, 
    #3D43B4 0%,    /* Darker Blue */
    #7130C3 25%,   /* Deep Purple */
    #9B45E4 50%,   /* Vibrant Purple */
    #BD39D1 75%,   /* Magenta shade */
    #D33A86 100%   /* Deep Pink */
); !important;
            
            border-bottom: 1px solid rgba(167, 139, 250, 0.3) !important;
            box-shadow: 0 4px 12px rgba(167, 139, 250, 0.25) !important;
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
            background: rgba(255, 255, 255, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 2px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.15);
            animation: avatarPulse 3s ease-in-out infinite;
        }
        
        @keyframes avatarPulse {
            0%, 100% {
                box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.15);
            }
            50% {
                box-shadow: 0 0 0 8px rgba(255, 255, 255, 0.08);
            }
        }
        
        .navbar-logo-text-wrapper {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        /*title color change */
        .navbar-logo-text {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.5px;
            line-height: 1;
        }
        
        .navbar-logo-text .ai-part {
            color: #ffffff;
        }
        
        .navbar-tagline {
            font-size: 11px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
            letter-spacing: 1px;
            line-height: 1;
            text-transform: uppercase;
        }
        
        /* ═══════════════════════════════════════════════════════════════
           BUTTON SPACING - Equal gap between all buttons
           ═══════════════════════════════════════════════════════════════
           
           💡 HOW TO CHANGE GAP:
           Change the "gap" value below
           
           CURRENT: 12px (equal spacing)
           
           OPTIONS:
           - Tight: gap: 8px !important;
           - Normal: gap: 12px !important;
           - Loose: gap: 16px !important;
           - Extra Loose: gap: 20px !important;
           
           ═══════════════════════════════════════════════════════════════ */
        
        /* Navigation buttons container - align right with equal gap */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) > div:last-child {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            
            /* 🎨 BUTTON GAP - CHANGE HERE */
            gap: 12px !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════
           NAVBAR BUTTONS - WHITE TEXT ON PURPLE BACKGROUND
           ═══════════════════════════════════════════════════════════
           
           🎨 DESIGN: White text buttons (matching screenshot)
           - Transparent background
           - White text color
           - Subtle hover effect with lighter background
           
           💡 HOW TO CHANGE BUTTON TEXT COLOR:
           Change the "color" property below
           
           🌈 COLOR OPTIONS:
           
           CURRENT - White (from screenshot):
           color: #ffffff !important;
           
           OPTION 2 - Light Purple:
           color: #e9d5ff !important;
           
           OPTION 3 - Light Pink:
           color: #fbcfe8 !important;
           
           ═══════════════════════════════════════════════════════════════ */
        
        /* Navigation buttons styling - prevent text wrapping */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button {
            /* 🎨 TRANSPARENT BACKGROUND - No background color */
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            
            /* 🎨 TEXT COLOR - WHITE (from screenshot) */
            color: #ffffff !important;
            
            font-size: 15px !important;
            font-weight: 600 !important;
            padding: 10px 16px !important;
            transition: all 0.2s ease !important;
            border-radius: 8px !important;
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            min-width: 100px !important;
            line-height: 1 !important;
            vertical-align: middle !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════
           HOVER EFFECT - Lighter background on hover
           ═══════════════════════════════════════════════════════════════
           
           💡 WHAT IT DOES:
           - Keeps text white
           - Adds subtle white background (20% opacity)
           
           ═══════════════════════════════════════════════════════════════ */
        
        /* Hover effect */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button:hover {
            /* 🎨 HOVER - White text with light background */
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Primary button (Get Started) - same style as others */
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button[kind="primary"] {
            color: #ffffff !important;
            font-weight: 600 !important;
            height: 40px !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            line-height: 1 !important;
            vertical-align: middle !important;
            padding: 10px 16px !important;
            margin: 0 !important;
            min-width: 100px !important;
        }
        
        div[data-testid="stHorizontalBlock"]:has(.navbar-container) button[kind="primary"]:hover {
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.2) !important;
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
                # Reset game state when navigating to Games from navbar
                st.session_state["game_screen"] = "home"
                st.session_state["game_active"] = False
                st.session_state["game_sequence"] = []
                st.session_state["player_index"] = 0
                st.session_state["game_level"] = 1
                st.session_state["game_score"] = 0
                st.session_state["is_playing_seq"] = False
                st.session_state["waiting"] = False
                st.session_state["game_message"] = ""
                st.session_state["_games_nav_trigger"] = None
                st.session_state.page = "games"
                st.rerun()
        
        with nav_cols[4]:
            if st.button("Get Started", key="nav_auth", type="primary"):
                st.session_state.page = "auth"
                st.rerun()
