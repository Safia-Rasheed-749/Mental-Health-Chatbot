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
        padding-top: 1.2rem !important;
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
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #fdf4ff 100%) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(167,139,250,0.25) !important;
        padding: 20px 40px;
        display: flex; 
        justify-content: space-around; 
        align-items: center;
        box-shadow: 0 8px 32px rgba(139,92,246,0.12) !important;
        border-radius: 0 0 24px 24px;
        margin-bottom: 24px;
        margin-top: 38px;
    }
    
    .score-item { 
        font-size: 18px; 
        font-weight: 700; 
        color: #6d28d9 !important; 
    }
    
    .score-val { 
        font-size: 28px; 
        font-weight: 900; 
        background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    .game-msg {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 100%) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(167,139,250,0.25) !important;
        padding: 24px 40px; 
        border-radius: 20px;
        font-size: 18px; 
        font-weight: 600; 
        color: #6d28d9 !important;
        margin: 10px auto; 
        max-width: 600px; 
        text-align: center;
        box-shadow: 0 8px 32px rgba(139,92,246,0.1) !important;
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
            margin: 28px 10px 0 10px;
            padding: 36px 20px 44px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(102,126,234,0.35);
            margin-top: 32px !important;
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
        # Apply animated teal-blue background only for countdown
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
            background: linear-gradient(
                135deg,
                #0d3b4f 0%,
                #0a4a5e 15%,
                #0e6b7a 30%,
                #1a7a6e 45%,
                #0d5c6e 60%,
                #0a3d52 75%,
                #0d3b4f 100%
            ) !important;
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
                <div style="font-size:140px;font-weight:900;color:white;text-shadow:0 0 40px rgba(100,220,200,0.6),0 4px 20px rgba(0,0,0,0.4);line-height:1;margin-bottom:24px;position:relative;z-index:10;animation:chipIn 0.6s ease;">{num}</div>
                <div style="font-size:22px;font-weight:500;color:rgba(180,230,220,0.9);text-shadow:0 2px 12px rgba(0,0,0,0.3);position:relative;z-index:10;letter-spacing:1px;">{hint}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        start_game()
        st.session_state.game_screen = "game"
        st.rerun()

    # ── SCREEN: GAME ──
    def show_game():
        st.markdown("""
        <style>
        @keyframes softShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .stApp {
            background: linear-gradient(135deg, #c9d6ff, #e2c9ff, #ffd6e7, #c9f0ff, #c9ffe8, #c9d6ff) !important;
            background-size: 400% 400% !important;
            animation: softShift 10s ease infinite !important;
        }
        .stApp .block-container { 
            position: relative !important; 
            z-index: 10 !important;
            padding-top: 1rem !important;
            background: transparent !important;
        }
        div.score-bar {
            background: linear-gradient(135deg, rgba(255,255,255,0.55), rgba(255,255,255,0.35)) !important;
            border: 1.5px solid rgba(255,255,255,0.5) !important;
            box-shadow: 0 4px 24px rgba(100,180,180,0.2) !important;
            border-radius: 16px !important;
            padding: 20px 40px !important;
            display: flex !important;
            justify-content: space-around !important;
            align-items: center !important;
            margin-bottom: 24px !important;
            margin-top: 38px !important;
            backdrop-filter: blur(12px) !important;
        }
        div.score-bar div.score-item {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #5b4fcf !important;
        }
        div.score-bar div.score-item span.score-val {
            font-size: 28px !important;
            font-weight: 900 !important;
            color: #7c3aed !important;
            -webkit-text-fill-color: #7c3aed !important;
            background: none !important;
        }
        div.game-msg {
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

            # Color buttons
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

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
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

        st.markdown("""<style>.stApp{background:linear-gradient(135deg,#f0f4ff 0%,#faf5ff 50%,#fce7f3 100%) !important;}.play-again-result button{background:linear-gradient(135deg,#667eea,#764ba2) !important;color:white !important;font-weight:700 !important;font-size:16px !important;padding:12px 0 !important;border-radius:50px !important;border:2px solid rgba(255,255,255,0.3) !important;box-shadow:0 8px 24px rgba(102,126,234,0.4) !important;transition:all 0.3s ease !important;width:100% !important;}.play-again-result button:hover{transform:translateY(-3px) !important;box-shadow:0 12px 32px rgba(102,126,234,0.55) !important;}</style>""", unsafe_allow_html=True)

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

        # ── ROW 1: Popup centered ──
        _, col, _ = st.columns([1, 1.4, 1])
        with col:
            st.markdown(f"""<div style="background:linear-gradient(145deg,#667eea 0%,#764ba2 40%,#f093fb 100%);border-radius:24px;padding:32px 28px 28px;text-align:center;box-shadow:0 16px 48px rgba(102,126,234,0.4);border:1px solid rgba(255,255,255,0.2);position:relative;overflow:hidden;"><div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;background:rgba(255,255,255,0.08);border-radius:50%;"></div><div style="position:absolute;bottom:-20px;left:-20px;width:80px;height:80px;background:rgba(255,255,255,0.06);border-radius:50%;"></div><div style="font-size:52px;margin-bottom:10px;position:relative;z-index:1;">{emoji}</div><div style="font-size:30px;font-weight:900;color:white;margin-bottom:24px;text-shadow:0 2px 12px rgba(0,0,0,0.2);position:relative;z-index:1;">{title}</div><div style="display:flex;justify-content:center;gap:14px;margin-bottom:18px;position:relative;z-index:1;"><div style="background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);border-radius:16px;padding:16px 24px;flex:1;border:1px solid rgba(255,255,255,0.3);"><div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.8);margin-bottom:8px;text-transform:uppercase;letter-spacing:1.5px;">🎯 Level</div><div style="font-size:38px;font-weight:900;color:white;text-shadow:0 2px 8px rgba(0,0,0,0.2);">{level}</div></div><div style="background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);border-radius:16px;padding:16px 24px;flex:1;border:1px solid rgba(255,255,255,0.3);"><div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.8);margin-bottom:8px;text-transform:uppercase;letter-spacing:1.5px;">⭐ Score</div><div style="font-size:38px;font-weight:900;color:white;text-shadow:0 2px 8px rgba(0,0,0,0.2);">{score}</div></div></div><div style="font-size:13px;color:rgba(255,255,255,0.85);line-height:1.7;background:rgba(255,255,255,0.12);border-radius:12px;padding:12px 16px;position:relative;z-index:1;">Every game is practice for mindfulness<br>Breathe deeply and try again</div></div>""", unsafe_allow_html=True)

        # ── GAP between popup and button ──
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        # ── ROW 2: Button centered — completely separate row ──
        _, btn_col, _ = st.columns([1.5, 1, 1.5])
        with btn_col:
            st.markdown('<div class="play-again-result">', unsafe_allow_html=True)
            if st.button("🎮 Play Again", key="btn_again", use_container_width=True):
                reset_game()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── ROUTER ──
    screen = st.session_state.game_screen
    if   screen == "home":      show_home()
    elif screen == "countdown": show_countdown()
    elif screen == "game":      show_game()
    elif screen == "result":    show_result()


def show_aesthetic_game_selector():
    show_calm_colors_game();