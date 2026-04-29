import streamlit as st
from datetime import datetime, timedelta
from db import get_messages_by_user, get_moods_by_user, get_journals_by_user

def show_dashboard():
    # ---------- Force scroll to top & remove top padding ----------
    st.markdown("""
        <script>
            // Scroll main content to top instantly
            window.parent.document.querySelector('.main').scrollTo({ top: 0, behavior: 'instant' });
        </script>
    """, unsafe_allow_html=True)

    # ---------- CSS for background, stat cards, banner, etc. ----------
    st.markdown("""
    <style>
        /* REMOVE ALL TOP SPACE - GUARANTEED */
            header, .stHeader, [data-testid="stHeader"] {
                display: none !important;
                height: 0px !important;
            }
            
            .block-container {
                padding-top: 0rem !important;
                margin-top: -0.5rem !important;
                background-color: #f5f9ff !important;
            }
            
            .stMarkdown:first-of-type {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            footer, #MainMenu, .stDeployButton {
                display: none !important;
            }
        /* Soft background */
        .stApp { background-color: #f5f9ff !important; }

        /* Title styling */
        .hero-title { text-align: center; margin: 0; padding: 0; }
        .hero-title span:first-child { font-size: 48px; }
        .hero-title span:last-child {
            font-size: 40px; font-weight: 900;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            background-clip: text; -webkit-background-clip: text; color: transparent;
        }
        .hero-subtitle { text-align: center; font-size: 18px; color: #2c3e66; margin-bottom: 20px; }

        /*  banner */
        .welcome-section {
            background: #4A6FA5;
            border-radius: 28px; padding: 20px 28px; margin: 10px 0 30px 0;
            text-align: center; box-shadow: 0 12px 24px -8px rgba(74, 111, 165, 0.4);
        }
        .welcome-greeting { font-size: 28px; font-weight: 800; color: white; }
        .welcome-note { font-size: 16px; color: white; font-weight: 600; }

        /* Stat cards (white, with slight top margin) */
        .stat-card {
            background: white; border-radius: 28px; padding: 1.2rem 0.8rem;
            text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.04);
            height: 130px; display: flex; flex-direction: column; justify-content: center;
            border: 1px solid #e2e8f0; transition: all 0.2s;
            margin-top: 10px;
        }
        .stat-card:hover { transform: translateY(-4px); box-shadow: 0 20px 30px -12px rgba(0,0,0,0.1); }
        .stat-num { font-size: 36px; font-weight: 800; color: #1e40af; }
        .stat-num-sm { font-size: 26px; font-weight: 800; color: #1e40af; }
        .stat-label { color: #475569; font-size: 15px; font-weight: 600; margin-top: 6px; }
        
        .nav-title {
            text-align: center; font-size: 28px; font-weight: 800;
            color: #0f172a; margin: 48px 0 28px 0;
        }

        /* Base button styling (size, shadow, etc.) */
        .main .stButton button {
            width: 100% !important;
            min-height: 220px !important;
            border-radius: 32px !important;
            border: none !important;
            background: white !important;
            box-shadow: 0 20px 30px -12px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
            padding: 2rem 1rem !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            gap: 10px !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            white-space: normal !important;
            cursor: pointer !important;
        }
        .main .stButton button:hover {
            transform: translateY(-8px) !important;
            box-shadow: 0 30px 40px -12px rgba(0,0,0,0.2) !important;
        }
        .stButton > button {
            background: #4A6FA5;
            color: white;}
        .stButton > button:hover {
            background: #1E3A5F;
            color: white;}

        /* Color classes that will be added by JavaScript */
        .dash-card-chat {
            background: linear-gradient(145deg, #ffffff, #e0f2fe) !important;
            border-bottom: 5px solid #3b82f6 !important;
        }
        .dash-card-mood {
            background: linear-gradient(145deg, #ffffff, #ccfbf1) !important;
            border-bottom: 5px solid #14b8a6 !important;
        }
        .dash-card-history {
            background: linear-gradient(145deg, #ffffff, #fce7f3) !important;
            border-bottom: 5px solid #ec4899 !important;
        }
        .dash-card-journal {
            background: linear-gradient(145deg, #ffffff, #f3e8ff) !important;
            border-bottom: 5px solid #a855f7 !important;
        }

        /* Sidebar reset */
        section[data-testid="stSidebar"] .stButton button {
            display: block !important;
            width: 100% !important;
            background-color: #f0f2f6 !important;
            border-radius: 30px !important;
            padding: 8px 16px !important;
            margin: 6px 0 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: left !important;
            color: #1e2a3a !important;
            gap: 8px !important;
            min-height: auto !important;
            box-shadow: none !important;
            cursor: pointer !important;
            transition: background-color 0.2s !important;
        }
        .dashboard-footer { text-align: center; color: #6c86a3; padding: 56px 0 24px; font-size: 14px; }
    </style>

    <!-- JavaScript to add color classes based on button text -->
    <script>
        function styleDashboardButtons() {
            const buttons = document.querySelectorAll('.main .stButton button');
            buttons.forEach(btn => {
                // Remove any existing dash-card classes
                btn.classList.remove('dash-card-chat', 'dash-card-mood', 'dash-card-history', 'dash-card-journal');
                const text = btn.innerText.toLowerCase();
                if (text.includes('ai chat') || (text.includes('chat') && !text.includes('history'))) {
                    btn.classList.add('dash-card-chat');
                } else if (text.includes('mood')) {
                    btn.classList.add('dash-card-mood');
                } else if (text.includes('history')) {
                    btn.classList.add('dash-card-history');
                } else if (text.includes('journal')) {
                    btn.classList.add('dash-card-journal');
                }
            });
        }
        // Run after DOM is ready
        setTimeout(styleDashboardButtons, 50);
        // Watch for DOM changes (Streamlit reruns)
        const observer = new MutationObserver(() => styleDashboardButtons());
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

    # ---------- DATA ----------
    user_id = st.session_state.user[0]
    username = st.session_state.user[1] if len(st.session_state.user) > 1 else "Friend"

    all_messages = get_messages_by_user(user_id)
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    chats_today = sum(1 for msg in all_messages if len(msg) > 2 and msg[2] and msg[2] > yesterday)

    moods = get_moods_by_user(user_id)
    if moods:
        last_mood = moods[-1][0]
        mood_emoji_map = {"Happy": "😊", "Neutral": "😐", "Sad": "😔", "Anxious": "😰", "Angry": "😡"}
        mood_emoji = mood_emoji_map.get(last_mood, "😊")
        last_mood_display = f"{mood_emoji} {last_mood}"
    else:
        last_mood_display = "😊 Not logged yet"

    journals = get_journals_by_user(user_id)
    journal_count = len(journals)

    # ---------- TITLE ----------
    st.markdown("""
        <div class="hero-title">
            <span>🧠</span><span>MindCare AI Dashboard</span>
        </div>
        <div class="hero-subtitle">Your Personal AI Mental Wellness Companion</div>
    """, unsafe_allow_html=True)

    # ---------- WELCOME BANNER ----------
    hour = datetime.now().hour
    if hour < 12:
        greeting, note = "Good morning", "Start your day with a moment of mindfulness. 🌅"
    elif hour < 17:
        greeting, note = "Good afternoon", "Take a breath — you're doing great so far. ☀️"
    else:
        greeting, note = "Good evening", "Wind down and reflect on your day with care. 🌙"

    st.markdown(f"""
        <div class="welcome-section">
            <div class="welcome-greeting">👋 {greeting}, {username}!</div>
            <div class="welcome-note">{note}<br>Here's your wellness snapshot — every step matters. 💙</div>
        </div>
    """, unsafe_allow_html=True)

    # ---------- STATS CARDS ----------
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{chats_today}</div><div class="stat-label">💬 Chats Today</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-num-sm">{last_mood_display}</div><div class="stat-label">🎭 Last Mood</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{journal_count}</div><div class="stat-label">📓 Journal Entries</div></div>', unsafe_allow_html=True)

    # ---------- NAVIGATION BUTTONS ----------
    st.markdown('<div class="nav-title">✨ Quick Navigation</div>', unsafe_allow_html=True)

    # Row 1
    r1c1, r1c2 = st.columns(2, gap="large")
    with r1c1:
        if st.button("💬 **AI Chat**\n\nTalk with your AI companion anytime.", key="chat_btn", use_container_width=True):
            st.session_state.current_page = "Chat"
            st.query_params["page"] = "Chat"
            st.rerun()
    with r1c2:
        if st.button("📊 **Mood Log**\n\nTrack daily mood & see trends.", key="mood_btn", use_container_width=True):
            st.session_state.current_page = "Mood Analytics"
            st.query_params["page"] = "Mood Analytics"
            st.rerun()

    st.markdown("<div style='margin-top: 1.5rem'></div>", unsafe_allow_html=True)

    # Row 2
    r2c1, r2c2 = st.columns(2, gap="large")
    with r2c1:
        if st.button("🕒 **Chat History**\n\nReview all conversations.", key="history_btn", use_container_width=True):
            st.session_state.current_page = "History"
            st.query_params["page"] = "History"
            st.rerun()
    with r2c2:
        if st.button("📖 **Journal**\n\nWrite private reflections.", key="journal_btn", use_container_width=True):
            st.session_state.current_page = "Journal"
            st.query_params["page"] = "Journal"
            st.rerun()

    st.markdown('<div class="dashboard-footer">🌿 Take care of your mental wellness — one day at a time.</div>', unsafe_allow_html=True)