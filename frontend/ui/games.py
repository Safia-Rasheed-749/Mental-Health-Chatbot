import streamlit as st
import time
import random

def show_calm_colors_game():
    # Detect if opened from sidebar (logged-in) or navbar (public)
    from_sidebar = st.session_state.get("games_from_sidebar", False)

    # ── LAYOUT CONTROL based on entry point ──
    if not from_sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebar"]        { display: none !important; }
        [data-testid="collapsedControl"]  { display: none !important; }
        .main { margin-left: 0rem !important; }
        header[data-testid="stHeader"]   { display: none !important; }
        footer, .stAppDeployButton       { display: none !important; }
        .main .block-container { padding-top: 100px !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        footer, .stAppDeployButton { display: none !important; }
        .block-container { padding-top: 0rem !important; margin-top: 0rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # ======================= COMPLETE FIXED CSS =======================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 45%, #F5F3FF 100%) !important;
        min-height: 100vh !important;
        position: relative !important;
        overflow-x: hidden !important;
    }

    .main .block-container {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
        background: transparent !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 70%, #f5576c 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        opacity: 0;
        pointer-events: none;
        z-index: -1;
        transition: opacity 0.5s ease;
    }

    .stApp.game-active::before { opacity: 1; }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @media (max-width: 1200px) {
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    }

    /* ── FLOATING ELEMENTS ── */
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    .floating-circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        animation: float 20s infinite linear;
    }
    .floating-circle:nth-child(1) { width: 80px; height: 80px; top: 20%; left: 10%; animation-delay: 0s; }
    .floating-circle:nth-child(2) { width: 120px; height: 120px; top: 60%; right: 15%; animation-delay: -5s; }
    .floating-circle:nth-child(3) { width: 60px; height: 60px; top: 80%; left: 70%; animation-delay: -10s; }
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.3; }
        100% { transform: translateY(0px) rotate(360deg); opacity: 0.7; }
    }

    /* ── GAME SCREEN BACKGROUNDS ── */
    .game-screen-bg {
        position: fixed;
        top: 10px;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 30%, #fef7f3 70%, #fffbeb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        z-index: -1;
        pointer-events: none;
    }
    .result-screen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 50%, #fce7f3 100%);
        background-image: radial-gradient(circle at 25% 25%, rgba(255,255,255,0.4) 0%, transparent 50%),
                          radial-gradient(circle at 75% 75%, rgba(255,255,255,0.3) 0%, transparent 50%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #1f2937;
        z-index: 1000;
        overflow-y: auto;
    }

    /* ── HERO BANNER (HTML ADDED IN HOME SCREEN) ── bannner backgroubnd color changes */
    .hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102,126,234,0.25);
    color: white;
}
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    /* hero main title color changes.*/
    .hero-title {
        font-size: 50px !important;
        font-weight: 900;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    /* line under the main heading c of hero heading .*/
    .hero-subtitle {
        font-size: 18px;
        font-weight: 500;
        color: white !important;
        position: relative;
        z-index: 1;
    }

    /* ── LOGGED-IN HEADER (game-page-header) ── */
    .game-page-header {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(91,141,239,0.28);
        border-radius: 20px;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    .game-header-avatar {
        width: 46px; height: 46px; border-radius: 50%;
        background: rgba(255,255,255,0.22);
        border: 2px solid rgba(255,255,255,0.45);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.12);
        animation: headerPulse 3s ease-in-out infinite;
    }
    .game-header-text h1 { margin: 0; font-size: 20px; font-weight: 700; color: #ffffff; line-height: 1.2; }
    .game-header-text p { margin: 2px 0 0; font-size: 14px; color: rgba(255,255,255,0.78); font-weight: 400; }
    .game-header-status {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: rgba(255,255,255,0.85);
        font-weight: 500;
    }
    .game-status-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 6px #4ade80;
        animation: statusBlink 2s ease-in-out infinite;
    }
    @keyframes headerPulse {
        0%,100% { box-shadow: 0 0 0 4px rgba(255,255,255,0.12); }
        50% { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
    }
    @keyframes statusBlink {
        0%,100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .game-msg {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 100%) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(167,139,250,0.25) !important;
        padding: 24px 40px;
        border-radius: 20px;
        font-size: 18px; font-weight: 600;
        color: #6d28d9 !important;
        margin: 10px auto;
        max-width: 600px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(139,92,246,0.1) !important;
    }


    /* ── START GAME BUTTON ── */
    .start-btn-wrap {
        margin-top: 40px !important;
        text-align: center;
    }
    .start-btn-wrap .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #667eea 100%) !important;
        background-size: 200% 200% !important;
        animation: btnShift 4s ease infinite !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        padding: 16px 48px !important;
        border-radius: 50px !important;
        border: 3px solid rgba(255,255,255,0.4) !important;
        box-shadow: 0 12px 40px rgba(240,147,251,0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(20px) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        margin-top: 10px !important;
    }
    .start-btn-wrap .stButton > button:hover {
        transform: translateY(-6px) scale(1.05) !important;
        box-shadow: 0 20px 60px rgba(240,147,251,0.6), inset 0 1px 0 rgba(255,255,255,0.5) !important;
        border: 3px solid rgba(255,255,255,0.6) !important;
    }
    @keyframes btnShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── SEQ CHIP ANIMATION ── */
    .seq-chip {
        display: inline-block;
        padding: 32px 40px;
        border-radius: 24px;
        margin: 12px;
        font-size: 56px;
        color: white;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.3);
        animation: chipIn 0.6s ease;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.3);
    }
    @keyframes chipIn {
        0%   { transform: scale(0.6) rotate(-10deg); opacity: 0; }
        60%  { transform: scale(1.15) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    @keyframes popIn {
        0%   { transform: scale(0.6); opacity: 0; }
        70%  { transform: scale(1.08); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* ── PROGRESS BAR ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 12px !important;
        height: 16px !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3) !important;
    }
    .stProgress > div {
        background: rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        height: 16px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ── SCROLLBAR (fixed duplicate) ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }

    /* ── MAIN BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        padding: 12px 18px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.38) !important;
        transition: all 0.25s ease !important;
        max-width: 320px !important;
        margin: auto !important;
        display: block !important;
    }
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 32px rgba(99,102,241,0.52) !important;
    }

    /* ── PLAY AGAIN BUTTON ── */
    .play-again-wrap {
        margin-top: 40px !important;
        text-align: center;
    }
    .play-again-wrap .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        padding: 16px 48px !important;
        border-radius: 50px !important;
        border: 3px solid rgba(255,255,255,0.4) !important;
        box-shadow: 0 12px 40px rgba(102,126,234,0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(20px) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    .play-again-wrap .stButton > button:hover {
        transform: translateY(-6px) scale(1.05) !important;
        box-shadow: 0 20px 60px rgba(102,126,234,0.6), inset 0 1px 0 rgba(255,255,255,0.5) !important;
        border: 3px solid rgba(255,255,255,0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── SESSION STATE (unchanged) ──
    if 'game_screen' not in st.session_state:
        st.session_state.game_screen    = "home"
        st.session_state.game_active    = False
        st.session_state.game_sequence  = []
        st.session_state.player_index   = 0
        st.session_state.game_level     = 1
        st.session_state.game_score     = 0
        st.session_state.is_playing_seq = False
        st.session_state.waiting        = False
        st.session_state.game_message   = ""
    st.session_state.public_game_mode = st.session_state.get("public_game_mode", False)

    colors = [
        {"name": "Blue",   "color": "#3b82f6", "emoji": "💙", "id": 0},
        {"name": "Green",  "color": "#10b981", "emoji": "💚", "id": 1},
        {"name": "Purple", "color": "#8b5cf6", "emoji": "💜", "id": 2},
        {"name": "Orange", "color": "#f97316", "emoji": "🧡", "id": 3},
    ]

    # ── HELPERS (unchanged) ──
    def start_game():
        st.session_state.game_active    = True
        st.session_state.game_sequence  = [random.randint(0, 3)]
        st.session_state.player_index   = 0
        st.session_state.game_level     = 1
        st.session_state.game_score     = 0
        st.session_state.is_playing_seq = True
        st.session_state.waiting        = False
        st.session_state.game_message   = "Watch the sequence carefully..."

    def end_game():
        st.session_state.game_active    = False
        st.session_state.is_playing_seq = False
        st.session_state.waiting        = False
        st.session_state.game_screen    = "result"

    def reset_game():
        st.session_state.game_screen    = "home"
        st.session_state.game_active    = False
        st.session_state.game_sequence  = []
        st.session_state.player_index   = 0
        st.session_state.game_level     = 1
        st.session_state.game_score     = 0
        st.session_state.is_playing_seq = False
        st.session_state.waiting        = False
        st.session_state.game_message   = ""

    def handle_move(color_id):
        if not st.session_state.game_active or not st.session_state.waiting:
            return
        expected = st.session_state.game_sequence[st.session_state.player_index]
        if color_id == expected:
            st.session_state.player_index += 1
            if st.session_state.player_index == len(st.session_state.game_sequence):
                pts = 10 * st.session_state.game_level
                st.session_state.game_score  += pts
                st.session_state.game_level  += 1
                st.session_state.player_index = 0
                st.session_state.waiting      = False
                st.session_state.is_playing_seq = True
                level = st.session_state.game_level
                
                # Sequence length progression
                if level <= 3:
                    new_length = 3
                elif level <= 6:
                    new_length = 4
                elif level <= 9:
                    new_length = 5
                elif level <= 12:
                    new_length = 6
                else:
                    new_length = min(8, 6 + (level - 12) // 3)
                
                new_sequence = []
                for i in range(new_length):
                    if level < 5:
                        new_color = random.randint(0, 3)
                    elif level < 10:
                        if len(new_sequence) > 0:
                            last = new_sequence[-1]
                            choices = [0,1,2,3]
                            choices.remove(last)
                            new_color = random.choice(choices)
                        else:
                            new_color = random.randint(0, 3)
                    else:
                        patterns = [[0,1,2,3], [3,2,1,0], [0,2,1,3], [1,3,0,2]]
                        if random.random() > 0.6 and i < len(patterns):
                            pattern = random.choice(patterns)
                            new_color = pattern[i % 4]
                        else:
                            if len(new_sequence) > 0:
                                last = new_sequence[-1]
                                choices = [0,1,2,3]
                                choices.remove(last)
                                new_color = random.choice(choices)
                            else:
                                new_color = random.randint(0, 3)
                    new_sequence.append(new_color)
                
                st.session_state.game_sequence = new_sequence
                if st.session_state.get("public_game_mode", False) and st.session_state.game_level > 5:
                    st.session_state.game_screen = "login_popup"
                    return
                st.session_state.game_message = f"✅ Perfect! +{pts} points!"
        else:
            end_game()

    # ── SCREEN: HOME (with hero-banner HTML added) ──
    def show_home():
        if from_sidebar:
            st.markdown("""
            <div class="game-page-header">
                <div class="game-header-avatar">🎨</div>
                <div class="game-header-text">
                    <h1>Calm Colors Game</h1>
                    <p>Train your focus &amp; relax your mind</p>
                </div>
                <div class="game-header-status">
                    <div class="game-status-dot"></div>
                    Ready to play
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # HERO BANNER – now using the CSS class
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">🎨 Calm Colors</div>
                <div class="hero-subtitle">Train your focus &amp; relax your mind</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            st.markdown('<div class="start-btn-wrap">', unsafe_allow_html=True)
            if st.button("▶  Start Game", key="btn_start", use_container_width=True, type="primary"):
                st.session_state.game_screen = "countdown"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        #how to play button ka color
        # How to Play text (fixed colon)
        st.markdown("""
        <div style="text-align:center; font-size:18px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; color:black; margin:28px 0 34px;">
            📖 How to Play
        </div>
        """, unsafe_allow_html=True)
        
#how to play and play cards col,ors and background changes
        # How to Play cards (animated)
        st.markdown("""
        <style>
        @keyframes cardShift1 { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
        @keyframes cardShift2 { 0%{background-position:100% 50%} 50%{background-position:0% 50%} 100%{background-position:100% 50%} }
        @keyframes cardShift3 { 0%{background-position:50% 0%} 50%{background-position:50% 100%} 100%{background-position:50% 0%} }
        .card1 { background:linear-gradient(135deg,#a5b4fc,#c7d2fe,#ddd6fe,#a5b4fc);background-size:300% 300%;animation:cardShift1 6s ease infinite; }
        .card2 { background:linear-gradient(135deg,#93c5fd,#bfdbfe,#dbeafe,#93c5fd);background-size:300% 300%;animation:cardShift2 6s ease infinite; }
        .card3 { background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#d1fae5,#6ee7b7);background-size:300% 300%;animation:cardShift3 6s ease infinite; }
        </style>
        <div style="margin:0 16px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px;">
                <div class="card1" style="border-radius:16px;padding:18px 14px;text-align:center;box-shadow:0 4px 16px rgba(165,180,252,0.3);">
                    <div style="font-size:26px;margin-bottom:8px;">👁️</div>
                    <div style="font-size:13px;font-weight:700;color:#3730a3;margin-bottom:4px;">Watch</div>
                    <div style="font-size:12px;color:#4338ca;line-height:1.5;">Colored squares flash in a sequence</div>
                </div>
                <div class="card2" style="border-radius:16px;padding:18px 14px;text-align:center;box-shadow:0 4px 16px rgba(147,197,253,0.3);">
                    <div style="font-size:26px;margin-bottom:8px;">🎯</div>
                    <div style="font-size:13px;font-weight:700;color:#1d4ed8;margin-bottom:4px;">Repeat</div>
                    <div style="font-size:12px;color:#1e40af;line-height:1.5;">Click the same colors in order</div>
                </div>
                <div class="card3" style="border-radius:16px;padding:18px 14px;text-align:center;box-shadow:0 4px 16px rgba(110,231,183,0.3);">
                    <div style="font-size:26px;margin-bottom:8px;">🚀</div>
                    <div style="font-size:13px;font-weight:700;color:#065f46;margin-bottom:4px;">Level Up</div>
                    <div style="font-size:12px;color:#047857;line-height:1.5;">Each round gets longer — score points!</div>
                </div>
            </div>
            <div style="background:linear-gradient(135deg,#ddd6fe,#ede9fe);border-radius:16px;padding:13px 20px;text-align:center;box-shadow:0 4px 16px rgba(167,139,250,0.2);">
                <span style="font-size:15px;">🧘</span>
                <span style="font-size:14px;font-weight:600;color:#5b21b6;margin-left:8px;">Breathe IN while watching &nbsp;·&nbsp; Breathe OUT while repeating</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SCREEN: COUNTDOWN (unchanged) ──
    def show_countdown():
        st.markdown("""
        <style>
        @keyframes countdownShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes starFloat {
            0%   { transform: translateY(0px) translateX(0px); opacity: 0.8; }
            50%  { transform: translateY(-15px) translateX(8px); opacity: 0.4; }
            100% { transform: translateY(0px) translateX(0px); opacity: 0.8; }
        }
        .stApp {
            background: linear-gradient(135deg, #0d3b4f 0%, #0a4a5e 15%, #0e6b7a 30%, #1a7a6e 45%, #0d5c6e 60%, #0a3d52 75%, #0d3b4f 100%) !important;
            background-size: 400% 400% !important;
            animation: countdownShift 8s ease infinite !important;
        }
        .block-container {
            background: transparent !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        placeholder = st.empty()
        for num, hint in [("3", "Take a deep breath in..."),
                          ("2", "Focus your mind..."),
                          ("1", "Get ready..."),
                          ("GO!", "Let's begin!")]:
            #countdown screen color changes
            placeholder.markdown(f"""
            <div style="position:fixed;top:0;left:0;right:0;bottom:0;background:linear-gradient(135deg,#0d3b4f 0%,#0a4a5e 15%,#0e6b7a 30%,#1a7a6e 45%,#0d5c6e 60%,#0a3d52 75%,#0d3b4f 100%);background-size:400% 400%;animation:countdownShift 8s ease infinite;display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:9999;overflow:hidden;">
                <div style="position:absolute;top:8%;left:15%;width:3px;height:3px;background:white;border-radius:50%;animation:starFloat 3s ease infinite;opacity:0.8;"></div>
                <div style="position:absolute;top:15%;left:70%;width:2px;height:2px;background:white;border-radius:50%;animation:starFloat 4s ease infinite 1s;opacity:0.6;"></div>
                <div style="position:absolute;top:25%;left:40%;width:2px;height:2px;background:white;border-radius:50%;animation:starFloat 5s ease infinite 0.5s;opacity:0.7;"></div>
                <div style="position:absolute;top:10%;left:85%;width:3px;height:3px;background:white;border-radius:50%;animation:starFloat 3.5s ease infinite 2s;opacity:0.5;"></div>
                <div style="position:absolute;top:35%;left:10%;width:2px;height:2px;background:white;border-radius:50%;animation:starFloat 4.5s ease infinite 1.5s;opacity:0.6;"></div>
                <div style="position:absolute;top:20%;left:55%;width:2px;height:2px;background:white;border-radius:50%;animation:starFloat 6s ease infinite 0.8s;opacity:0.5;"></div>
                <div style="position:absolute;top:5%;left:30%;width:2px;height:2px;background:white;border-radius:50%;animation:starFloat 3.8s ease infinite 2.5s;opacity:0.7;"></div>
                <div style="position:absolute;top:30%;left:80%;width:3px;height:3px;background:white;border-radius:50%;animation:starFloat 5.5s ease infinite 0.3s;opacity:0.6;"></div>
                <div style="position:absolute;bottom:0;left:0;right:0;height:45%;background:linear-gradient(180deg,transparent 0%,#0a3347 40%,#071f2e 100%);border-radius:60% 60% 0 0 / 20% 20% 0 0;"></div>
                <div style="position:absolute;bottom:0;left:-10%;right:-10%;height:35%;background:linear-gradient(180deg,transparent 0%,#0d4a3a 40%,#082a20 100%);border-radius:50% 50% 0 0 / 15% 15% 0 0;opacity:0.7;"></div>
                <div style="position:absolute;bottom:0;left:5%;right:-5%;height:25%;background:linear-gradient(180deg,transparent 0%,#0a3d2e 50%,#051a14 100%);border-radius:55% 45% 0 0 / 18% 18% 0 0;opacity:0.8;"></div>
                <div style="font-size:140px;font-weight:900;color:white;text-shadow:0 0 40px rgba(100,220,200,0.6),0 4px 20px rgba(0,0,0,0.4);line-height:1;margin-bottom:24px;position:relative;z-index:10;animation:popIn 0.6s ease;">{num}</div>
                <div style="font-size:22px;font-weight:500;color:rgba(180,230,220,0.9);text-shadow:0 2px 12px rgba(0,0,0,0.3);position:relative;z-index:10;letter-spacing:1px;">{hint}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        start_game()
        st.session_state.game_screen = "game"
        st.rerun()

    # ── SCREEN: GAME (unchanged, but ensures .game-msg, .score-bar etc. are used) ──
    def show_game():
        top_padding = "4rem" if from_sidebar else "110px"
        st.markdown(f"""
        <style>
        @keyframes softShift {{
            0%   {{ background-position: 0% 50%; }}
            50%  {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .stApp {{
            background: linear-gradient(135deg, #c9d6ff, #e2c9ff, #ffd6e7, #c9f0ff, #c9ffe8, #c9d6ff) !important;
            background-size: 400% 400% !important;
            animation: softShift 10s ease infinite !important;
        }}
        .stApp .block-container {{ 
            position: relative !important; 
            z-index: 10 !important;
            padding-top: {top_padding} !important;
            background: transparent !important;
        }}
        div.game-msg {{
            background: linear-gradient(135deg, rgba(255,255,255,0.55), rgba(255,255,255,0.35)) !important;
            border: 1.5px solid rgba(255,255,255,0.5) !important;
            color: #5b4fcf !important;
            box-shadow: 0 4px 24px rgba(100,180,180,0.2) !important;
            border-radius: 16px !important;
            padding: 20px 40px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin: 10px auto 24px auto !important;
            max-width: 600px !important;
            text-align: center !important;
            backdrop-filter: blur(12px) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        #score bar container bacxkground color headings color 

        st.markdown(f"""
        <div style="
            background:rgba(255,255,255,0.45);
            backdrop-filter:blur(12px);
            border:1.5px solid rgba(255,255,255,0.5);
            border-radius:20px;
            padding:18px 30px;
            display:flex;
            justify-content:space-around;
            align-items:center;
            margin-bottom:24px;
             box-shadow:0 6px 24px rgba(0,0,0,0.12);
        ">
                <div style="text-align:center;">
                    <div style="font-size:14px;font-weight:600;color:#5b4fcf;">🎯 LEVEL</div>
                    <div style="font-size:30px;font-weight:900;color:#7c3aed;">
                        {st.session_state.game_level}
                    </div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:14px;font-weight:600;color:#5b4fcf;">🏆 SCORE</div>
                    <div style="font-size:30px;font-weight:900;color:#7c3aed;">
                        {st.session_state.game_score}
                   </div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:14px;font-weight:600;color:#5b4fcf;">📏 LENGTH</div>
                    <div style="font-size:30px;font-weight:900;color:#7c3aed;">
                        {len(st.session_state.game_sequence)}
                    </div>
                </div>
             </div>
            """, unsafe_allow_html=True)

        if st.session_state.is_playing_seq:
            st.markdown(f'<div class="game-msg">🎵 Watch the sequence — Length: {len(st.session_state.game_sequence)}</div>', unsafe_allow_html=True)
            slot = st.empty()
            for idx in st.session_state.game_sequence:
                c = colors[idx]
                slot.markdown(f"""
                <div style="text-align:center;margin:40px 0;animation:popIn 0.3s ease;">
                    <div class="seq-chip" style="background:{c['color']};">{c['emoji']} {c['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1.2)
                slot.empty()
                time.sleep(0.15)
            st.session_state.is_playing_seq = False
            st.session_state.waiting = True
            st.rerun()

        if st.session_state.waiting:
            st.markdown('<div class="game-msg">🎮 Your turn! Click the colors in order...</div>', unsafe_allow_html=True)
            total = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.markdown(f"<p style='text-align:center;color:#4b5563;font-weight:600;margin:8px 0 20px;text-shadow:0 2px 4px rgba(0,0,0,0.1);'>Progress: {progress} / {total}</p>", unsafe_allow_html=True)

            _, center, _ = st.columns([1, 2, 1])
            with center:
                r1c1, r1c2 = st.columns(2, gap="large")
                with r1c1:
                    if st.button(f"{colors[0]['emoji']}  {colors[0]['name']}", key="color_blue", use_container_width=True):
                        handle_move(0); st.rerun()
                with r1c2:
                    if st.button(f"{colors[1]['emoji']}  {colors[1]['name']}", key="color_green", use_container_width=True):
                        handle_move(1); st.rerun()
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                r2c1, r2c2 = st.columns(2, gap="large")
                with r2c1:
                    if st.button(f"{colors[2]['emoji']}  {colors[2]['name']}", key="color_purple", use_container_width=True):
                        handle_move(2); st.rerun()
                with r2c2:
                    if st.button(f"{colors[3]['emoji']}  {colors[3]['name']}", key="color_orange", use_container_width=True):
                        handle_move(3); st.rerun()
                st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
                st.markdown("""
                <style>

/* ─── PASTED FINAL GAME CSS ─── */

    
/* ─── BASE BUTTON STYLE ─── */
div[data-testid="stButton"] > button {
    color: white !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 22px 16px !important;
    border-radius: 22px !important;
    border: none !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25) !important;
}

/* ─── TARGET BY KEY (WORKING METHOD) ─── */

button[aria-label*="Blue"] {
    background: linear-gradient(135deg,#2563eb,#1d4ed8) !important;
}

button[aria-label*="Green"] {
    background: linear-gradient(135deg,#16a34a,#15803d) !important;
}

button[aria-label*="Purple"] {
    background: linear-gradient(135deg,#9333ea,#7e22ce) !important;
}

button[aria-label*="Orange"] {
    background: linear-gradient(135deg,#f97316,#ea580c) !important;
}

/* ─── HOVER EFFECT ─── */
div[data-testid="stButton"] > button:hover {
    transform: scale(1.06) translateY(-4px) !important;
    filter: brightness(1.1) !important;
}

</style>
""", unsafe_allow_html=True)
                #End game color changes
                st.markdown("""
                <style>
                div[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }
                div[data-testid="stFormSubmitButton"] > button {
                    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
                    color: white !important;
                    font-weight: 600 !important;
                    font-size: 15px !important;
                    padding: 10px 0 !important;
                    border-radius: 40px !important;
                    border: none !important;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
                    transition: all 0.3s ease !important;
                    width: 100% !important;
                }
                div[data-testid="stFormSubmitButton"] > button:hover { filter: brightness(1.08) !important; transform: translateY(-2px) !important; }
                </style>
                """, unsafe_allow_html=True)
                _, end_btn_col, _ = st.columns([1, 1.2, 1])
                with end_btn_col:
                    with st.form("end_game_form", border=False):
                        if st.form_submit_button("⏹ End Game", use_container_width=True):
                            end_game(); st.rerun()

    # ── SCREEN: RESULT (unchanged) ──
    def show_result():
        level = st.session_state.game_level
        score = st.session_state.game_score
        emoji = "🎉"
        title = "Game Ended!"
        st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(160deg, #0a0e1a 0%, #0d1b3e 35%, #0f2352 60%, #0a1628 100%) !important;
        }}
        .main .block-container {{
            padding-top: 2rem !important;
            max-width: 100% !important;
        }}
        div[data-testid="stForm"] {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin-top: 0 !important;
        }}
        div[data-testid="stForm"] button {{
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            padding: 13px 0 !important;
            border-radius: 40px !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(102,126,234,0.45) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        div[data-testid="stForm"] button:hover {{
            filter: brightness(1.1) !important;
            transform: translateY(-3px) !important;
        }}
        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
            gap: 0 !important;
        }}
        </style>
        <div style="display: flex; flex-direction: column; align-items: center; padding: 20px 20px 0 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 55%, #9b59b6 100%); border-radius: 24px 24px 0 0; padding: 20px 36px 28px; text-align: center; box-shadow: 0 20px 60px rgba(102,126,234,0.55), 0 8px 32px rgba(118,75,162,0.4); border: 1.5px solid rgba(255,255,255,0.25); border-bottom: none; width: 100%; max-width: 400px;">
                <div style="font-size:56px;margin-bottom:14px;">{emoji}</div>
                <div style="font-size:30px;font-weight:900;color:white;margin-bottom:24px;text-shadow:0 2px 12px rgba(0,0,0,0.3);">{title}</div>
                <div style="display:flex;justify-content:center;gap:14px;margin-bottom:20px;">
                    <div style="background:rgba(255,255,255,0.18);border-radius:14px;padding:16px 24px;flex:1;border:1px solid rgba(255,255,255,0.3);">
                        <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.85);margin-bottom:8px;text-transform:uppercase;letter-spacing:1.5px;">🎯 Level</div>
                        <div style="font-size:38px;font-weight:900;color:white;">{level}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.18);border-radius:14px;padding:16px 24px;flex:1;border:1px solid rgba(255,255,255,0.3);">
                        <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.85);margin-bottom:8px;text-transform:uppercase;letter-spacing:1.5px;">⭐ Score</div>
                        <div style="font-size:38px;font-weight:900;color:white;">{score}</div>
                    </div>
                </div>
                <div style="font-size:13px;color:rgba(255,255,255,0.88);line-height:1.7;background:rgba(255,255,255,0.15);border-radius:12px;padding:14px 18px;">
                    Every game is practice for mindfulness<br>Breathe deeply and try again 🧘
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        _, btn_col, _ = st.columns([1, 1.4, 1])
        with btn_col:
            with st.form("play_again_form", border=False):
                submitted = st.form_submit_button("🎮 Play Again", use_container_width=True)
                if submitted:
                    st.session_state.game_screen = "countdown"
                    st.rerun()

    def show_login_popup():
        _, col, _ = st.columns([1, 1.2, 1])
        with col:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 55%,#9b59b6 100%);
                        border-radius:24px;margin-top:80px;padding:32px 28px 28px;text-align:center;
                        color:white;box-shadow:0 20px 60px rgba(102,126,234,0.55),0 8px 32px rgba(118,75,162,0.4);
                        border:1.5px solid rgba(255,255,255,0.25);">
                <div style="font-size:52px;margin-bottom:12px;">🔐</div>
                <h2 style="font-size:24px;font-weight:800;margin-bottom:10px;">Unlock Unlimited Levels</h2>
                <p style="opacity:0.88;font-size:14px;line-height:1.65;margin-bottom:0;">
                    You've reached 5 free levels.<br>
                    Sign in or create an account to continue.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
            st.markdown("""
            <style>
            .game-popup-btns .stButton > button {
                background: linear-gradient(135deg,#667eea,#764ba2) !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                padding: 11px 16px !important;
                border-radius: 50px !important;
                border: 2px solid rgba(255,255,255,0.3) !important;
                box-shadow: 0 6px 20px rgba(102,126,234,0.35) !important;
                transition: all 0.2s ease !important;
                width: 100% !important;
            }
            .game-popup-btns .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 28px rgba(102,126,234,0.5) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<div class="game-popup-btns">', unsafe_allow_html=True)
            b1, b2 = st.columns(2, gap="medium")
            with b1:
                if st.button("Create Account", key="popup_register", use_container_width=True):
                    st.session_state.page = "auth"
                    st.session_state.game_screen = "home"
                    st.session_state.public_game_mode = False
                    st.rerun()
            with b2:
                if st.button("← Back to Home", key="popup_home", use_container_width=True):
                    st.session_state.page = "landing"
                    st.session_state.game_screen = "home"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── ROUTER ──
    screen = st.session_state.game_screen
    if screen == "home":
        show_home()
    elif screen == "countdown":
        show_countdown()
    elif screen == "game":
        show_game()
    elif screen in ("result", "login_popup"):
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(160deg, #0a0e1a 0%, #0d1b3e 35%, #0f2352 60%, #0a1628 100%) !important;
            background-attachment: fixed !important;
        }
        .main .block-container { position: relative !important; z-index: 10 !important; }
        </style>
        """, unsafe_allow_html=True)
        if screen == "result":
            show_result()
        else:
            show_login_popup()

def show_aesthetic_game_selector():
    show_calm_colors_game()