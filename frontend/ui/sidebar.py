import streamlit as st

def show_sidebar():

    if not st.session_state.get("user"):
        return

    user = st.session_state.user
    username = user[1] if len(user) > 1 else "User"
    is_admin = len(user) > 3 and user[3]

    with st.sidebar:

        # ================= HEADER (PROFESSIONAL) =================
        st.markdown("""
            <div style="
                padding: 15px 10px;
                border-radius: 12px;
                background: linear-gradient(135deg, #a8d8ff, #d6ecff);
                text-align: center;
                margin-bottom: 15px;
            ">
                <h2 style="color:white; margin:0;">🧠 MindCare AI</h2>
            </div>
        """, unsafe_allow_html=True)

        # ================= WELCOME USER =================
        st.markdown(f"""
            <div style="
                padding: 10px;
                border-radius: 10px;
                background: #f5f7fa;
                text-align: center;
                margin-bottom: 10px;
            ">
                <h4 style="margin:0;">👋 Welcome, <b>{username}</b></h4>
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

        if is_admin:
            menu.append("🛡️ Admin Panel")

        current = st.session_state.get("current_page", "Dashboard")

        # normalize current selection
        mapping = {
            "Dashboard": "🏠 Dashboard",
            "Chat": "💬 Chat",
            "History": "📜 History",
            "Mood Analytics": "😊 Mood Analytics",
            "Journal": "📓 Journal",
            "Admin Panel": "🛡️ Admin Panel"
        }

        reverse_map = {v: k for k, v in mapping.items()}

        if current in mapping:
            current_ui = mapping[current]
        else:
            current_ui = "🏠 Dashboard"

        # ================= NAVIGATION TITLE =================
        st.markdown("""
            <div style="
                font-size:18px;
                font-weight:700;
                margin-bottom:8px;
                color:#333;
            ">
                Navigation
            </div>
        """, unsafe_allow_html=True)

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

        # ================= LOGOUT BUTTON =================
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #e74c3c !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px !important;
        }
        div.stButton > button:hover {
            background-color: #c0392b !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()