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
            background-color: #ffffff;
            border-right: 1px solid #e6e6e6;
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
            font-weight: 800;
            margin-top: -8px;
            margin-left: -2px;
            margin-bottom: 14px;
            padding: 0;
            line-height: 1.1;
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

        /* Navigation title */
        .section-title {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.3px;
            margin: 10px 0 8px 2px;
            color: #4b5563;
        }

        /* Controlled divider spacing */
        hr {
            margin-top: 10px !important;
            margin-bottom: 10px !important;
        }

        /* Default button style (grey) for all sidebar buttons */
        section[data-testid="stSidebar"] .stButton button {
            background-color: #f0f2f6 !important;
            border-radius: 30px !important;
            padding: 8px 16px !important;
            margin: 4px 0 !important;
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

        /* Navigation radio spacing */
        div[role="radiogroup"] {
            gap: 0.2rem !important;
        }

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

        /* Add balanced spacing above logout */
        .logout-btn {
            margin-top: 30px !important;
            margin-bottom: -2px !important;
            padding-bottom: 0 !important;
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
            '<div class="sidebar-header">🧠 MindCare AI</div>',
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