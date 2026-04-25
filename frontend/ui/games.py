# ui/games.py
import streamlit as st
import time
import random

def show_calm_colors_game():
    """
    Memory & Focus Game - Calm Colors Edition
    Fully working Simon Says style game
    """
    
    # Game styling
    st.markdown("""
    <style>
    .game-wrapper {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
        background: white;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    .score-panel {
        background: linear-gradient(135deg, #E0F2FE, #F0F9FF);
        padding: 15px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
    }
    .message-area {
        background: #F8FAFC;
        padding: 12px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        color: #4A90E2;
        font-weight: 500;
    }
    .game-title {
        text-align: center;
        margin-bottom: 20px;
    }
    .game-title h1 {
        color: #1e293b;
        font-size: 2rem;
        margin: 0;
    }
    .game-title p {
        color: #475569;
        margin: 5px 0 0 0;
    }
    .color-button {
        transition: all 0.2s ease;
    }
    .color-button:active {
        transform: scale(0.95);
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
    
    # Color options
    colors = [
        {"name": "Blue", "color": "#4A90E2", "emoji": "💙", "id": 0},
        {"name": "Green", "color": "#34D399", "emoji": "💚", "id": 1},
        {"name": "Purple", "color": "#A855F7", "emoji": "💜", "id": 2},
        {"name": "Orange", "color": "#FBBF24", "emoji": "🧡", "id": 3},
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
        # Add first random color
        first_color = random.randint(0, 3)
        st.session_state.game_sequence.append(first_color)
        st.session_state.game_message = "🎵 Watch the sequence carefully... 🎵"
    
    def end_game():
        st.session_state.game_active = False
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
        st.session_state.game_message = f"💙 Game Over! You reached Level {st.session_state.game_level}"
    
    def reset_game():
        st.session_state.game_active = False
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
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
            # Correct move
            st.session_state.player_index += 1
            
            if st.session_state.player_index == len(st.session_state.game_sequence):
                # Round completed successfully
                round_points = 10 * st.session_state.game_level
                st.session_state.game_score += round_points
                st.session_state.game_level += 1
                st.session_state.player_index = 0
                st.session_state.waiting_for_player = False
                st.session_state.is_playing_sequence = True
                
                # Add new color for next round
                new_color = random.randint(0, 3)
                st.session_state.game_sequence.append(new_color)
                
                st.session_state.game_message = f"✅ Round complete! +{round_points} points! Watch next sequence..."
        else:
            # Wrong move - Game Over
            end_game()
    
    # ========== UI ==========
    st.markdown('<div class="game-wrapper">', unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <div class="game-title">
        <h1>🎨 Calm Colors</h1>
        <p>🧘 Watch the sequence & repeat it to calm your mind</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Score Panel
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
    
    # Message Area
    st.markdown(f'<div class="message-area">{st.session_state.game_message}</div>', unsafe_allow_html=True)
    
    # ========== START / END BUTTONS ==========
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.game_active:
            if st.button("🎮 Start New Game", use_container_width=True):
                start_new_game()
                st.rerun()
        else:
            if st.button("🔄 End Game", use_container_width=True):
                reset_game()
                st.rerun()
    
    # ========== SHOW SEQUENCE (Auto-play) ==========
    if st.session_state.game_active and st.session_state.is_playing_sequence:
        sequence = st.session_state.game_sequence
        if sequence:
            st.info(f"🎵 Watching sequence length: {len(sequence)}...")
            
            # Create placeholder for flashing colors
            flash_placeholder = st.empty()
            
            for color_idx in sequence:
                color_data = colors[color_idx]
                flash_placeholder.markdown(f"""
                    <div style="
                        background-color: {color_data['color']};
                        padding: 60px;
                        border-radius: 30px;
                        text-align: center;
                        margin: 20px 0;
                        animation: pulse 0.5s ease-in-out;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    ">
                        <div style="font-size: 64px;">{color_data['emoji']}</div>
                        <div style="color: white; font-size: 24px; font-weight: bold; margin-top: 10px;">
                            {color_data['name']}
                        </div>
                    </div>
                    <style>
                    @keyframes pulse {{
                        0% {{ transform: scale(0.8); opacity: 0.5; }}
                        100% {{ transform: scale(1); opacity: 1; }}
                    }}
                    </style>
                """, unsafe_allow_html=True)
                time.sleep(1)
                flash_placeholder.empty()
                time.sleep(0.4)
            
            flash_placeholder.empty()
            
            # Switch to player's turn
            st.session_state.is_playing_sequence = False
            st.session_state.waiting_for_player = True
            st.session_state.game_message = f"🎵 Your turn! Repeat the sequence of {len(sequence)} colors... 🎵"
            st.rerun()
    
    # ========== GAME PLAY AREA ==========
    if st.session_state.game_active:
        # Show waiting or playing status
        if st.session_state.waiting_for_player:
            st.markdown("""
                <div style="text-align: center; padding: 15px; background: #F0FDF4; border-radius: 15px; margin: 10px 0;">
                    <div style="font-size: 28px;">🎯</div>
                    <div style="color: #166534; font-weight: bold;">Your turn! Click the colors in order...</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show progress
            total = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.caption(f"🎯 Progress: {progress} / {total}")
        
        # Color buttons in 2x2 grid
        st.markdown("### 🎨 Click colors:")
        
        # Row 1
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # Blue button
            btn_style = f"""
                <div style="
                    background: linear-gradient(135deg, {colors[0]['color']}, {colors[0]['color']}dd);
                    padding: 30px;
                    border-radius: 20px;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    <div style="font-size: 48px;">{colors[0]['emoji']}</div>
                    <div style="color: white; font-size: 20px; font-weight: bold;">{colors[0]['name']}</div>
                </div>
            """
            if st.button(f"{colors[0]['emoji']} {colors[0]['name']}", key="color_blue", use_container_width=True):
                handle_player_move(0)
                st.rerun()
        
        with row1_col2:
            # Green button
            if st.button(f"{colors[1]['emoji']} {colors[1]['name']}", key="color_green", use_container_width=True):
                handle_player_move(1)
                st.rerun()
        
        # Row 2
        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            # Purple button
            if st.button(f"{colors[2]['emoji']} {colors[2]['name']}", key="color_purple", use_container_width=True):
                handle_player_move(2)
                st.rerun()
        
        with row2_col2:
            # Orange button
            if st.button(f"{colors[3]['emoji']} {colors[3]['name']}", key="color_orange", use_container_width=True):
                handle_player_move(3)
                st.rerun()
    
    # ========== GAME OVER SCREEN ==========
    if not st.session_state.game_active and st.session_state.game_message.startswith("💙 Game Over"):
        st.markdown(f"""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #E0F2FE, #F0F9FF); border-radius: 20px; margin-top: 20px;">
            <div style="font-size: 64px;">💙</div>
            <h2 style="color: #1e293b;">Game Over</h2>
            <p style="color: #475569; font-size: 18px;">You reached Level {st.session_state.game_level-1}</p>
            <p style="color: #4A90E2; font-size: 28px; font-weight: bold;">Final Score: {st.session_state.game_score}</p>
            <p style="color: #475569;">✨ Every game is practice for a calmer mind ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 Play Again", use_container_width=True):
            start_new_game()
            st.rerun()
    
    # Instructions
    with st.expander("📖 How to Play"):
        st.markdown("""
        **🎮 Game Rules:**
        1. Click **Start New Game** to begin
        2. **Watch carefully** as colored squares flash in a sequence
        3. **Repeat** the sequence by clicking the colors in the same order
        4. **Level Up** after each correct round (sequence gets longer)
        5. **Game Over** if you click the wrong color
        
        🧘 **Mindfulness Tip:** Breathe in while watching the sequence, breathe out while repeating it.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_aesthetic_game_selector():
    """Main game selector"""
    show_calm_colors_game()