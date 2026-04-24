import streamlit as st

def show_sidebar():
    if not st.session_state.get("user"):
        return

    user = st.session_state.user
    username = user[1] if len(user) > 1 else "User"

    # ===== GLOBAL SIDEBAR STYLING =====
    st.markdown("""
        <style>
            /* Reduce sidebar width */
            section[data-testid="stSidebar"] {
                width: 250px !important;
                min-width: 250px !important;
                max-width: 250px !important;
                background-color: #ffffff;
                border-right: 1px solid #e6e6e6;
            }

            /* Header (LEFT aligned) */
            .sidebar-header {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 18px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 12px;
            }

            /* Welcome box with icon */
            .welcome-box {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px;
                border-radius: 10px;
                background: #f8f9fb;
                margin-bottom: 15px;
                border: 1px solid #eee;
                font-size: 14px;
            }

            .welcome-box span {
                font-weight: 600;
            }

            /* Navigation title */
            .nav-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 6px;
                color: #444;
            }

            /* Radio spacing */
            div[role="radiogroup"] > label {
                margin-bottom: 8px !important;
            }

            /* Logout button */
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
        # ===== LEFT ALIGNED HEADER =====
        st.markdown(f"""
            <div class="sidebar-header">
                <div style="font-size:22px;">🧠</div>
                <div>MindCare AI</div>
            </div>
        """, unsafe_allow_html=True)

        # ===== USER WELCOME WITH ICON =====
        st.markdown(f"""
            <div class="welcome-box">
                <div style="font-size:18px;">👤</div>
                <div>Welcome, <span>{username}</span></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ================= MENU =================
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

        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()