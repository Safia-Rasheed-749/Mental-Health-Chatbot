import streamlit as st
from db import get_conversations, get_messages_by_conversation

def short_title(text, max_len=26):
    text = text.strip()
    return text if len(text) <= max_len else text[:max_len] + "..."

def show_sidebar(user_id=None, current_page="Dashboard"):
    if not st.session_state.get("user"):
        return

    user = st.session_state.user
    username = user[1] if len(user) > 1 else "User"
    user_id = user[0]

    # ================= STRONG SIDEBAR STYLES =================
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            width: 280px !important;
            background-color: #ffffff;
            border-right: 1px solid #e6e6e6;
        }
        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .welcome-box {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: #f8f9fb;
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 14px;
        }
        .section-title {
            font-size: 13px;
            font-weight: 600;
            margin: 10px 0;
            color: #555;
        }
        /* Default button style (grey) for all sidebar buttons */
        section[data-testid="stSidebar"] .stButton button {
            background-color: #f0f2f6 !important;
            border-radius: 30px !important;
            padding: 8px 16px !important;
            margin: 6px 0 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: left !important;
            border: none !important;
            transition: all 0.2s ease !important;
            color: #1e2a3a !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: #e2e6ea !important;
            transform: translateX(4px);
        }
        /* Force logout button to be DARK BLUE by default and on all pages */
        /* Force primary button (logout) to dark blue */
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background-color: #1e3a8a !important;
    color: white !important;
    font-weight: 700 !important;
    justify-content: center !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
    background-color: #2563eb !important;
}
        </style>
    """, unsafe_allow_html=True)

    # ================= PAGE MAP =================
    menu_map = {
        "🏠 Dashboard": "Dashboard",
        "💬 Chat": "Chat",
        "📜 History": "History",
        "😊 Mood Analytics": "Mood Analytics",
        "📓 Journal": "Journal"
    }
    reverse_map = {v: k for k, v in menu_map.items()}
    current_label = reverse_map.get(current_page, "🏠 Dashboard")

    with st.sidebar:
        st.markdown('<div class="sidebar-header">🧠 MindCare AI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="welcome-box">👤 Welcome, <b>{username}</b></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)

        menu = list(menu_map.keys())
        choice = st.radio("", menu, index=menu.index(current_label), key="nav")

        new_page = menu_map[choice]
        if st.session_state.get("current_page") != new_page:
            st.session_state["current_page"] = new_page
            st.rerun()

        st.markdown("---")

        # ================= RECENT SESSIONS (ONLY ON HISTORY, STAY ON HISTORY PAGE) =================
        if st.session_state["current_page"] == "History":
            st.markdown('<div class="section-title">📌 Recent Sessions</div>', unsafe_allow_html=True)
            conversations = get_conversations(user_id)
            if not conversations:
                st.caption("No chats yet. Start a conversation in Chat 💬")
            else:
                for i, convo in enumerate(conversations):
                    convo_id = str(convo[0])
                    messages = get_messages_by_conversation(convo_id)
                    if not messages:
                        continue
                    title = next((m[1] for m in messages if m[0] == "user"), "New Chat")
                    title = short_title(title, 28)
                    if st.button(f"💬 {title}", key=f"sb_{convo_id}_{i}"):
                        # Store selected conversation and stay on History page
                        st.session_state["selected_history_conversation"] = convo_id
                        st.session_state["chat_history"] = messages
                        # DO NOT change current_page – remain on History
                        st.rerun()

        # ================= LOGOUT BUTTON (DARK BLUE) =================
        st.markdown("---")
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn", type="primary"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)