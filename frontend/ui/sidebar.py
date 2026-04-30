import streamlit as st
from db import get_conversations, get_messages_by_conversation, rename_conversation

def short_title(text, max_len=18):
    """
    Convert first user message into a short generic session title.
    """
    text_lower = text.lower().strip()

    mood_keywords = {
        "sad": "Sadness",
        "depress": "Depression",
        "stress": "Stress",
        "anxious": "Anxiety",
        "anxiety": "Anxiety",
        "panic": "Panic",
        "happy": "Happiness",
        "angry": "Anger",
        "fear": "Fear",
        "lonely": "Loneliness",
        "tired": "Fatigue",
        "overthink": "Overthinking",
        "motivation": "Motivation",
        "relationship": "Relationship",
        "study": "Studies",
        "exam": "Exams",
        "sleep": "Sleep Issues",
        "work": "Work Stress",
        "family": "Family Issues"
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

    # ================= STRONG SIDEBAR STYLES =================
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            width: 280px !important;
            background: linear-gradient(145deg, rgba(12,22,48,0.85), rgba(12,22,48,0.55));
            border-right: 1px solid rgba(148,163,184,0.18);
            box-shadow: 0 18px 60px rgba(0,0,0,0.25);
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.2rem !important;
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
            padding-bottom: 0.7rem !important;
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 10px;
            font-size: 22px;
            font-weight: 900;
            margin-top: -8px;
            margin-left: -2px;
            margin-bottom: 14px;
            padding: 0;
            line-height: 1.1;
            color: rgba(196,181,253,0.98);
            text-shadow: 0 0 18px rgba(124,58,237,0.25);
        }

        .sidebar-brain-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 0 0 3px rgba(167,139,250,0.25);
            animation: sidebarPulse 3s ease-in-out infinite;
            flex-shrink: 0;
        }
        @keyframes sidebarPulse {
            0%, 100% { box-shadow: 0 0 0 3px rgba(167,139,250,0.25); }
            50%       { box-shadow: 0 0 0 6px rgba(167,139,250,0.12); }
        }

        .welcome-box {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: rgba(15,23,42,0.45);
            border: 1px solid rgba(148,163,184,0.18);
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 14px;
        }

        .section-title {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.3px;
            margin: 10px 0 8px 2px;
            color: rgba(226,232,240,0.78);
        }

        hr {
            margin-top: 10px !important;
            margin-bottom: 10px !important;
        }

        section[data-testid="stSidebar"] .stButton button {
            background-color: rgba(15,23,42,0.35) !important;
            border: 1px solid rgba(148,163,184,0.18) !important;
            border-radius: 30px !important;
            padding: 8px 16px !important;
            margin: 4px 0 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: left !important;
            border: none !important;
            transition: all 0.2s ease !important;
            color: #F8FAFC !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }

        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: rgba(59,130,246,0.10) !important;
            transform: translateX(4px);
        }

        div[role="radiogroup"] {
            gap: 0.2rem !important;
        }

        section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #4a7fd4 0%, #5fa8e0 55%, #7ecde8 100%);
            border: 1px solid rgba(255,255,255,0.12) !important;
            color: white !important;
            font-weight: 900 !important;
            justify-content: center !important;
        }

        section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
            filter: brightness(1.06);
        }

        section[data-testid="stSidebar"] .stButton button[aria-checked="true"],
        section[data-testid="stSidebar"] .stButton button[data-state="checked"] {
            background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(124,58,237,0.28)) !important;
            border: 1px solid rgba(124,58,237,0.55) !important;
            color: #ffffff !important;
            box-shadow: 0 18px 60px rgba(124,58,237,0.18);
        }

        .logout-btn {
            margin-top: 30px !important;
            margin-bottom: -2px !important;
            padding-bottom: 0 !important;
            
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] .stButton button:not([kind="primary"]) {
            background-color: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            color: #FFFFFF !important;
            box-shadow: none !important;
        }

        section[data-testid="stSidebar"] .stButton button:not([kind="primary"]):hover {
            background-color: rgba(59,130,246,0.15) !important;
            transform: translateX(4px);
        }

        /* ===== SESSION TABS STYLES (CHAT-INSPIRED) ===== */
        .session-item {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 12px;
            border-radius: 12px;
            margin-bottom: 6px;
            cursor: pointer;
            transition: all 0.2s;
            background: rgba(15,23,42,0.25);
            border: 1px solid rgba(148,163,184,0.12);
        }
        .session-item:hover {
            background: rgba(99,102,241,0.15);
            border-color: rgba(99,102,241,0.25);
            transform: translateX(3px);
        }
        .session-item.active-session {
            background: linear-gradient(135deg, rgba(99,102,241,0.28), rgba(139,92,246,0.28)) !important;
            border: 1px solid rgba(139,92,246,0.45) !important;
            box-shadow: 0 4px 12px rgba(99,102,241,0.20);
        }
        .session-label {
            font-size: 13px;
            color: #e2e8f0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 170px;
            flex: 1;
            font-weight: 500;
        }
        .session-dots {
            opacity: 0;
            font-size: 18px;
            color: rgba(226,232,240,0.85);
            padding: 2px 6px;
            border-radius: 6px;
            cursor: pointer;
            transition: opacity 0.15s, background 0.15s;
            flex-shrink: 0;
        }
        .session-item:hover .session-dots {
            opacity: 1;
        }
        .session-dots:hover {
            background: rgba(99,102,241,0.25);
        }

        /* Dropdown menu - chat styled */
        .session-dropdown {
            position: absolute;
            right: 0;
            top: 38px;
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(99,102,241,0.30);
            border-radius: 12px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.45);
            z-index: 9999;
            min-width: 150px;
            overflow: hidden;
        }
        .session-dropdown-item {
            padding: 10px 16px;
            font-size: 13px;
            color: #e2e8f0;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: background 0.15s;
            font-weight: 500;
        }
        .session-dropdown-item:hover {
            background: rgba(99,102,241,0.22);
        }
        .session-dropdown-item.delete-item {
            color: #fca5a5;
        }
        .session-dropdown-item.delete-item:hover {
            background: rgba(239,68,68,0.18);
        }

        /* New Chat button - gradient style */
        section[data-testid="stSidebar"] button[key="new_chat_btn"] {
            background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.25)) !important;
            border: 1px solid rgba(99,102,241,0.40) !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            color: #c4b5fd !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 8px rgba(99,102,241,0.15) !important;
        }
        section[data-testid="stSidebar"] button[key="new_chat_btn"]:hover {
            background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(139,92,246,0.35)) !important;
            transform: translateX(0) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ================= PAGE MAP (no History) =================
    menu_map = {
        "🏠 Dashboard": "Dashboard",
        "💬 Chat": "Chat",
        "😊 Mood Analytics": "Mood Analytics",
        "📓 Journal": "Journal"
    }

    reverse_map = {v: k for k, v in menu_map.items()}
    current_label = reverse_map.get(current_page, "🏠 Dashboard")

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-header"><div class="sidebar-brain-avatar">🧠</div><span>MindCare AI</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            '<div class="section-title">Navigation</div>',
            unsafe_allow_html=True
        )

        menu = list(menu_map.keys())

        choice = st.radio(
            "",
            menu,
            index=menu.index(current_label),
            key="nav"
        )

        new_page = menu_map[choice]

        if st.session_state.get("current_page") != new_page:
            st.session_state["current_page"] = new_page
            # When switching away from Chat, clear any open dropdown
            if new_page != "Chat":
                st.session_state.pop("open_dropdown", None)
                st.session_state.pop("rename_active", None)
            st.rerun()

        # ================= SESSION TABS (ONLY ON CHAT PAGE) =================
        if st.session_state.get("current_page") == "Chat":
            st.markdown("---")
            st.markdown(
                '<div class="section-title">💬 Sessions</div>',
                unsafe_allow_html=True
            )

            # New Chat button - don't create conversation until user sends first message
            if st.button("＋  New Chat", key="new_chat_btn"):
                st.session_state["conversation_id"] = None
                st.session_state["chat_history"] = []
                st.session_state["last_loaded_chat"] = None
                st.session_state.pop("open_dropdown", None)
                st.session_state.pop("rename_active", None)
                st.rerun()

            conversations = get_conversations(user_id)

            if not conversations:
                st.caption("No sessions yet. Start chatting! 💬")
            else:
                # Init state
                if "open_dropdown" not in st.session_state:
                    st.session_state["open_dropdown"] = None
                if "rename_active" not in st.session_state:
                    st.session_state["rename_active"] = None
                if "deleted_sessions" not in st.session_state:
                    st.session_state["deleted_sessions"] = []
                if "custom_session_names" not in st.session_state:
                    st.session_state["custom_session_names"] = {}

                active_cid = str(st.session_state.get("conversation_id", ""))

                for i, convo in enumerate(conversations):
                    convo_id = str(convo[0])

                    # Skip deleted
                    if convo_id in st.session_state["deleted_sessions"]:
                        continue

                    # Determine title
                    if convo_id in st.session_state["custom_session_names"]:
                        title = st.session_state["custom_session_names"][convo_id]
                    else:
                        # Use DB title if not "New Chat", else derive from messages
                        db_title = convo[1] if len(convo) > 1 else "New Chat"
                        if db_title and db_title != "New Chat":
                            title = db_title[:18] + ("..." if len(db_title) > 18 else "")
                        else:
                            messages = get_messages_by_conversation(convo_id)
                            if messages:
                                first_user = next(
                                    (m[1] for m in messages if m[0] == "user"),
                                    "New Chat"
                                )
                                title = short_title(first_user, 18)
                            else:
                                title = "New Chat"

                    is_active = (convo_id == active_cid)
                    is_open = (st.session_state["open_dropdown"] == convo_id)
                    is_renaming = (st.session_state["rename_active"] == convo_id)

                    # ---- RENAME MODE ----
                    if is_renaming:
                        col_input, col_save, col_cancel = st.columns([5, 2, 2])
                        with col_input:
                            new_name = st.text_input(
                                "",
                                value=title,
                                key=f"rename_input_{convo_id}",
                                label_visibility="collapsed"
                            )
                        with col_save:
                            if st.button("✓", key=f"save_rename_{convo_id}"):
                                if new_name.strip():
                                    st.session_state["custom_session_names"][convo_id] = new_name.strip()
                                    rename_conversation(int(convo_id), new_name.strip())
                                st.session_state["rename_active"] = None
                                st.session_state["open_dropdown"] = None
                                st.rerun()
                        with col_cancel:
                            if st.button("✕", key=f"cancel_rename_{convo_id}"):
                                st.session_state["rename_active"] = None
                                st.session_state["open_dropdown"] = None
                                st.rerun()
                        continue

                    # ---- NORMAL SESSION ROW ----
                    active_class = "active-session" if is_active else ""

                    # Session label button (click to open)
                    col_label, col_dots = st.columns([8, 1])

                    with col_label:
                        label_display = f"{'▶ ' if is_active else '💬 '}{title}"
                        if st.button(
                            label_display,
                            key=f"sess_{convo_id}_{i}",
                            use_container_width=True
                        ):
                            st.session_state["conversation_id"] = int(convo_id)
                            st.session_state["chat_history"] = get_messages_by_conversation(convo_id)
                            st.session_state["last_loaded_chat"] = int(convo_id)
                            st.session_state["open_dropdown"] = None
                            st.session_state["rename_active"] = None
                            st.rerun()

                    with col_dots:
                        if st.button("⋮", key=f"dots_{convo_id}_{i}"):
                            if st.session_state["open_dropdown"] == convo_id:
                                st.session_state["open_dropdown"] = None
                            else:
                                st.session_state["open_dropdown"] = convo_id
                            st.rerun()

                    # ---- DROPDOWN (shown below the row) ----
                    if is_open:
                        col_space, col_menu = st.columns([1, 7])
                        with col_menu:
                            if st.button("✏️  Rename", key=f"rename_opt_{convo_id}"):
                                st.session_state["rename_active"] = convo_id
                                st.session_state["open_dropdown"] = None
                                st.rerun()
                            if st.button("🗑️  Delete", key=f"delete_opt_{convo_id}"):
                                st.session_state["deleted_sessions"].append(convo_id)
                                st.session_state["open_dropdown"] = None
                                # If deleted session was active, clear it
                                if active_cid == convo_id:
                                    st.session_state["conversation_id"] = None
                                    st.session_state["chat_history"] = []
                                    st.session_state["last_loaded_chat"] = None
                                st.rerun()

        # ================= LOGOUT BUTTON =================
        st.markdown("---")

        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)

        if st.button("🚪 Logout", key="logout_btn", type="primary"):
            st.session_state.clear()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
