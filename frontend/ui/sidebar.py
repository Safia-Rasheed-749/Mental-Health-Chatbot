import streamlit as st
from db import get_conversations, get_messages_by_conversation

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

    # Fallback: use only first 2 words if no keyword matched
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

        /* Move entire sidebar content upward */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
        }

        /* Sidebar container spacing */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.2rem !important;
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
            padding-bottom: 0.7rem !important;
        }

        /* Top title/logo */
        .sidebar-header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 10px;
            font-size: 26px;
            font-weight: 900;
            margin-top: -8px;
            margin-left: -2px;
            margin-bottom: 14px;
            padding: 0;
            line-height: 1.1;
            color: rgba(196,181,253,0.98);
            text-shadow: 0 0 18px rgba(124,58,237,0.25);
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

        /* Navigation title */
        .section-title {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.3px;
            margin: 10px 0 8px 2px;
            color: rgba(226,232,240,0.78);
        }

        /* Controlled divider spacing */
        hr {
            margin-top: 10px !important;
            margin-bottom: 10px !important;
        }

        /* Default button style (grey) for all sidebar buttons */
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

        /* Navigation radio spacing */
        div[role="radiogroup"] {
            gap: 0.2rem !important;
        }

        /* Force primary button (logout) to dark blue */
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

        /* Best-effort "active" styling for radio-like buttons */
        section[data-testid="stSidebar"] .stButton button[aria-checked="true"],
        section[data-testid="stSidebar"] .stButton button[data-state="checked"] {
            background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(124,58,237,0.28)) !important;
            border: 1px solid rgba(124,58,237,0.55) !important;
            color: #ffffff !important;
            box-shadow: 0 18px 60px rgba(124,58,237,0.18);
        }

        /* Add balanced spacing above logout */
        .logout-btn {
            margin-top: 30px !important;
            margin-bottom: -2px !important;
            padding-bottom: 0 !important;
            
        }
        /* 1. Make navigation radio labels pure white (target the actual text) */
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #FFFFFF !important;
}

/* 2. Remove bubble from session buttons (background, border, radius) AND make text white */
section[data-testid="stSidebar"] .stButton button:not([kind="primary"]) {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}

/* 3. Keep a subtle hover effect (optional, does not affect spacing) */
section[data-testid="stSidebar"] .stButton button:not([kind="primary"]):hover {
    background-color: rgba(59,130,246,0.15) !important;
    transform: translateX(4px);
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
        st.markdown(
            '<div class="sidebar-header">🧠 <span>MindCare AI</span></div>',
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
            st.rerun()

        st.markdown("---")

        # ================= RECENT SESSIONS (ONLY ON HISTORY, STAY ON HISTORY PAGE) =================
        if st.session_state["current_page"] == "History":
            st.markdown(
                '<div class="section-title">📌 Recent Sessions</div>',
                unsafe_allow_html=True
            )

<<<<<<< HEAD
            # New Chat button - don't create conversation until user sends first message
            if st.button("＋  New Chat", key="new_chat_btn"):
                st.session_state["conversation_id"] = None
                st.session_state["chat_history"] = []
                st.session_state["last_loaded_chat"] = None
                st.session_state.pop("open_dropdown", None)
                st.session_state.pop("rename_active", None)
                st.rerun()

=======
>>>>>>> eba4ac8 (update)
            conversations = get_conversations(user_id)

            if not conversations:
                st.caption("No chats yet. Start a conversation in Chat 💬")
            else:
                for i, convo in enumerate(conversations):
                    convo_id = str(convo[0])

                    messages = get_messages_by_conversation(convo_id)

                    if not messages:
                        continue

                    title = next(
                        (m[1] for m in messages if m[0] == "user"),
                        "New Chat"
                    )

                    # SHORT GENERIC SESSION TITLE
                    title = short_title(title, 18)

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