import streamlit as st
from db import get_conversations, get_messages_by_conversation, rename_conversation, delete_conversation

def short_title(text, max_len=18):
    """Convert first user message into a short generic session title."""
    text_lower = text.lower().strip()
    mood_keywords = {
        "sad": "Sadness", "depress": "Depression", "stress": "Stress",
        "anxious": "Anxiety", "anxiety": "Anxiety", "panic": "Panic",
        "happy": "Happiness", "angry": "Anger", "fear": "Fear",
        "lonely": "Loneliness", "tired": "Fatigue", "overthink": "Overthinking",
        "motivation": "Motivation", "relationship": "Relationship",
        "study": "Studies", "exam": "Exams", "sleep": "Sleep Issues",
        "work": "Work Stress", "family": "Family Issues"
    }
    for keyword, title in mood_keywords.items():
        if keyword in text_lower:
            return title
    words = text.strip().split()
    if len(words) >= 2:
        fallback = " ".join(words[:2])
    elif len(words) == 1:
        fallback = words[0]
    else:
        fallback = "New Chat"
    return fallback if len(fallback) <= max_len else fallback[:max_len] + "..."


def show_sidebar(user_id=None, current_page="Dashboard"):
    if not st.session_state.get("user"):
        return

    user = st.session_state.user
    username = user[1] if len(user) > 1 else "User"
    user_id = user[0]

    st.markdown("""
    <style>
    /* ── SIDEBAR CONTAINER ── */
    section[data-testid="stSidebar"] {
        width: 260px !important;
        background: linear-gradient(180deg, #44556C 0%, #526581 50%, #607592 100%) !important;
        border-right: 1px solid rgba(180,200,220,0.15) !important;
        box-shadow: 2px 0 12px rgba(15,23,42,0.06) !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.6rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-bottom: 0.7rem !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }

    /* ── HEADER ── */
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 2px 0 10px 0;
        margin-bottom: 4px;
    }
    .sidebar-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        border: 2px solid rgba(255,255,255,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.12);
        animation: avatarPulse 3s ease-in-out infinite;
    }
    @keyframes avatarPulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(255,255,255,0.12); }
        50%       { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
    }
    .sidebar-brand {
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
        letter-spacing: 0.2px;
    }

    /* ── DIVIDER ── */
    hr {
        margin-top: 6px !important;
        margin-bottom: 6px !important;
        border-color: rgba(74,127,212,0.2) !important;
    }

    /* ── SECTION LABEL ── */
    section[data-testid="stSidebar"] .sb-section-label {
        font-size: 13px !important;
        font-weight: 800 !important;
        letter-spacing: 1.6px !important;
        text-transform: uppercase !important;
        margin: 16px 0 10px 2px !important;
        color: #ffffff !important;
        display: block !important;
        opacity: 1 !important;
    }

    /* ── NAVIGATION RADIO ── */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 1px !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 5px 8px !important;
        border-radius: 8px !important;
        transition: background 0.15s !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.12) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: rgba(255,255,255,0.92) !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }

    /* ── ALL SIDEBAR BUTTONS ── */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 5px 10px !important;
        margin: 1px 0 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        text-align: left !important;
        color: rgba(226,232,240,0.88) !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        /* Neutralise any page-level overrides */
        height: auto !important;
        min-height: auto !important;
        max-width: none !important;
        display: block !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        transform: translateX(2px) !important;
        box-shadow: none !important;
    }

    /* ── PROTECT SIDEBAR COLUMNS from page-level column rules ── */
    section[data-testid="stSidebar"] div[data-testid="column"] {
        padding: 0 !important;
        background: transparent !important;
        gap: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
        background: transparent !important;
        align-items: center !important;
    }

    /* ── DIVIDER (scoped so mood/journal hr rules don't override) ── */
    section[data-testid="stSidebar"] hr {
        margin-top: 6px !important;
        margin-bottom: 6px !important;
        border-color: rgba(255,255,255,0.15) !important;
        background: none !important;
        height: auto !important;
    }

    /* ── LOGOUT (primary) ── */
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #e05a5a 0%, #f07070 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        text-align: center !important;
        margin-top: 4px !important;
        box-shadow: 0 3px 10px rgba(224,90,90,0.35) !important;
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #d04848 0%, #e06060 100%) !important;
        box-shadow: 0 4px 14px rgba(224,90,90,0.50) !important;
        transform: none !important;
    }
    .logout-btn { margin-top: 36px !important; padding-top: 16px !important; border-top: 1px solid rgba(255,255,255,0.15) !important; }

    /* ── NEW CHAT BUTTON ── */
    .new-chat-btn .stButton button {
        background: rgba(74,127,212,0.18) !important;
        border: 1px solid rgba(74,127,212,0.35) !important;
        border-radius: 8px !important;
        color: #93c5fd !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        padding: 7px 12px !important;
        margin-bottom: 6px !important;
    }
    .new-chat-btn .stButton button:hover {
        background: rgba(74,127,212,0.28) !important;
        border-color: rgba(74,127,212,0.6) !important;
        transform: none !important;
    }

    /* ── SESSION ITEMS ── */
    .session-item {
        border-radius: 8px;
        padding: 0;
        margin-bottom: 1px;
        transition: background 0.15s;
    }
    .session-item:hover { background: rgba(255,255,255,0.04); }
    .session-active {
        background: rgba(74,127,212,0.2) !important;
        border-left: 2px solid #5fa8e0 !important;
        padding-left: 2px !important;
    }
    .session-title-btn .stButton button {
        color: rgba(203,213,225,0.85) !important;
        font-size: 12.5px !important;
        font-weight: 400 !important;
        padding: 5px 8px !important;
        border-radius: 6px !important;
        text-align: left !important;
    }
    .session-title-btn .stButton button:hover {
        color: #ffffff !important;
        background: rgba(255,255,255,0.06) !important;
        transform: none !important;
    }
    .session-active .session-title-btn .stButton button {
        color: #93c5fd !important;
        font-weight: 500 !important;
    }
    .session-menu-btn .stButton button {
        color: rgba(148,163,184,0.45) !important;
        font-size: 14px !important;
        padding: 3px 6px !important;
        border-radius: 5px !important;
        width: auto !important;
        min-width: 26px !important;
    }
    .session-menu-btn .stButton button:hover {
        color: #e2e8f0 !important;
        background: rgba(255,255,255,0.08) !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── PAGE MAP ──
    menu_map = {
        "🏠 Dashboard":      "Dashboard",
        "💬 Chat":           "Chat",
        "😊 Mood Analytics": "Mood Analytics",
        "📓 Journal":        "Journal",
        "🎮 Games":          "Games",
    }
    reverse_map = {v: k for k, v in menu_map.items()}
    current_label = reverse_map.get(current_page, "🏠 Dashboard")

    with st.sidebar:

        # ── HEADER — top left ──
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-avatar">🧠</div>
            <div class="sidebar-brand">MindCare AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="sb-section-label">Navigation</div>', unsafe_allow_html=True)

        menu = list(menu_map.keys())
        choice = st.radio("", menu, index=menu.index(current_label), key="nav")
        new_page = menu_map[choice]

        if st.session_state.get("current_page") != new_page:
            st.session_state["current_page"] = new_page
            for k in list(st.session_state.keys()):
                if k.startswith("rename_") or k.startswith("menu_open_"):
                    del st.session_state[k]
            st.rerun()

        # ── SESSION TABS — only on Chat page ──
        if st.session_state.get("current_page") == "Chat":
            st.markdown("---")

            st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
            if st.button("✏️  New Chat", key="new_chat_btn"):
                st.session_state["conversation_id"] = None
                st.session_state["chat_history"] = []
                st.session_state["last_loaded_chat"] = None
                for k in list(st.session_state.keys()):
                    if k.startswith("rename_") or k.startswith("menu_open_"):
                        del st.session_state[k]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sb-section-label">Recent Sessions</div>', unsafe_allow_html=True)

            conversations = get_conversations(user_id)

            valid_convos = []
            for convo in conversations:
                msgs = get_messages_by_conversation(str(convo[0]))
                if msgs:
                    valid_convos.append((convo, msgs))

            if not valid_convos:
                st.markdown('<p style="color:rgba(148,163,184,0.5);font-size:11.5px;padding:3px 2px;">No sessions yet. Start chatting!</p>', unsafe_allow_html=True)
            else:
                active_cid = str(st.session_state.get("conversation_id", ""))

                for convo, msgs in valid_convos:
                    convo_id = str(convo[0])
                    db_title = convo[1] if convo[1] and convo[1] != "New Chat" else None

                    if db_title:
                        display_title = db_title[:22] + "..." if len(db_title) > 22 else db_title
                    else:
                        first_user = next((m[1] for m in msgs if m[0] == "user"), "New Chat")
                        display_title = short_title(first_user, 22)

                    is_active = (convo_id == active_cid)
                    is_renaming = st.session_state.get(f"rename_{convo_id}", False)
                    menu_open = st.session_state.get(f"menu_open_{convo_id}", False)

                    active_class = "session-item session-active" if is_active else "session-item"
                    st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)

                    if is_renaming:
                        new_name = st.text_input(
                            "", value=display_title,
                            key=f"rename_input_{convo_id}",
                            label_visibility="collapsed"
                        )
                        col_save, col_cancel = st.columns([1, 1])
                        with col_save:
                            if st.button("✓", key=f"save_rename_{convo_id}"):
                                if new_name.strip():
                                    rename_conversation(convo_id, new_name.strip())
                                st.session_state[f"rename_{convo_id}"] = False
                                st.rerun()
                        with col_cancel:
                            if st.button("✕", key=f"cancel_rename_{convo_id}"):
                                st.session_state[f"rename_{convo_id}"] = False
                                st.rerun()

                    elif menu_open:
                        st.markdown(f'<p style="color:rgba(226,232,240,0.65);font-size:11.5px;padding:2px 4px;margin:0;">📝 {display_title}</p>', unsafe_allow_html=True)
                        col_r, col_d, col_c = st.columns([1, 1, 1])
                        with col_r:
                            if st.button("✏️ Rename", key=f"do_rename_{convo_id}"):
                                st.session_state[f"menu_open_{convo_id}"] = False
                                st.session_state[f"rename_{convo_id}"] = True
                                st.rerun()
                        with col_d:
                            if st.button("🗑️ Delete", key=f"do_delete_{convo_id}"):
                                delete_conversation(convo_id)
                                st.session_state[f"menu_open_{convo_id}"] = False
                                if convo_id == active_cid:
                                    st.session_state["conversation_id"] = None
                                    st.session_state["chat_history"] = []
                                    st.session_state["last_loaded_chat"] = None
                                st.rerun()
                        with col_c:
                            if st.button("✕", key=f"close_menu_{convo_id}"):
                                st.session_state[f"menu_open_{convo_id}"] = False
                                st.rerun()

                    else:
                        col_title, col_menu = st.columns([5, 1])
                        with col_title:
                            st.markdown('<div class="session-title-btn">', unsafe_allow_html=True)
                            if st.button(f"💬 {display_title}", key=f"sess_{convo_id}"):
                                st.session_state["conversation_id"] = convo_id
                                st.session_state["chat_history"] = msgs
                                st.session_state["last_loaded_chat"] = convo_id
                                st.session_state["current_page"] = "Chat"
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col_menu:
                            st.markdown('<div class="session-menu-btn">', unsafe_allow_html=True)
                            if st.button("⋯", key=f"menu_{convo_id}"):
                                for k in list(st.session_state.keys()):
                                    if k.startswith("menu_open_") and k != f"menu_open_{convo_id}":
                                        st.session_state[k] = False
                                st.session_state[f"menu_open_{convo_id}"] = True
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn", type="primary"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
