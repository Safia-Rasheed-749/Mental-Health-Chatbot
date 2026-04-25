import streamlit as st

def show_sidebar():
    if not st.session_state.get("user"):
        return

    user = st.session_state.user
    username = user[1] if len(user) > 1 else "User"

    # ===== SIDEBAR STYLING (removed extra spacing, slightly wider) =====
    st.markdown("""
        <style>
            /* Increase sidebar width a bit so "Mood Analytics" fits on one line */
            section[data-testid="stSidebar"] {
                width: 280px !important;
                background-color: #ffffff;
                border-right: 1px solid #e6e6e6;
            }

            /* Remove default top padding from sidebar container (move content up) */
            section[data-testid="stSidebar"] .block-container {
                padding-top: 0rem !important;
                margin-top: -0.5rem !important;
            }

            /* Header (LEFT aligned) – reduced bottom margin */
            .sidebar-header {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 18px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 6px;   /* was 12px */
                margin-top: 0px;
            }

            /* Welcome box – reduced padding and margin */
            .welcome-box {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 8px 10px;    /* was 10px */
                border-radius: 10px;
                background: #f8f9fb;
                margin-bottom: 8px;    /* was 15px */
                border: 1px solid #eee;
                font-size: 14px;
            }

            .welcome-box span {
                font-weight: 600;
            }

            /* Reduce separator margins */
            hr {
                margin-top: 6px !important;
                margin-bottom: 6px !important;
            }

            /* Navigation title – reduced bottom space */
            .nav-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 4px;   /* was 6px */
                color: #444;
            }

            /* Radio items – tighter spacing */
            div[role="radiogroup"] > label {
                margin-bottom: 4px !important;   /* was 8px */
            }

            /* Logout button – consistent with others */
            div.stButton > button {
                background-color: #e74c3c !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 10px !important;
            }

            div.stButton > button:hover {
                background-color: #c0392b !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-header">
                <div style="font-size:22px;">🧠</div>
                <div>MindCare AI</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="welcome-box">
                <div style="font-size:18px;">👤</div>
                <div>Welcome, <span>{username}</span></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        menu = [
            "🏠 Dashboard",
            "💬 Chat",
            "📜 History",
            "😊 Mood Analytics",
            "📓 Journal"
        ]

        current = st.session_state.get("current_page", "Dashboard")
        mapping = {
            "Dashboard": "🏠 Dashboard",
            "Chat": "💬 Chat",
            "History": "📜 History",
            "Mood Analytics": "😊 Mood Analytics",
            "Journal": "📓 Journal"
        }
        reverse_map = {v: k for k, v in mapping.items()}
        current_ui = mapping.get(current, "🏠 Dashboard")

        st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)

        choice = st.radio(
            " ",
            menu,
            index=menu.index(current_ui),
            key="nav"
        )

        if choice != current_ui:
            st.session_state.current_page = reverse_map[choice]
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()