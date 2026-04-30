import streamlit as st
import time
import random


def show_calm_colors_game():
    # app.py already calls apply_clean_layout + render_navbar before this.
    # Do NOT call apply_clean_layout here — it shifts the navbar down.

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    header, footer, .stDeployButton { display: none !important; }

    html, body, .stApp {
        font-family: 'Inter', sans-serif !important;
    }

    .block-container {
        padding-top: 1.8rem !important;
    }

    /* ── SCORE BAR ── */
    .score-bar {
        background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(248,250,252,0.97));
        padding: 16px 40px;
        display: flex; justify-content: space-around; align-items: center;
        box-shadow: 0 4px 20px rgba(99,102,241,0.18);
        border-bottom: 4px solid #8b5cf6;
    }
    .score-item { font-size: 18px; font-weight: 700; color: #1e293b; }
    .score-val  { font-size: 26px; font-weight: 900; color: #6366f1; }

    /* ── GAME MESSAGE ── */
    .game-msg {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15));
        padding: 18px 36px; border-radius: 18px;
        font-size: 18px; font-weight: 600; color: #4338ca;
        margin: 30px auto; border: 2px solid rgba(99,102,241,0.28);
        max-width: 600px; text-align: center;
    }

    /* ── SEQUENCE CHIP ── */
    .seq-chip {
        display: inline-block;
        padding: 28px 36px; border-radius: 18px;
        margin: 8px; font-size: 52px; color: white;
        box-shadow: 0 8px 28px rgba(0,0,0,0.22);
        animation: chipIn 0.5s ease;
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
         margin-top: 20px; !important
        padding-left: 28px; !important
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
    .play-again-wrap .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important; font-weight: 800 !important;
        font-size: 18px !important; padding: 14px 44px !important;
        border-radius: 50px !important; border: none !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.45) !important;
        width: auto !important;
         margin-top: 20px; !important
        padding-left: 28px; !important
    }
    .play-again-wrap .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(99,102,241,0.55) !important;
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
                st.session_state.game_message = f"✅ Perfect! +{pts} points!"
        else:
            end_game()

    # ── SCREEN: HOME ──
    def show_home():
        # Banner — smaller, with top margin so it sits below navbar
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 55%, #f093fb 100%);
            border-radius: 20px;
            margin: 28px 16px 0 16px;
            padding: 36px 20px 44px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(102,126,234,0.35);
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
                    <div style="font-size:26px;margin-bottom:8px;">🎯</div>
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
                <span style="font-size:14px;font-weight:600;color:#1c1917;margin-left:8px;">
                    Breathe IN while watching &nbsp;·&nbsp; Breathe OUT while repeating
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SCREEN: COUNTDOWN ──
    def show_countdown():
        placeholder = st.empty()
        for num, hint in [("3","Take a deep breath in..."),
                          ("2","Focus your mind..."),
                          ("1","Get ready..."),
                          ("GO!","Let's begin!")]:
            placeholder.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4A90E2 0%, #A855F7 100%);
                border-radius: 20px;
                margin: 12px 16px;
                padding: 80px 20px;
                text-align: center;
                color: white;
                box-shadow: 0 8px 32px rgba(74,144,226,0.35);
            ">
                <div style="font-size:130px;font-weight:900;
                            text-shadow:0 8px 30px rgba(0,0,0,0.4);
                            animation:chipIn 0.8s ease;line-height:1;">{num}</div>
                <div style="font-size:20px;margin-top:24px;opacity:0.85;">{hint}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        start_game()
        st.session_state.game_screen = "game"
        st.rerun()

    # ── SCREEN: GAME ──
    def show_game():
        st.markdown(f"""
        <div class="score-bar">
            <div class="score-item">🎯 Level  <span class="score-val">{st.session_state.game_level}</span></div>
            <div class="score-item">🏆 Score  <span class="score-val">{st.session_state.game_score}</span></div>
            <div class="score-item">📊 Length <span class="score-val">{len(st.session_state.game_sequence)}</span></div>
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
                '<div class="game-msg">🎯 Your turn! Click the colors in order...</div>',
                unsafe_allow_html=True
            )
            total    = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.markdown(
                    f"<p style='text-align:center;color:#64748b;font-weight:600;margin:8px 0 20px;'>"
                    f"Progress: {progress} / {total}</p>",
                    unsafe_allow_html=True
                )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"{colors[0]['emoji']}  {colors[0]['name']}", key="color_blue",  use_container_width=True):
                    handle_move(0); st.rerun()
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                if st.button(f"{colors[2]['emoji']}  {colors[2]['name']}", key="color_purple", use_container_width=True):
                    handle_move(2); st.rerun()
            with col2:
                if st.button(f"{colors[1]['emoji']}  {colors[1]['name']}", key="color_green",  use_container_width=True):
                    handle_move(1); st.rerun()
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                if st.button(f"{colors[3]['emoji']}  {colors[3]['name']}", key="color_orange", use_container_width=True):
                    handle_move(3); st.rerun()

            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1.2, 1, 1.2])
            with c2:
                if st.button("🔄  End Game", key="btn_end"):
                    end_game(); st.rerun()

    # ── SCREEN: RESULT ──
    def show_result():
        import streamlit.components.v1 as components
        level = st.session_state.game_level
        score = st.session_state.game_score
        is_win = score > 50
        emoji  = "🎉" if is_win else "💙"
        title  = "Amazing!" if is_win else "Game Over"
        bg     = "linear-gradient(135deg,#667eea 0%,#764ba2 60%,#f093fb 100%)" if is_win else \
                 "linear-gradient(135deg,#4a7fd4 0%,#764ba2 100%)"
        badge  = "#fbbf24" if is_win else "#e0d7ff"

        # Use components.html — bypasses Streamlit's Markdown parser completely
        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
            * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }}
            body {{ background:transparent; padding: 20px 16px 0 16px; }}
            .card {{
                background: {bg};
                border-radius: 24px;
                padding: 36px 24px 32px;
                text-align: center;
                color: white;
                box-shadow: 0 12px 40px rgba(102,126,234,0.40);
            }}
            .emoji  {{ font-size:56px; margin-bottom:8px; }}
            .title  {{ font-size:34px; font-weight:900; margin-bottom:24px;
                       text-shadow:0 3px 12px rgba(0,0,0,0.25); }}
            .stats  {{ display:flex; justify-content:center; gap:16px;
                       flex-wrap:wrap; margin-bottom:22px; }}
            .stat-box {{
                background: rgba(255,255,255,0.18);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255,255,255,0.32);
                border-radius: 18px;
                padding: 18px 28px;
                min-width: 120px;
            }}
            .stat-label {{
                font-size: 11px; font-weight: 700; opacity: 0.85;
                text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;
            }}
            .stat-val {{
                font-size: 48px; font-weight: 900; line-height: 1;
                color: {badge};
            }}
            .tip {{
                font-size: 13px; opacity: 0.88; line-height: 1.8;
            }}
        </style>
        </head>
        <body>
        <div class="card">
            <div class="emoji">{emoji}</div>
            <div class="title">{title}</div>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">🎯 Level Reached</div>
                    <div class="stat-val">{level}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">⭐ Final Score</div>
                    <div class="stat-val">{score}</div>
                </div>
            </div>
            <div class="tip">
                ✨ Every game is practice for mindfulness ✨<br>
                💡 Breathe deeply and try again
            </div>
        </div>
        </body>
        </html>
        """, height=340)

        # Play Again button below the card
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c2:
            st.markdown('<div class="play-again-wrap">', unsafe_allow_html=True)
            if st.button("🔄  Play Again", key="btn_again"):
                reset_game(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── ROUTER ──
    screen = st.session_state.game_screen
    if   screen == "home":      show_home()
    elif screen == "countdown": show_countdown()
    elif screen == "game":      show_game()
    elif screen == "result":    show_result()


def show_aesthetic_game_selector():
    show_calm_colors_game()
