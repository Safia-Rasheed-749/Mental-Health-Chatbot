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
    /* sidebar background color change*/
    /* ── SIDEBAR CONTAINER ── */
    section[data-testid="stSidebar"] {
        width: 260px !important;
        background: linear-gradient(180deg, #EEF2FF 0%, #E8EDFF 50%, #EDE9FF 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.15) !important;
        box-shadow: 2px 0 16px rgba(99,102,241,0.08) !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.6rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-bottom: 0.7rem !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }

    section[data-testid="stSidebar"] {
        position: relative !important;
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
        background: linear-gradient(135deg, #e9d5ff 0%, #ddd6fe 100%);
        border: 2px solid rgba(99,102,241,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.12);
        animation: avatarPulse 3s ease-in-out infinite;
    }
    @keyframes avatarPulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(99,102,241,0.12); }
        50%       { box-shadow: 0 0 0 8px rgba(99,102,241,0.06); }
    }
    .sidebar-brand {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .sidebar-brand-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
        letter-spacing: -0.5px;
    }
    .sidebar-brand-title .ai-part {
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-brand-tagline {
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

    /* ── DIVIDER ── */
    hr {
        margin-top: 6px !important;
        margin-bottom: 6px !important;
        border-color: rgba(74,127,212,0.2) !important;
    }
    /*navigation label color change*/
    /* ── SECTION LABEL ── */
    section[data-testid="stSidebar"] .sb-section-label {
        font-size: 13px !important;
        font-weight: 800 !important;
        letter-spacing: 1.6px !important;
        text-transform: uppercase !important;
        margin: 16px 0 10px 2px !important;
        color: black!important;
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
        background: rgba(99,102,241,0.1) !important;
    }
    
    /* text color in sidebar changes*/
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: black !important;
        font-size: 16.5px !important;
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
        color: #3730a3 !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        height: auto !important;
        min-height: auto !important;
        max-width: none !important;
        display: block !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(99,102,241,0.1) !important;
        color: #312e81 !important;
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
        border-color: rgba(99,102,241,0.2) !important;
        background: none !important;
        height: auto !important;
    }
    /*logout button color changes*/
    /* ── LOGOUT (primary) - Cool Red Color ── */
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        text-align: center !important;
        margin-top: 4px !important;
        box-shadow: 0 3px 12px rgba(239,68,68,0.25) !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%) !important;
        box-shadow: 0 4px 16px rgba(239,68,68,0.35) !important;
        transform: translateY(-1px) !important;
    }
    .logout-btn { 
        margin-top: 36px !important; 
        padding-top: 16px !important; 
        border-top: 1px solid rgba(99,102,241,0.2) !important; 
    }

    /* ── NEW CHAT BUTTON - Ultra Specific Selector with !important ── */
    section[data-testid="stSidebar"] div.new-chat-btn {
        margin-top: 16px !important;
        margin-bottom: 12px !important;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] div.new-chat-btn div[data-testid="stButton"] {
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] div.new-chat-btn div[data-testid="stButton"] button {
        background: linear-gradient(135deg, rgba(99,102,241,0.18) 0%, rgba(139,92,246,0.18) 100%) !important;
        border: 1.5px solid rgba(99,102,241,0.4) !important;
        border-radius: 10px !important;
        color: #4f46e5 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        box-shadow: 0 3px 10px rgba(99,102,241,0.15) !important;
        transition: all 0.2s ease !important;
        text-align: center !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] div.new-chat-btn div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, rgba(99,102,241,0.25) 0%, rgba(139,92,246,0.25) 100%) !important;
        border-color: rgba(99,102,241,0.6) !important;
        box-shadow: 0 5px 16px rgba(99,102,241,0.25) !important;
        transform: translateY(-2px) !important;
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
        background: rgba(99,102,241,0.12) !important;
        border-left: 2px solid #6366f1 !important;
        padding-left: 2px !important;
    }
    /*session tabs and label color*/
    /* FORCE SESSION BUTTON TEXT COLOR (ALL STATES) */
      section[data-testid="stSidebar"] div[data-testid="stButton"] button,
      section[data-testid="stSidebar"] div[data-testid="stButton"] button p {
    color: #111827 !important;
    opacity: 1 !important;
}

