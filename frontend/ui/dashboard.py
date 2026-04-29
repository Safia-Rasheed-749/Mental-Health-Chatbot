import streamlit as st
from datetime import datetime, timedelta
from db import get_messages_by_user, get_moods_by_user, get_journals_by_user

def show_dashboard():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, .stApp {
        font-family: 'Inter','Segoe UI',sans-serif !important;
        background: linear-gradient(135deg, #ece9f7 0%, #dff0f5 50%, #d9f0e8 100%) !important;
        min-height: 100vh !important;
    }

    header[data-testid="stHeader"] { background:transparent !important; box-shadow:none !important; border-bottom:none !important; }
    .stDeployButton { display:none !important; }
    #MainMenu       { visibility:hidden !important; }
    footer          { visibility:hidden !important; }

    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3rem !important;
        background: transparent !important;
        max-width: 1060px !important;
    }

    /* ── HERO ── */
    .dash-hero {
        background: linear-gradient(135deg, #4a7fd4 0%, #5fa8e0 55%, #7ecde8 100%);
        border-radius: 24px;
        padding: 28px 32px 24px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 28px rgba(74,127,212,0.30);
    }
    .dash-hero::before { content:''; position:absolute; top:-50px; right:-50px; width:180px; height:180px; background:rgba(255,255,255,0.10); border-radius:50%; }
    .dash-hero::after  { content:''; position:absolute; bottom:-35px; left:28%; width:130px; height:130px; background:rgba(255,255,255,0.07); border-radius:50%; }
    .hero-top      { display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:10px; }
    .hero-greeting { font-size:25px; font-weight:800; color:#ffffff; line-height:1.25; margin:0; }
    .hero-sub      { font-size:14px; color:rgba(255,255,255,0.88); margin-top:5px; }
    .hero-badge    { background:rgba(255,255,255,0.22); border:1px solid rgba(255,255,255,0.35); border-radius:50px; padding:6px 16px; font-size:12px; font-weight:600; color:#fff; white-space:nowrap; margin-top:2px; }
    .hero-divider  { height:1px; background:rgba(255,255,255,0.22); margin:16px 0 14px; }
    .hero-stats-row { display:flex; gap:28px; flex-wrap:wrap; align-items:center; }
    .hero-stat     { display:flex; flex-direction:column; }
    .hero-stat-val { font-size:24px; font-weight:800; color:#ffffff; line-height:1; }
    .hero-stat-lbl { font-size:11px; color:rgba(255,255,255,0.75); margin-top:3px; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; }
    .hero-stat-sep { width:1px; height:34px; background:rgba(255,255,255,0.28); }

    /* ── SECTION LABEL ── */
    .section-label { font-size:11px; font-weight:700; letter-spacing:1.1px; text-transform:uppercase; color:#9b8ec4; text-align:center; margin:0 0 14px; }

    /* ── SPACERS ── */
    .sp-md { height:22px; }
    .sp-lg { height:32px; }

    /* ── OVERVIEW STAT CARDS ── */
    .stat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
    .stat-card-pro {
        border-radius:18px; padding:20px 18px;
        border:1px solid rgba(255,255,255,0.80);
        box-shadow:0 4px 18px rgba(160,140,220,0.10);
        position:relative; overflow:hidden;
        backdrop-filter: blur(10px);
    }
    .sc-blue   { background: linear-gradient(145deg, rgba(220,230,255,0.80), rgba(255,255,255,0.60)); }
    .sc-teal   { background: linear-gradient(145deg, rgba(210,245,238,0.80), rgba(255,255,255,0.60)); }
    .sc-purple { background: linear-gradient(145deg, rgba(235,225,255,0.80), rgba(255,255,255,0.60)); }

    .sc-top-bar { height:4px; border-radius:18px 18px 0 0; position:absolute; top:0; left:0; right:0; }
    .sc-blue   .sc-top-bar { background:linear-gradient(90deg,#7b9ef0,#a5c0f5); }
    .sc-teal   .sc-top-bar { background:linear-gradient(90deg,#5ecfb8,#7de8c8); }
    .sc-purple .sc-top-bar { background:linear-gradient(90deg,#a78bfa,#c4b5fd); }

    .sc-icon-wrap { width:40px; height:40px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:18px; margin:8px 0 12px; background:rgba(255,255,255,0.70); }
    .sc-val    { font-size:28px; font-weight:800; color:#3b2f6e; line-height:1; }
    .sc-val-sm { font-size:17px; font-weight:700; color:#3b2f6e; line-height:1.3; }
    .sc-lbl    { font-size:12px; color:#8b7ec0; font-weight:500; margin-top:5px; }

    /* ── INSIGHT PANEL ── */
    .insight-panel {
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.75);
        border-radius:18px; padding:20px 24px;
        display:flex; align-items:center; gap:16px;
        box-shadow: 0 4px 18px rgba(160,140,220,0.10);
    }
    .insight-icon    { font-size:34px; flex-shrink:0; }
    .insight-text h4 { font-size:14px; font-weight:700; color:#3b2f6e; margin:0 0 4px; }
    .insight-text p  { font-size:13px; color:#6b5fa0; margin:0; line-height:1.6; }

    /* ── NAV CARDS ── */
    .nav-card {
        border-radius:20px;
        border: 1px solid rgba(255,255,255,0.80);
        box-shadow: 0 4px 18px rgba(160,140,220,0.10);
        padding: 22px 20px 18px;
        position: relative; overflow:hidden;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }
    .nc-chat    { background: linear-gradient(160deg, rgba(220,230,255,0.75) 0%, rgba(255,255,255,0.55) 60%); }
    .nc-mood    { background: linear-gradient(160deg, rgba(210,245,238,0.75) 0%, rgba(255,255,255,0.55) 60%); }
    .nc-history { background: linear-gradient(160deg, rgba(235,225,255,0.75) 0%, rgba(255,255,255,0.55) 60%); }
    .nc-journal { background: linear-gradient(160deg, rgba(255,237,213,0.75) 0%, rgba(255,255,255,0.55) 60%); }

    .nav-card-stripe { height:4px; border-radius:20px 20px 0 0; position:absolute; top:0; left:0; right:0; }
    .nc-chat    .nav-card-stripe { background:linear-gradient(90deg,#7b9ef0,#a5c0f5); }
    .nc-mood    .nav-card-stripe { background:linear-gradient(90deg,#5ecfb8,#7de8c8); }
    .nc-history .nav-card-stripe { background:linear-gradient(90deg,#a78bfa,#c4b5fd); }
    .nc-journal .nav-card-stripe { background:linear-gradient(90deg,#fb923c,#fbbf24); }

    .nav-card-icon { width:46px; height:46px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:21px; margin:4px 0 12px; background:rgba(255,255,255,0.70); }
    .nav-card-title { font-size:15px; font-weight:700; color:#3b2f6e; margin-bottom:5px; }
    .nav-card-desc  { font-size:13px; color:#6b7a99; line-height:1.55; }
    .nav-card-tag   { display:inline-block; margin-top:12px; padding:4px 11px; border-radius:50px; font-size:11px; font-weight:600; background:rgba(255,255,255,0.70); }
    .nc-chat    .nav-card-tag { color:#4a6fd4; }
    .nc-mood    .nav-card-tag { color:#0d9488; }
    .nc-history .nav-card-tag { color:#7c3aed; }
    .nc-journal .nav-card-tag { color:#ea580c; }

    /* ── NAV BUTTONS — colored by Streamlit's own key-based data-testid ── */
    /* Streamlit renders: <div data-testid="stButton"><button ...> */
    /* We target the button inside each column's stButton by order */

    /* All 4 nav buttons: shared base */
    [data-testid="stButton"]:has(button[data-testid="baseButton-secondary"]) button {
        border-radius: 12px !important;
        border: none !important;
        height: 42px !important;
        min-height: 42px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        cursor: pointer !important;
        width: 100% !important;
        transition: filter 0.18s, transform 0.18s !important;
    }

    /* Target by button text via attribute — Streamlit sets aria-label from button label */
    button[aria-label="Open AI Chat"],
    button[data-testid="Open AI Chat"] {
        background: linear-gradient(135deg, #7b9ef0, #a5c0f5) !important;
        box-shadow: 0 4px 14px rgba(123,158,240,0.40) !important;
    }
    button[aria-label="Open Mood Analytics"],
    button[data-testid="Open Mood Analytics"] {
        background: linear-gradient(135deg, #5ecfb8, #7de8c8) !important;
        box-shadow: 0 4px 14px rgba(94,207,184,0.40) !important;
    }
    button[aria-label="Open Chat History"],
    button[data-testid="Open Chat History"] {
        background: linear-gradient(135deg, #a78bfa, #c4b5fd) !important;
        box-shadow: 0 4px 14px rgba(167,139,250,0.40) !important;
    }
    button[aria-label="Open Journal"],
    button[data-testid="Open Journal"] {
        background: linear-gradient(135deg, #fb923c, #fbbf24) !important;
        box-shadow: 0 4px 14px rgba(251,146,60,0.40) !important;
    }

    button[aria-label="Open AI Chat"]:hover,
    button[aria-label="Open Mood Analytics"]:hover,
    button[aria-label="Open Chat History"]:hover,
    button[aria-label="Open Journal"]:hover {
        filter: brightness(1.08) !important;
        transform: translateY(-2px) !important;
    }

    /* ── FOOTER ── */
    .dash-footer { text-align:center; color:#9b8ec4; font-size:13px; padding:26px 0 8px; border-top:1px solid rgba(160,140,220,0.20); margin-top:10px; }

    /* ── SIDEBAR — untouched ── */
    section[data-testid="stSidebar"] .stButton > button {
        display:block !important; width:100% !important; background:transparent !important;
        border:none !important; border-radius:30px !important; padding:8px 16px !important;
        margin:4px 0 !important; font-size:14px !important; font-weight:500 !important;
        text-align:left !important; color:#F8FAFC !important; min-height:auto !important;
        box-shadow:none !important; cursor:pointer !important; height:auto !important;
        transition:background-color 0.2s !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color:rgba(59,130,246,0.15) !important; transform:translateX(4px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── DATA ──
    user_id  = st.session_state.user[0]
    username = st.session_state.user[1] if len(st.session_state.user) > 1 else "Friend"

    all_messages = get_messages_by_user(user_id)
    today_dt     = datetime.now()
    yesterday    = today_dt - timedelta(days=1)
    chats_today  = sum(1 for m in all_messages if len(m) > 2 and m[2] and m[2] > yesterday)
    total_chats  = len([m for m in all_messages if m[0] == "user"])

    moods = get_moods_by_user(user_id)
    mood_emoji_map = {"Happy":"😊","Neutral":"😐","Sad":"😔","Anxious":"😰","Angry":"😡"}
    if moods:
        last_mood_disp = f"{mood_emoji_map.get(moods[-1][0],'😊')} {moods[-1][0]}"
        mood_streak    = len(moods)
    else:
        last_mood_disp = "Not logged yet"
        mood_streak    = 0

    journal_count = len(get_journals_by_user(user_id))

    hour = today_dt.hour
    if hour < 12:   greeting, icon, note = "Good Morning",   "🌅", "Start your day with a moment of mindfulness."
    elif hour < 17: greeting, icon, note = "Good Afternoon", "☀️", "You're doing great — keep going."
    else:           greeting, icon, note = "Good Evening",   "🌙", "Wind down and reflect on your day."

    # ── HERO ──
    st.markdown(f"""
    <div class="dash-hero">
        <div class="hero-top">
            <div>
                <div class="hero-greeting">{icon} {greeting}, {username}!</div>
                <div class="hero-sub">{note}</div>
            </div>
            <div class="hero-badge">📅 {today_dt.strftime("%A, %B %d")}</div>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-stats-row">
            <div class="hero-stat"><div class="hero-stat-val">{chats_today}</div><div class="hero-stat-lbl">Chats Today</div></div>
            <div class="hero-stat-sep"></div>
            <div class="hero-stat"><div class="hero-stat-val">{total_chats}</div><div class="hero-stat-lbl">Total Messages</div></div>
            <div class="hero-stat-sep"></div>
            <div class="hero-stat"><div class="hero-stat-val">{mood_streak}</div><div class="hero-stat-lbl">Mood Logs</div></div>
            <div class="hero-stat-sep"></div>
            <div class="hero-stat"><div class="hero-stat-val">{journal_count}</div><div class="hero-stat-lbl">Journal Entries</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── OVERVIEW ──
    st.markdown('<div class="sp-md"></div><p class="section-label">Overview</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card-pro sc-blue">
            <div class="sc-top-bar"></div><div class="sc-icon-wrap">💬</div>
            <div class="sc-val">{chats_today}</div><div class="sc-lbl">Chats Today</div>
        </div>
        <div class="stat-card-pro sc-teal">
            <div class="sc-top-bar"></div><div class="sc-icon-wrap">🎭</div>
            <div class="sc-val-sm">{last_mood_disp}</div><div class="sc-lbl">Last Mood Logged</div>
        </div>
        <div class="stat-card-pro sc-purple">
            <div class="sc-top-bar"></div><div class="sc-icon-wrap">📓</div>
            <div class="sc-val">{journal_count}</div><div class="sc-lbl">Journal Entries</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INSIGHT ──
    insight_msg = (
        f"You've logged <b>{mood_streak} mood entries</b> so far — keep tracking to reveal your emotional patterns."
        if mood_streak > 0 else
        "Start logging your mood daily to unlock personalized wellness insights."
    )
    st.markdown(f"""
    <div class="sp-lg"></div>
    <div class="insight-panel">
        <div class="insight-icon">🌿</div>
        <div class="insight-text">
            <h4>Wellness Insight</h4>
            <p>{insight_msg} Your mental wellness journey is unique — every entry matters. 💙</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── QUICK NAVIGATION ──
    st.markdown('<div class="sp-lg"></div><p class="section-label">Quick Navigation</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""<div class="nav-card nc-chat"><div class="nav-card-stripe"></div>
            <div class="nav-card-icon">💬</div><div class="nav-card-title">AI Chat</div>
            <div class="nav-card-desc">Talk with your AI companion anytime, day or night.</div>
            <span class="nav-card-tag">Start Chatting →</span></div>""", unsafe_allow_html=True)
        if st.button("Open AI Chat", key="chat_btn", use_container_width=True):
            st.session_state.current_page = "Chat"; st.query_params["page"] = "Chat"; st.rerun()

    with col2:
        st.markdown("""<div class="nav-card nc-mood"><div class="nav-card-stripe"></div>
            <div class="nav-card-icon">📊</div><div class="nav-card-title">Mood Analytics</div>
            <div class="nav-card-desc">Log your mood and visualize emotional trends over time.</div>
            <span class="nav-card-tag">Track Mood →</span></div>""", unsafe_allow_html=True)
        if st.button("Open Mood Analytics", key="mood_btn", use_container_width=True):
            st.session_state.current_page = "Mood Analytics"; st.query_params["page"] = "Mood Analytics"; st.rerun()

    st.markdown('<div class="sp-md"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="medium")
    with col3:
        st.markdown("""<div class="nav-card nc-history"><div class="nav-card-stripe"></div>
            <div class="nav-card-icon">🕒</div><div class="nav-card-title">Chat History</div>
            <div class="nav-card-desc">Review past conversations, search and export sessions.</div>
            <span class="nav-card-tag">View History →</span></div>""", unsafe_allow_html=True)
        if st.button("Open Chat History", key="history_btn", use_container_width=True):
            st.session_state.current_page = "History"; st.query_params["page"] = "History"; st.rerun()

    with col4:
        st.markdown("""<div class="nav-card nc-journal"><div class="nav-card-stripe"></div>
            <div class="nav-card-icon">📖</div><div class="nav-card-title">Journal</div>
            <div class="nav-card-desc">Write private reflections and build your personal diary.</div>
            <span class="nav-card-tag">Write Entry →</span></div>""", unsafe_allow_html=True)
        if st.button("Open Journal", key="journal_btn", use_container_width=True):
            st.session_state.current_page = "Journal"; st.query_params["page"] = "Journal"; st.rerun()

    st.markdown('<div class="dash-footer">🌿 MindCare AI &nbsp;·&nbsp; Take care of your mental wellness — one day at a time.</div>', unsafe_allow_html=True)
