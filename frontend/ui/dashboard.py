import streamlit as st
from datetime import datetime, timedelta
from db import get_messages_by_user, get_moods_by_user, get_journals_by_user

def show_dashboard():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, .stApp { font-family:'Inter','Segoe UI',sans-serif !important; background:#f0f4fb !important; }

    header[data-testid="stHeader"] { background:transparent !important; box-shadow:none !important; border-bottom:none !important; }
    .stDeployButton { display:none !important; }
    #MainMenu       { visibility:hidden !important; }
    footer          { visibility:hidden !important; }

    .block-container { padding-top:1.4rem !important; padding-bottom:3rem !important; background:#f0f4fb !important; max-width:1080px !important; }

    /* HERO */
    .dash-hero {
        background:linear-gradient(135deg,#4a7fd4 0%,#5fa8e0 55%,#7ecde8 100%);
        border-radius:20px; padding:28px 32px 26px; margin-bottom:32px;
        position:relative; overflow:hidden; box-shadow:0 8px 28px rgba(74,127,212,0.25);
    }
    .dash-hero::before { content:''; position:absolute; top:-50px; right:-50px; width:180px; height:180px; background:rgba(255,255,255,0.10); border-radius:50%; }
    .dash-hero::after  { content:''; position:absolute; bottom:-35px; left:28%; width:130px; height:130px; background:rgba(255,255,255,0.07); border-radius:50%; }
    .hero-top        { display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:10px; }
    .hero-greeting   { font-size:26px; font-weight:800; color:#fff; line-height:1.25; margin:0; }
    .hero-sub        { font-size:14px; color:rgba(255,255,255,0.88); margin-top:5px; }
    .hero-badge      { background:rgba(255,255,255,0.22); border:1px solid rgba(255,255,255,0.35); border-radius:50px; padding:6px 16px; font-size:12px; font-weight:600; color:#fff; white-space:nowrap; margin-top:2px; }
    .hero-divider    { height:1px; background:rgba(255,255,255,0.22); margin:18px 0 16px; }
    .hero-stats-row  { display:flex; gap:24px; flex-wrap:wrap; align-items:center; }
    .hero-stat       { display:flex; flex-direction:column; }
    .hero-stat-val   { font-size:24px; font-weight:800; color:#fff; line-height:1; }
    .hero-stat-lbl   { font-size:11px; color:rgba(255,255,255,0.75); margin-top:3px; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; }
    .hero-stat-sep   { width:1px; height:36px; background:rgba(255,255,255,0.28); }

    /* SECTION LABEL */
    .section-label { font-size:11px; font-weight:700; letter-spacing:1.1px; text-transform:uppercase; color:#7c8db5; text-align:center; margin:0 0 16px; padding-top:4px; }

    /* SPACERS */
    .sp-md { height:24px; }
    .sp-lg { height:36px; }

    /* OVERVIEW STAT CARDS */
    .stat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
    .stat-card-pro { background:#fff; border-radius:16px; padding:20px 18px; border:1px solid #e4eaf4; box-shadow:0 2px 12px rgba(0,0,0,0.04); position:relative; overflow:hidden; }
    .sc-top-bar    { height:4px; border-radius:16px 16px 0 0; position:absolute; top:0; left:0; right:0; }
    .sc-blue   .sc-top-bar { background:linear-gradient(90deg,#4a7fd4,#5fa8e0); }
    .sc-teal   .sc-top-bar { background:linear-gradient(90deg,#0ea5a0,#34d399); }
    .sc-purple .sc-top-bar { background:linear-gradient(90deg,#8b5cf6,#c084fc); }
    .sc-icon-wrap  { width:42px; height:42px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:19px; margin:8px 0 12px; }
    .sc-blue   .sc-icon-wrap { background:#eef3ff; }
    .sc-teal   .sc-icon-wrap { background:#e6faf8; }
    .sc-purple .sc-icon-wrap { background:#f3eeff; }
    .sc-val    { font-size:30px; font-weight:800; color:#1e2d4e; line-height:1; }
    .sc-val-sm { font-size:18px; font-weight:700; color:#1e2d4e; line-height:1.3; }
    .sc-lbl    { font-size:12px; color:#7c8db5; font-weight:500; margin-top:5px; }

    /* INSIGHT PANEL */
    .insight-panel { background:linear-gradient(135deg,#eaf3fd,#f0f6ff); border:1px solid #c8dff5; border-radius:16px; padding:22px 26px; display:flex; align-items:center; gap:18px; }
    .insight-icon  { font-size:36px; flex-shrink:0; }
    .insight-text h4 { font-size:15px; font-weight:700; color:#1e3a6e; margin:0 0 5px; }
    .insight-text p  { font-size:13px; color:#3d5a8a; margin:0; line-height:1.6; }

    /* NAV CARDS */
    .nav-card        { background:#fff; border-radius:18px; border:1.5px solid #e4eaf4; box-shadow:0 2px 14px rgba(0,0,0,0.05); padding:24px 22px 20px; position:relative; overflow:hidden; margin-bottom:10px; }
    .nav-card-stripe { height:4px; border-radius:18px 18px 0 0; position:absolute; top:0; left:0; right:0; }
    .nc-chat    .nav-card-stripe { background:linear-gradient(90deg,#4a7fd4,#5fa8e0); }
    .nc-mood    .nav-card-stripe { background:linear-gradient(90deg,#0ea5a0,#34d399); }
    .nc-journal .nav-card-stripe { background:linear-gradient(90deg,#f97316,#fbbf24); }
    .nc-chat    { background:linear-gradient(180deg,#f0f5ff 0%,#fff 55%); }
    .nc-mood    { background:linear-gradient(180deg,#f0fdfb 0%,#fff 55%); }
    .nc-journal { background:linear-gradient(180deg,#fff7f0 0%,#fff 55%); }
    .nav-card-icon  { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:22px; margin:6px 0 14px; }
    .nc-chat    .nav-card-icon { background:#dbeafe; }
    .nc-mood    .nav-card-icon { background:#ccfbf1; }
    .nc-journal .nav-card-icon { background:#ffedd5; }
    .nav-card-title { font-size:16px; font-weight:700; color:#1e2d4e; margin-bottom:6px; }
    .nav-card-desc  { font-size:13px; color:#64748b; line-height:1.55; }
    .nav-card-tag   { display:inline-block; margin-top:14px; padding:4px 12px; border-radius:50px; font-size:11px; font-weight:600; }
    .nc-chat    .nav-card-tag { background:#dbeafe; color:#2563eb; }
    .nc-mood    .nav-card-tag { background:#ccfbf1; color:#0d9488; }
    .nc-journal .nav-card-tag { background:#ffedd5; color:#ea580c; }

    /* FOOTER */
    .dash-footer { text-align:center; color:#a0aec0; font-size:13px; padding:28px 0 10px; border-top:1px solid #e4eaf4; margin-top:12px; }

    /* Sidebar styling is handled exclusively in sidebar.py */
    </style>

    <script>
    (function() {
        const colors = {
            'Open AI Chat':        { bg:'linear-gradient(135deg,#4a7fd4,#5fa8e0)', shadow:'0 4px 14px rgba(74,127,212,0.40)' },
            'Open Mood Analytics': { bg:'linear-gradient(135deg,#0ea5a0,#34d399)', shadow:'0 4px 14px rgba(14,165,160,0.40)' },
            'Open Journal':        { bg:'linear-gradient(135deg,#f97316,#fbbf24)', shadow:'0 4px 14px rgba(249,115,22,0.40)' },
            'Open Games':          { bg:'linear-gradient(135deg,#8b5cf6,#c084fc)', shadow:'0 4px 14px rgba(139,92,246,0.40)' },
        };
        function paint() {
            window.parent.document.querySelectorAll('button').forEach(btn => {
                const c = colors[btn.innerText.trim()];
                if (!c) return;
                btn.style.setProperty('background', c.bg, 'important');
                btn.style.setProperty('color', '#fff', 'important');
                btn.style.setProperty('box-shadow', c.shadow, 'important');
                btn.style.setProperty('border', 'none', 'important');
                btn.style.setProperty('border-radius', '12px', 'important');
                btn.style.setProperty('font-weight', '700', 'important');
                btn.style.setProperty('height', '44px', 'important');
                btn.onmouseenter = () => btn.style.setProperty('filter','brightness(1.08)','important');
                btn.onmouseleave = () => btn.style.removeProperty('filter');
            });
        }
        setTimeout(paint, 100);
        setTimeout(paint, 600);
        new MutationObserver(paint).observe(window.parent.document.body, { childList:true, subtree:true });
    })();
    </script>
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
        st.markdown("""<div class="nav-card nc-journal"><div class="nav-card-stripe"></div>
            <div class="nav-card-icon">📖</div><div class="nav-card-title">Journal</div>
            <div class="nav-card-desc">Write private reflections and build your personal diary.</div>
            <span class="nav-card-tag">Write Entry →</span></div>""", unsafe_allow_html=True)
        if st.button("Open Journal", key="journal_btn", use_container_width=True):
            st.session_state.current_page = "Journal"; st.query_params["page"] = "Journal"; st.rerun()

    with col4:
        st.markdown("""<div class="nav-card nc-chat" style="background:linear-gradient(180deg,#f5f0ff 0%,#fff 55%)"><div class="nav-card-stripe" style="background:linear-gradient(90deg,#8b5cf6,#c084fc)"></div>
            <div class="nav-card-icon" style="background:#ede9fe">🎮</div><div class="nav-card-title">Games</div>
            <div class="nav-card-desc">Play mindfulness games to relax and sharpen your focus.</div>
            <span class="nav-card-tag" style="background:#ede9fe;color:#7c3aed">Play Now →</span></div>""", unsafe_allow_html=True)
        if st.button("Open Games", key="games_btn", use_container_width=True):
            st.session_state.current_page = "Games"; st.query_params["page"] = "Games"; st.rerun()

    st.markdown('<div class="dash-footer">🌿 MindCare AI &nbsp;·&nbsp; Take care of your mental wellness — one day at a time.</div>', unsafe_allow_html=True)
