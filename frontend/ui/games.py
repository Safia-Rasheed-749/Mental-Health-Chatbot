# ui/games.py
import streamlit as st
import time
import random
from layout_utils import apply_clean_layout

def show_calm_colors_game():
    apply_clean_layout(hide_header_completely=True)
    
<<<<<<< Updated upstream
    # ========== CSS STYLING ==========
=======
     # ===== CSS (SAFE - NO NAVBAR BREAK) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Game styling
>>>>>>> Stashed changes
    st.markdown("""
    <style>
    /* Main container - center everything */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Center all columns */
    .row-widget.stHorizontal {
        justify-content: center !important;
    }
    
    /* Center the score panel */
    .score-panel {
        background: linear-gradient(135deg, #E0F2FE, #F0F9FF);
        padding: 15px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        width: 100%;
    }
    
    /* Center message area */
    .message-area {
        background: #F8FAFC;
        padding: 12px;
        border-radius: 15px;
        text-align: center;
        margin: 15px auto;
        color: #4A90E2;
        font-weight: 500;
        width: 100%;
    }
    
    /* Game title center */
    .game-title {
        text-align: center;
        margin-bottom: 30px;
        width: 100%;
        display: block;
    }

    .game-title h1 {
        background: linear-gradient(135deg, #A7C7E7 0%, #4A90E2 100%);        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        margin: 0;
        text-align: center;
        width: 100%;
    }

    .game-title p {
        color: #475569;
        margin: 10px 0 0 0;
        text-align: center;
        width: 100%;
        font-size: 1.1rem;
    }
    
    /* Center and style buttons */
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
    }
    
    div[data-testid="column"] button {
        margin: 8px auto !important;
        padding: 25px 20px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        transition: transform 0.2s;
        width: 90% !important;
        min-width: 150px;
    }
    
    div[data-testid="column"] button:hover {
        transform: scale(1.02);
    }
    
    /* Center the button container */
    .stButton {
        text-align: center;
    }
    
    /* Center the progress bar */
    .stProgress {
        width: 80%;
        margin: 0 auto;
    }
    
    /* Center expander */
    .streamlit-expander {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ========== INITIALIZE SESSION STATE ==========
    if 'memory_game_initialized' not in st.session_state:
        st.session_state.memory_game_initialized = True
        st.session_state.game_active = False
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
        st.session_state.game_message = "✨ Click 'Start Game' to begin your mindfulness journey ✨"
        st.session_state.quit_game_called = False
    
    # Color options
    colors = [
        {"name": "Blue", "color": "#4A90E2", "emoji": "💙", "id": 0},
        {"name": "Green", "color": "#34D399", "emoji": "💚", "id": 1},
        {"name": "Purple", "color": "#A855F7", "emoji": "💜", "id": 2},
        {"name": "Orange", "color": "#ff8c00", "emoji": "🧡", "id": 3},
    ]
    
    # ========== FUNCTIONS ==========
    def start_new_game():
        st.session_state.game_active = True
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = True
        st.session_state.waiting_for_player = False
        st.session_state.quit_game_called = False
        first_color = random.randint(0, 3)
        st.session_state.game_sequence.append(first_color)
        st.session_state.game_message = "🎵 Watch the sequence carefully... 🎵"
    
    def end_game(quit_game=False):
        """End the game - either by quitting or losing"""
        if quit_game:
            st.session_state.quit_game_called = True
            st.session_state.game_message = f"👋 You quit the game|Level:{st.session_state.game_level}|Score:{st.session_state.game_score}"
        else:
            st.session_state.quit_game_called = False
            st.session_state.game_message = f"💙 Game Over! You reached Level {st.session_state.game_level}"
        
        st.session_state.game_active = False
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
    
    def reset_game():
        st.session_state.game_active = False
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
        st.session_state.quit_game_called = False
        st.session_state.game_message = "✨ Click 'Start Game' to begin your mindfulness journey ✨"
    
    def handle_player_move(color_id):
        if not st.session_state.game_active:
            st.toast("Start a game first!", icon="🎮")
            return
        
        if not st.session_state.waiting_for_player:
            st.toast("Wait for your turn!", icon="⏳")
            return
        
        expected_color = st.session_state.game_sequence[st.session_state.player_index]
        
        if color_id == expected_color:
            st.session_state.player_index += 1
            
            if st.session_state.player_index == len(st.session_state.game_sequence):
                round_points = 10 * st.session_state.game_level
                st.session_state.game_score += round_points
                st.session_state.game_level += 1
                st.session_state.player_index = 0
                st.session_state.waiting_for_player = False
                st.session_state.is_playing_sequence = True
                
                new_sequence_length = st.session_state.game_level
                new_sequence = []
                for _ in range(new_sequence_length):
                    new_color = random.randint(0, 3)
                    new_sequence.append(new_color)
                st.session_state.game_sequence = new_sequence
                
                st.session_state.game_message = f"✅ Round complete! +{round_points} points! Watch next sequence..."
        else:
            end_game(quit_game=False)
    
    # ========== MAIN CONTAINER ==========
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Game Title - Centered
    st.markdown("""
    <div class="game-title">
        <h1>🎨 Calm Colors Game</h1>
        <p>🧘 Watch the sequence & repeat it to calm your mind</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Score Panel - Centered
    if st.session_state.game_active:
        st.markdown(f"""
        <div class="score-panel">
            <div style="font-size: 18px; font-weight: bold; color: #1e293b;">
                🔷 Level: {st.session_state.game_level} &nbsp;&nbsp;|&nbsp;&nbsp;
                🏆 Score: {st.session_state.game_score} &nbsp;&nbsp;|&nbsp;&nbsp;
                📊 Sequence Length: {len(st.session_state.game_sequence)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="score-panel">
            <div style="font-size: 18px; font-weight: bold; color: #1e293b;">
                🎮 Ready to play?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Message Area - Centered
    display_message = st.session_state.game_message
    if "|" in display_message:
        display_message = display_message.split("|")[0]
    st.markdown(f'<div class="message-area">{display_message}</div>', unsafe_allow_html=True)
    
    # ========== START / END BUTTONS - Centered ==========
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.game_active:
            if st.button("🎮 Start New Game", use_container_width=True):
                start_new_game()
                st.rerun()
        else:
            if st.button("🔄 End Game", use_container_width=True):
                end_game(quit_game=True)
                st.rerun()
    
    # ========== SEQUENCE DISPLAY ==========
    if st.session_state.game_active and st.session_state.is_playing_sequence:
        sequence = st.session_state.game_sequence
        if sequence:
            st.markdown(f"""
            <div style="text-align: center; margin: 10px auto; width: 100%;">
                <div style="background: #F0F9FF; padding: 10px; border-radius: 15px; display: inline-block;">
                    🎵 <strong>Watching Sequence</strong> - Length: {len(sequence)} 🎵
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(len(sequence))
            
            for idx, color_idx in enumerate(sequence):
                color_data = colors[color_idx]
                
                with cols[idx]:
                    chip_placeholder = st.empty()
                    
                    chip_placeholder.markdown(f"""
                        <div style="
                            background: {color_data['color']};
                            padding: 20px 10px;
                            border-radius: 15px;
                            text-align: center;
                            margin: 5px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            animation: glow 0.6s ease-in-out;
                        ">
                            <div style="font-size: 48px;">{color_data['emoji']}</div>
                            <div style="color: white; font-size: 14px; font-weight: bold; margin-top: 5px;">
                                {color_data['name']}
                            </div>
                        </div>
                        <style>
                        @keyframes glow {{
                            0% {{ transform: scale(0.9); opacity: 0.5; }}
                            50% {{ transform: scale(1.05); opacity: 1; }}
                            100% {{ transform: scale(1); opacity: 1; }}
                        }}
                        </style>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(0.8)
                    
                    chip_placeholder.markdown(f"""
                        <div style="
                            background: {color_data['color']};
                            padding: 20px 10px;
                            border-radius: 15px;
                            text-align: center;
                            margin: 5px;
                            opacity: 0.6;
                        ">
                            <div style="font-size: 48px;">{color_data['emoji']}</div>
                            <div style="color: white; font-size: 14px; font-weight: bold; margin-top: 5px;">
                                {color_data['name']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(0.2)
            
            time.sleep(0.5)
            
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: #E0F2FE; border-radius: 15px; margin: 10px auto; width: 80%;">
                🎯 Sequence completed! Your turn now! 🎯
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.is_playing_sequence = False
            st.session_state.waiting_for_player = True
            st.session_state.game_message = f"🎵 Your turn! Repeat the sequence of {len(sequence)} colors... 🎵"
            st.rerun()
    
    # ========== GAME PLAY AREA ==========
    if st.session_state.game_active:
        if st.session_state.waiting_for_player:
            st.markdown("""
                <div style="text-align: center; padding: 15px; background: #F0FDF4; border-radius: 15px; margin: 10px auto; width: 80%;">
                    <div style="font-size: 28px;">🎯</div>
                    <div style="color: #166534; font-weight: bold;">Your turn! Click the colors in order...</div>
                </div>
            """, unsafe_allow_html=True)
            
            total = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.caption(f"🎯 Progress: {progress} / {total}")
        
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎨 Click colors:</h3>", unsafe_allow_html=True)

        # Row 1 with gap
        col1, spacer1, col2 = st.columns([1, 0.1, 1])
        with col1:
            if st.button(f"{colors[0]['emoji']} {colors[0]['name']}", 
                        key="color_blue", 
                        use_container_width=True):
                handle_player_move(0)
                st.rerun()

        with col2:
            if st.button(f"{colors[1]['emoji']} {colors[1]['name']}", 
                        key="color_green", 
                        use_container_width=True):
                handle_player_move(1)
                st.rerun()

        # Space between rows (20px gap)
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

        # Row 2 with gap
        col3, spacer2, col4 = st.columns([1, 0.1, 1])
        with col3:
            if st.button(f"{colors[2]['emoji']} {colors[2]['name']}", 
                        key="color_purple", 
                        use_container_width=True):
                handle_player_move(2)
                st.rerun()

        with col4:
            if st.button(f"{colors[3]['emoji']} {colors[3]['name']}", 
                        key="color_orange", 
                        use_container_width=True):
                handle_player_move(3)
                st.rerun()
    
    # ========== GAME OVER / QUIT SCREEN ==========
    if not st.session_state.game_active:
        if "quit the game" in st.session_state.game_message.lower():
            if "|" in st.session_state.game_message:
                parts = st.session_state.game_message.split("|")
                level_part = [p for p in parts if "Level:" in p][0] if any("Level:" in p for p in parts) else "Level:1"
                score_part = [p for p in parts if "Score:" in p][0] if any("Score:" in p for p in parts) else "Score:0"
                current_level = int(level_part.split(":")[1])
                current_score = int(score_part.split(":")[1])
            else:
                current_level = st.session_state.game_level
                current_score = st.session_state.game_score
            
            st.markdown("---")
            
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #E0F2FE, #F0F9FF); 
                    padding: 20px; 
                    border-radius: 15px; 
                    text-align: center;
                    margin: 10px 0 40px 0;                ">
                    <div style="font-size: 48px; margin-bottom: 10px;">👋</div>
                    <h3 style="color: #1e293b; margin: 0 0 10px 0;">Game Ended</h3>
                    <div style="
                        background: white; 
                        padding: 12px; 
                        border-radius: 10px; 
                        margin: 10px 0;
                    ">
                        <p style="font-size: 16px; color: #475569; margin: 5px 0;">
                            🏆 <strong>Level:</strong> {current_level}
                        </p>
                        <p style="font-size: 18px; color: #4A90E2; font-weight: bold; margin: 5px 0;">
                            ⭐ <strong>Score:</strong> {current_score}
                        </p>
                    </div>
                    <p style="color: #475569; font-size: 12px; margin: 5px 0 0 0;">
                        ✨ Come back anytime ✨
                    </p>
                </div>
                """, unsafe_allow_html=True)
                col_left, col_center, col_right = st.columns([1, 2, 1])
                with col_center:
                    if st.button("🎮 Play New Game", use_container_width=True):
                        reset_game()
                        start_new_game()
                        st.rerun()
    
    
                
                
        
        elif "Game Over" in st.session_state.game_message:
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #E0F2FE, #F0F9FF); 
                    padding: 20px; 
                    border-radius: 15px; 
                    text-align: center;
                    margin: 10px 0 40px 0;                ">
                    <div style="font-size: 48px; margin-bottom: 10px;">💙</div>
                    <h3 style="color: #1e293b; margin: 0 0 10px 0;">Game Over</h3>
                    <div style="
                        background: white; 
                        padding: 12px; 
                        border-radius: 10px; 
                        margin: 7px 0;
                    ">
                        <p style="font-size: 16px; color: #475569; margin: 5px 0;">
                            🎯 <strong>Level:</strong> {st.session_state.game_level}
                        </p>
                        <p style="font-size: 18px; color: #4A90E2; font-weight: bold; margin: 5px 0;">
                            ⭐ <strong>Score:</strong> {st.session_state.game_score}
                        </p>
                    </div>
                    <p style="color: #475569; font-size: 15px ; font-weight: bold; margin: 5px 0 0 0;">
                        ✨ Every game is practice ✨
                    </p>
                    <p style="color: #475569; font-size: 14px; font-weight: bold; margin: 5px 0 0 0;">
                        💡 Watch carefully & breathe deeply
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    
                
                if st.button("🎮 Try Again", use_container_width=True):
                    reset_game()
                    start_new_game()
                    st.rerun()
    
    # Instructions
    # ========== SPACE BEFORE EXPANDER ==========
    st.markdown('<div style="margin: 30px 0 10px 0;"></div>', unsafe_allow_html=True)

    # Instructions
    with st.expander("📖 How to Play"):
        st.markdown("""
        <div style="padding: 5px 0;">
            <strong>🎮 Game Rules:</strong><br><br>
            1. Click <strong>Start New Game</strong> to begin<br><br>
            2. <strong>Watch carefully</strong> as colored squares flash in a sequence horizontally<br><br>
            3. <strong>Repeat</strong> the sequence by clicking the colors in the same order<br><br>
            4. <strong>Level Up</strong> after each correct round (completely new sequence each time!)<br><br>
            5. <strong>Game Over</strong> if you click the wrong color<br><br>
            <hr>
            🧘 <strong>Mindfulness Tip:</strong> Breathe in while watching the sequence, breathe out while repeating it.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def show_aesthetic_game_selector():
    """Main game selector"""
    show_calm_colors_game()