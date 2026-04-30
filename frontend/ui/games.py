import streamlit as st
import time
import random


def show_calm_colors_game():
    # app.py already calls apply_clean_layout + render_navbar before this.
    # Do NOT call apply_clean_layout here — it shifts the navbar down.

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    header, footer, .stDeployButton { display: none !important; }

    html, body, .stApp {
        font-family: 'Inter', sans-serif !important;
        background: #fafbfc !important;
        min-height: 100vh !important;
        position: relative !important;
    }

    /* Game screen background overlay */
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

    .stApp.game-active::before {
        opacity: 1;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .block-container {
        padding-top: 0.4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        background: transparent !important;
        margin-top: 25px;
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

    .floating-circle:nth-child(1) {
        width: 80px;
        height: 80px;
        top: 20%;
        left: 10%;
        animation-delay: 0s;
    }

    .floating-circle:nth-child(2) {
        width: 120px;
        height: 120px;
        top: 60%;
        right: 15%;
        animation-delay: -5s;
    }

    .floating-circle:nth-child(3) {
        width: 60px;
        height: 60px;
        top: 80%;
        left: 70%;
        animation-delay: -10s;
    }

    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.3; }
        100% { transform: translateY(0px) rotate(360deg); opacity: 0.7; }
    }

    /* ── GAME SCREEN BACKGROUNDS ── */
    .game-screen-bg {
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 30%, #fef7f3 70%, #fffbeb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        z-index: -1;
        pointer-events: none;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .countdown-screen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, #a7f3d0 0%, #bfdbfe 50%, #ddd6fe 100%);
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(255,255,255,0.2) 0%, transparent 50%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='3'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #1f2937;
        z-index: 1000;
    }

    .result-screen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 50%, #fce7f3 100%);
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.3) 0%, transparent 50%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #1f2937;
        z-index: 1000;
        overflow-y: auto;
    }

    /* ── HERO BANNER ── */
    .hero-banner {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 24px;
        padding: 60px 40px;
        text-align: center;
        color: #1a202c;
        margin-bottom: 40px;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        overflow: hidden;
        margin-top: 25px;
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
        margin-top: 25px;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 18px;
        font-weight: 500;
        color: #4a5568;
        position: relative;
        z-index: 1;
    }

    /* ── HOW TO PLAY SECTION ── */
    .section-title {
        text-align: center;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #64748b;
        margin: 40px 0 32px;
    }

    .play-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        margin-bottom: 32px;
    }

    .play-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 36px 28px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .play-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }

    .play-card:hover::before {
        left: 100%;
    }

    .play-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }

    .play-card.watch {
        background: linear-gradient(135deg, rgba(139,92,246,0.9) 0%, rgba(167,139,250,0.9) 100%);
        color: white;
    }

    .play-card.repeat {
        background: linear-gradient(135deg, rgba(59,130,246,0.9) 0%, rgba(96,165,250,0.9) 100%);
        color: white;
    }

    .play-card.level {
        background: linear-gradient(135deg, rgba(16,185,129,0.9) 0%, rgba(52,211,153,0.9) 100%);
        color: white;
    }

    .play-icon {
        font-size: 36px;
        margin-bottom: 20px;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }

    .play-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .play-desc {
        font-size: 14px;
        opacity: 0.95;
        line-height: 1.5;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* ── BREATHING TIP ── */
    .breathing-tip {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        border-radius: 20px;
        padding: 24px 36px;
        text-align: center;
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 40px;
        box-shadow: 0 4px 16px rgba(245,158,11,0.3);
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }

    .breathing-tip::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        transform: translate(-50%, -50%);
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.2; }
    }

    /* ── COLOR BUTTONS WITH BETTER SPACING ── */
    .color-buttons-container {
        background: rgba(255,255,255,0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 24px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    div[data-testid="column"] {
        padding: 0 12px !important;
    }

    div[data-testid="column"] button {
        padding: 48px 24px !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        border-radius: 24px !important;
        border: 3px solid rgba(255,255,255,0.6) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        color: white !important;
        margin: 8px 0 !important;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px) !important;
    }

    div[data-testid="column"] button:hover {
        transform: scale(1.05) translateY(-8px) !important;
        box-shadow: 
            0 16px 48px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.5) !important;
        border: 3px solid rgba(255,255,255,0.8) !important;
    }

    div[data-testid="column"] button:active { 
        transform: scale(0.98) translateY(-4px) !important; 
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
        box-shadow: 
            0 12px 40px rgba(240,147,251,0.4),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(20px) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        margin-top: 10px !important;
    }
    
    .start-btn-wrap .stButton > button:hover {
        transform: translateY(-6px) scale(1.05) !important;
        box-shadow: 
            0 20px 60px rgba(240,147,251,0.6),
            inset 0 1px 0 rgba(255,255,255,0.5) !important;
        border: 3px solid rgba(255,255,255,0.6) !important;
    }
    
    @keyframes btnShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── SCORE BAR ── */
    .score-bar {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.5);
        padding: 20px 40px;
        display: flex; 
        justify-content: space-around; 
        align-items: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border-radius: 0 0 24px 24px;
        margin-bottom: 24px;
    }
    
    .score-item { 
        font-size: 18px; 
        font-weight: 700; 
        color: #1f2937; 
    }
    
    .score-val { 
        font-size: 28px; 
        font-weight: 900; 
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .game-msg {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.5);
        padding: 24px 40px; 
        border-radius: 20px;
        font-size: 18px; 
        font-weight: 600; 
        color: #4338ca;
        margin: 30px auto; 
        max-width: 600px; 
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    .seq-chip {
        display: inline-block;
        padding: 32px 40px; 
        border-radius: 24px;
        margin: 12px; 
        font-size: 56px; 
        color: white;
        box-shadow: 
            0 12px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.3);
        animation: chipIn 0.6s ease;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    @keyframes chipIn {
        0%   { transform: scale(0.6) rotate(-10deg); opacity: 0; }
        60%  { transform: scale(1.15) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }

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
    }
    @keyframes chipIn {
        0%   { transform: scale(0.7); opacity: 0.2; }
        60%  { transform: scale(1.12); }
        100% { transform: scale(1); opacity: 1; }
    }

    /* ── COLOR BUTTONS ── */
    div[data-testid="column"] button {
        padding: 40px 20px !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        border-radius: 20px !important;
        border: 3px solid rgba(255,255,255,0.55) !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        color: white !important;
    }
    div[data-testid="column"] button:hover {
        transform: scale(1.07) translateY(-6px) !important;
        box-shadow: 0 14px 36px rgba(0,0,0,0.28) !important;
    }
    div[data-testid="column"] button:active { transform: scale(0.96) !important; }

    /* ── PROGRESS BAR ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        border-radius: 10px !important; height: 12px !important;
    }
    .stProgress > div {
        background: rgba(99,102,241,0.18) !important;
        border-radius: 10px !important; height: 12px !important;
    }

    /* ── MAIN BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important; font-weight: 700 !important;
        font-size: 18px !important; padding: 14px 44px !important;
        border-radius: 50px !important; border: none !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.38) !important;
        transition: all 0.25s ease !important; width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 32px rgba(99,102,241,0.52) !important;
    }

    /* ── START GAME BUTTON ── */
    .start-btn-wrap .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #667eea 100%) !important;
        background-size: 200% 200% !important;
        animation: btnShift 4s ease infinite !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 14px 0 !important;
        border-radius: 50px !important;
        border: 3px solid rgba(255,255,255,0.40) !important;
        box-shadow: 0 8px 28px rgba(240,147,251,0.50) !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 15px;
    }
    
    .start-btn-wrap {
        margin-top: 30px !important;
        padding-left: 28px !important;
    }
    .start-btn-wrap .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 14px 36px rgba(240,147,251,0.65) !important;
    }
    @keyframes btnShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
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
        box-shadow: 
            0 12px 40px rgba(102,126,234,0.4),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(20px) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .play-again-wrap .stButton > button:hover {
        transform: translateY(-6px) scale(1.05) !important;
        box-shadow: 
            0 20px 60px rgba(102,126,234,0.6),
            inset 0 1px 0 rgba(255,255,255,0.5) !important;
        border: 3px solid rgba(255,255,255,0.6) !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.35); border-radius: 8px; }
    </style>

    <script>
    /* Color the 4 game buttons by their text label */
    (function() {
        const map = {
            '💙  Blue':   'linear-gradient(135deg,#3b82f6,#60a5fa)',
            '💚  Green':  'linear-gradient(135deg,#10b981,#34d399)',
            '💜  Purple': 'linear-gradient(135deg,#8b5cf6,#a78bfa)',
            '🧡  Orange': 'linear-gradient(135deg,#f97316,#fb923c)',
        };
        function paint() {
            const doc = window.parent.document;
            doc.querySelectorAll('button').forEach(btn => {
                const t = btn.innerText.trim();
                if (map[t]) {
                    btn.style.setProperty('background', map[t], 'important');
                    btn.style.setProperty('color', '#fff', 'important');
                    btn.style.setProperty('border', '3px solid rgba(255,255,255,0.45)', 'important');
                }
            });
        }
        setTimeout(paint, 120);
        setTimeout(paint, 600);
        new MutationObserver(paint).observe(
            window.parent.document.body, { childList: true, subtree: true }
        );
    })();
    </script>
    """, unsafe_allow_html=True)

    # ── SESSION STATE ──
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

    colors = [
        {"name": "Blue",   "color": "#3b82f6", "emoji": "💙", "id": 0},
        {"name": "Green",  "color": "#10b981", "emoji": "💚", "id": 1},
        {"name": "Purple", "color": "#8b5cf6", "emoji": "💜", "id": 2},
        {"name": "Orange", "color": "#f97316", "emoji": "🧡", "id": 3},
    ]

    # ── HELPERS ──
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
                st.session_state.game_sequence = [
                    random.randint(0, 3) for _ in range(st.session_state.game_level)
                ]
                st.session_state.game_message = f"&#9989; Perfect! +{pts} points!"
        else:
            end_game()

    # ── SCREEN: HOME ──
    def show_home():
        # Banner — smaller, with reduced top margin so it sits closer to navbar
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 55%, #f093fb 100%);
            border-radius: 20px;
            margin: 8px 10px 0 10px;
            padding: 36px 20px 44px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(102,126,234,0.35);
            margin-top: 20px !important;
        ">
            <div style="font-size:44px;font-weight:900;margin-bottom:10px;
                        text-shadow:0 4px 20px rgba(0,0,0,0.25);">🎨 Calm Colors</div>
            <div style="font-size:16px;font-weight:400;opacity:0.92;">
                Train your focus &amp; relax your mind
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Start Game button — centered, styled via CSS class
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            st.markdown('<div class="start-btn-wrap">', unsafe_allow_html=True)
            if st.button("▶  Start Game", key="btn_start", use_container_width=True):
                st.session_state.game_screen = "countdown"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # How to Play label
        st.markdown("""
        <div style="text-align:center;font-size:16px;font-weight:700;letter-spacing:1.2px;
                    text-transform:uppercase;color:#6d28d9;margin:28px 0 14px;">
            📖 How to Play
        </div>
        """, unsafe_allow_html=True)

        # How to Play — lighter gradient cards with visible text
        st.markdown("""
        <div style="margin:0 16px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px;">
                <div style="background:linear-gradient(135deg,#6366f1,#818cf8);border-radius:16px;
                            padding:18px 14px;text-align:center;
                            box-shadow:0 4px 16px rgba(99,102,241,0.35);">
                    <div style="font-size:26px;margin-bottom:8px;">👁️</div>
                    <div style="font-size:13px;font-weight:700;color:#ffffff;margin-bottom:4px;">Watch</div>
                    <div style="font-size:12px;color:#e0e7ff;line-height:1.5;">
                        Colored squares flash in a sequence
                    </div>
                </div>
                <div style="background:linear-gradient(135deg,#3b82f6,#60a5fa);border-radius:16px;
                            padding:18px 14px;text-align:center;
                            box-shadow:0 4px 16px rgba(59,130,246,0.35);">
                    <div style="font-size:26px;margin-bottom:8px;">&#127919;</div>
                    <div style="font-size:13px;font-weight:700;color:#ffffff;margin-bottom:4px;">Repeat</div>
                    <div style="font-size:12px;color:#dbeafe;line-height:1.5;">
                        Click the same colors in order
                    </div>
                </div>
                <div style="background:linear-gradient(135deg,#10b981,#34d399);border-radius:16px;
                            padding:18px 14px;text-align:center;
                            box-shadow:0 4px 16px rgba(16,185,129,0.35);">
                    <div style="font-size:26px;margin-bottom:8px;">🚀</div>
                    <div style="font-size:13px;font-weight:700;color:#ffffff;margin-bottom:4px;">Level Up</div>
                    <div style="font-size:12px;color:#d1fae5;line-height:1.5;">
                        Each round gets longer — score points!
                    </div>
                </div>
            </div>
            <div style="background:linear-gradient(135deg, #8b5cf6, #c4b5fd);border-radius:16px;
                        padding:13px 20px;text-align:center;
                        box-shadow:0 4px 16px rgba(245,158,11,0.30);">
                <span style="font-size:15px;">🧘</span>
                <span style="font-size:14px;font-weight:600;color:#1c1917;margin-left:8px; margin-top: 25px;">
                    Breathe IN while watching &nbsp;·&nbsp; Breathe OUT while repeating
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SCREEN: COUNTDOWN ──
    def show_countdown():
        # Apply countdown screen background with overlay
        st.markdown("""
        <style>
        .stApp { 
            background: linear-gradient(135deg, #a7f3d0 0%, #bfdbfe 50%, #ddd6fe 100%) !important;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255,255,255,0.4) 0%, transparent 50%),
                radial-gradient(circle at 80% 50%, rgba(255,255,255,0.3) 0%, transparent 50%) !important;
        }
        .block-container {
            background: transparent !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        placeholder = st.empty()
        for num, hint in [("3","Take a deep breath in..."),
                          ("2","Focus your mind..."),
                          ("1","Get ready..."),
                          ("GO!","Let's begin!")]:
            placeholder.markdown(f"""
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                min-height: 100vh;
                background: linear-gradient(135deg, #a7f3d0 0%, #bfdbfe 50%, #ddd6fe 100%);
                background-image: 
                    radial-gradient(circle at 20% 50%, rgba(255,255,255,0.4) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(255,255,255,0.3) 0%, transparent 50%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #1f2937;
                z-index: 1000;
            ">
                <div class="floating-elements">
                    <div class="floating-circle"></div>
                    <div class="floating-circle"></div>
                    <div class="floating-circle"></div>
                </div>
                <div style="font-size:140px;font-weight:900;
                            animation:chipIn 0.8s ease;line-height:1;
                            margin-bottom:24px;
                            color:#1f2937;
                            text-shadow:0 4px 20px rgba(0,0,0,0.1);
                            position: relative;
                            z-index: 10;">
                    {num}
                </div>
                <div style="font-size:22px;
                            font-weight:600;
                            color:#374151;
                            text-shadow:0 2px 8px rgba(0,0,0,0.1);
                            position: relative;
                            z-index: 10;">
                    {hint}
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        start_game()
        st.session_state.game_screen = "game"
        st.rerun()

    # ── SCREEN: GAME ──
    def show_game():
        # Add game screen background wrapper with proper class and ensure content is on top
        st.markdown("""
        <div class="game-screen-bg"></div>
        <div class="floating-elements">
            <div class="floating-circle"></div>
            <div class="floating-circle"></div>
            <div class="floating-circle"></div>
        </div>
        <style>
        .stApp .block-container { 
            position: relative !important; 
            z-index: 10 !important;
            padding-top: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="score-bar">
            <div class="score-item">&#127919; Level  <span class="score-val">{st.session_state.game_level}</span></div>
            <div class="score-item">&#127942; Score  <span class="score-val">{st.session_state.game_score}</span></div>
            <div class="score-item">&#128202; Length <span class="score-val">{len(st.session_state.game_sequence)}</span></div>
        </div>
        """, unsafe_allow_html=True)

        # Sequence playback
        if st.session_state.is_playing_seq:
            st.markdown(
                f'<div class="game-msg">🎵 Watch the sequence — Length: {len(st.session_state.game_sequence)}</div>',
                unsafe_allow_html=True
            )
            slot = st.empty()
            for idx in st.session_state.game_sequence:
                c = colors[idx]
                slot.markdown(f"""
                <div style="text-align:center;margin:40px 0;">
                    <div class="seq-chip" style="background:{c['color']};">
                        {c['emoji']} {c['name']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.85)
            time.sleep(0.4)
            st.session_state.is_playing_seq = False
            st.session_state.waiting        = True
            st.session_state.game_message   = "Your turn! Repeat the sequence..."
            st.rerun()

        # Player turn
        if st.session_state.waiting:
            st.markdown(
                '<div class="game-msg">🎮 Your turn! Click the colors in order...</div>',
                unsafe_allow_html=True
            )
            total    = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.markdown(
                    f"<p style='text-align:center;color:#4b5563;font-weight:600;margin:8px 0 20px;text-shadow:0 2px 4px rgba(0,0,0,0.1);'>"
                    f"Progress: {progress} / {total}</p>",
                    unsafe_allow_html=True
                )

            # Color buttons with better spacing
            st.markdown('<div class="color-buttons-container">', unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")
            with col1:
                if st.button(f"{colors[0]['emoji']}  {colors[0]['name']}", key="color_blue",  use_container_width=True):
                    handle_move(0); st.rerun()
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                if st.button(f"{colors[2]['emoji']}  {colors[2]['name']}", key="color_purple", use_container_width=True):
                    handle_move(2); st.rerun()
            with col2:
                if st.button(f"{colors[1]['emoji']}  {colors[1]['name']}", key="color_green",  use_container_width=True):
                    handle_move(1); st.rerun()
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                if st.button(f"{colors[3]['emoji']}  {colors[3]['name']}", key="color_orange", use_container_width=True):
                    handle_move(3); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1.2, 1, 1.2])
            with c2:
                if st.button("End Game", key="btn_end"):
                    end_game(); st.rerun()

    # ── SCREEN: RESULT ──
    def show_result():
        level = st.session_state.game_level
        score = st.session_state.game_score
        is_win = score > 50
        emoji = "🎉" if is_win else "💙"
        title = "Amazing!" if is_win else "Game Over"
        
        # Apply soft background
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Add some top spacing
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        
        # Main result banner
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 50%, #fce7f3 100%);
            border-radius: 24px;
            padding: 48px 40px;
            text-align: center;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.5);
        ">
            <div style="font-size:80px;margin-bottom:20px;">{emoji}</div>
            <h1 style="font-size:48px;font-weight:900;color:#6366f1;margin-bottom:40px;">{title}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats cards in columns
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 32px 24px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.5);
            ">
                <div style="font-size:24px;margin-bottom:16px;">🎯</div>
                <h3 style="font-size:18px;font-weight:600;color:#1f2937;margin-bottom:16px;">Level Reached</h3>
                <div style="font-size:48px;font-weight:900;color:#6366f1;">{level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 32px 24px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.5);
            ">
                <div style="font-size:24px;margin-bottom:16px;">⭐</div>
                <h3 style="font-size:18px;font-weight:600;color:#1f2937;margin-bottom:16px;">Final Score</h3>
                <div style="font-size:48px;font-weight:900;color:#8b5cf6;">{score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mindfulness message
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.info("🧘 Every game is practice for mindfulness • Breathe deeply and try again")
        
        # Play Again button
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎮 Play Again", key="btn_again", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()

    # ── ROUTER ──
    screen = st.session_state.game_screen
    if   screen == "home":      show_home()
    elif screen == "countdown": show_countdown()
    elif screen == "game":      show_game()
    elif screen == "result":    show_result()


def show_aesthetic_game_selector():
    show_calm_colors_game();