/* ACTIVE SESSION */
      section[data-testid="stSidebar"] .session-active div[data-testid="stButton"] button,
      section[data-testid="stSidebar"] .session-active div[data-testid="stButton"] button p {
      color: #4f46e5 !important;
      font-weight: 700 !important;
}
    }
    .session-active .session-title-btn .stButton button {
        color: #4f46e5 !important;
        font-weight: 500 !important;
    }
    .session-menu-btn .stButton button {
        color: rgba(99,102,241,0.5) !important;
        font-size: 14px !important;
        padding: 3px 6px !important;
        border-radius: 5px !important;
        width: auto !important;
        min-width: 26px !important;
    }
    .session-menu-btn .stButton button:hover {
        color: #4f46e5 !important;
        background: rgba(99,102,241,0.1) !important;
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
            <div class="sidebar-brand">
                <span class="sidebar-brand-title">MindCare<span class="ai-part">AI</span></span>
                <span class="sidebar-brand-tagline">Mental Wellness</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="sb-section-label">Navigation</div>', unsafe_allow_html=True)

        menu = list(menu_map.keys())
        choice = st.radio("", menu, index=menu.index(current_label), key="nav")
        new_page = menu_map[choice]

        if st.session_state.get("current_page") != new_page:
            st.session_state["current_page"] = new_page
            # Clear game nav trigger so next visit to Games resets to home
            if new_page != "Games":
                st.session_state["_games_nav_trigger"] = None
            for k in list(st.session_state.keys()):
                if k.startswith("rename_") or k.startswith("menu_open_"):
                    del st.session_state[k]
            st.rerun()

        # ═══════════════════════════════════════════════════════════
        # NEW CHAT BUTTON - SIDEBAR (CHAT PAGE ONLY)
        # ═══════════════════════════════════════════════════════════
        # LOCATION: Sidebar mein "NAVIGATION" ke neeche
        # STYLING: Simple, transparent background with border
        # 
        # CUSTOMIZATION GUIDE:
        # 1. SPACING ABOVE: height: 32px (line 355) - YAHAN SE SPACE CHANGE KARO
        # 2. BUTTON WIDTH: columns([1.5, 1]) - First number ko change karo
        #    - [1.5, 1] = 60% width (current)
        #    - [2, 1] = 67% width (wider)
        #    - [1, 1] = 50% width (narrower)
        # 3. BUTTON STYLING: CSS section mein (line 368)
        #    - font-size: 14px = Button text size
        #    - padding: 10px 14px = Button ke andar space
        #    - border-radius: 8px = Corner roundness
        # ═══════════════════════════════════════════════════════════
        
        # ── SESSION TABS — only on Chat page ──
        if st.session_state.get("current_page") == "Chat":
            st.markdown("---")

            # SPACING ABOVE BUTTON - Change height value to adjust space
            st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)
            
            # BUTTON WIDTH & POSITION - Change column ratio to adjust width
            # [1.5, 1] means button takes 60% width, left-aligned
            col1, col2 = st.columns([1.5, 1])
            with col1:
                if st.button("✏️  New Chat", key="new_chat_btn", use_container_width=True):
                    st.session_state["conversation_id"] = None
                    st.session_state["chat_history"] = []
                    st.session_state["last_loaded_chat"] = None
                    for k in list(st.session_state.keys()):
                        if k.startswith("rename_") or k.startswith("menu_open_"):
                            del st.session_state[k]
                    st.rerun()
            
            # ═══════════════════════════════════════════════════════════
            # BUTTON STYLING - CSS
            # ═══════════════════════════════════════════════════════════
            # DESIGN: Transparent background with subtle border
            # HOVER: Light background + slide right animation
            # 
            # CUSTOMIZATION:
            # - background: transparent = No background color
            # - border: 1px solid rgba(99,102,241,0.3) = Purple border
            # - color: #4f46e5 = Text color (purple)
            # - font-size: 14px = YAHAN SE TEXT SIZE CHANGE KARO
            # - padding: 10px 14px = Button ke andar space
            # ═══════════════════════════════════════════════════════════
            st.markdown("""
            <style>
            /* New Chat Button - Simple, left-aligned, narrower */
            section[data-testid="stSidebar"] button[key="new_chat_btn"] {
                background: transparent !important;
                border: 1px solid rgba(99,102,241,0.3) !important;
                border-radius: 8px !important;
                color: #4f46e5 !important;
                font-size: 14px !important;  /* TEXT SIZE - YAHAN SE CHANGE KARO */
                font-weight: 600 !important;
                padding: 10px 14px !important;  /* BUTTON PADDING - YAHAN SE CHANGE KARO */
                transition: all 0.2s ease !important;
                text-align: left !important;
            }
            section[data-testid="stSidebar"] button[key="new_chat_btn"]:hover {
                background: rgba(99,102,241,0.08) !important;  /* Hover background */
                border-color: rgba(99,102,241,0.5) !important;  /* Hover border */
                transform: translateX(2px) !important;  /* Slide right on hover */
            }
            </style>
            """, unsafe_allow_html=True)

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
