# ui/games.py
import streamlit as st
import time
import random
from layout_utils import apply_clean_layout

def show_calm_colors_game():
    apply_clean_layout(hide_header_completely=True)
    st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True) 
    
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
    /* Button spacing improvement */
    div[data-testid="column"] button {
        margin: 8px 0 !important;
        padding: 25px 10px !important;
        font-size: 20px !important;
        transition: transform 0.2s;
    }
    div[data-testid="column"] button:hover {
        transform: scale(1.02);
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
            st.session_state.player_index += 1
            
            if st.session_state.player_index == len(st.session_state.game_sequence):
                round_points = 10 * st.session_state.game_level
                st.session_state.game_score += round_points
                st.session_state.game_level += 1
                st.session_state.player_index = 0
                st.session_state.waiting_for_player = False
                st.session_state.is_playing_sequence = True
                
                # Generate completely new sequence for next round
                new_sequence_length = st.session_state.game_level
                new_sequence = []
                for _ in range(new_sequence_length):
                    new_color = random.randint(0, 3)
                    new_sequence.append(new_color)
                st.session_state.game_sequence = new_sequence
                
                st.session_state.game_message = f"✅ Round complete! +{round_points} points! Watch next sequence..."
        else:
            end_game()
    
    # ========== UI ==========
    # st.markdown('<div class="game-wrapper">', unsafe_allow_html=True)
    
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
    
    # ========== NEW AND IMPROVED SEQUENCE DISPLAY ==========
    if st.session_state.game_active and st.session_state.is_playing_sequence:
        sequence = st.session_state.game_sequence
        if sequence:
            # Show header with progress
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0;">
                <div style="background: #F0F9FF; padding: 10px; border-radius: 15px;">
                    🎵 <strong>Watching Sequence</strong> - Length: {len(sequence)} 🎵
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create horizontal chips layout
            cols = st.columns(len(sequence))
            
            # Animate each chip one by one
            for idx, color_idx in enumerate(sequence):
                color_data = colors[color_idx]
                
                with cols[idx]:
                    # Create placeholder for this chip
                    chip_placeholder = st.empty()
                    
                    # Show chip with animation
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
                            0% {{ 
                                transform: scale(0.9);
                                opacity: 0.5;
                            }}
                            50% {{
                                transform: scale(1.05);
                                opacity: 1;
                            }}
                            100% {{ 
                                transform: scale(1);
                                opacity: 1;
                            }}
                        }}
                        </style>
                    """, unsafe_allow_html=True)
                    
                    # Wait before moving to next chip
                    time.sleep(0.8)
                    
                    # Dim the chip after showing
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
            
            # Give a moment to review
            time.sleep(0.5)
            
            # Show transition message
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: #E0F2FE; border-radius: 15px; margin: 10px 0;">
                🎯 Sequence completed! Your turn now! 🎯
            </div>
            """, unsafe_allow_html=True)
            
            # Switch to player's turn
            st.session_state.is_playing_sequence = False
            st.session_state.waiting_for_player = True
            st.session_state.game_message = f"🎵 Your turn! Repeat the sequence of {len(sequence)} colors... 🎵"
            st.rerun()
    
    # ========== GAME PLAY AREA ==========
    if st.session_state.game_active:
        if st.session_state.waiting_for_player:
            st.markdown("""
                <div style="text-align: center; padding: 15px; background: #F0FDF4; border-radius: 15px; margin: 10px 0;">
                    <div style="font-size: 28px;">🎯</div>
                    <div style="color: #166534; font-weight: bold;">Your turn! Click the colors in order...</div>
                </div>
            """, unsafe_allow_html=True)
            
            total = len(st.session_state.game_sequence)
            progress = st.session_state.player_index
            if total > 0:
                st.progress(progress / total)
                st.caption(f"🎯 Progress: {progress} / {total}")
        
        st.markdown("### 🎨 Click colors:")
        
        # Color buttons in 2x2 grid with improved spacing
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            if st.button(f"{colors[0]['emoji']} {colors[0]['name']}", key="color_blue", use_container_width=True):
                handle_player_move(0)
                st.rerun()
        
        with row1_col2:
            if st.button(f"{colors[1]['emoji']} {colors[1]['name']}", key="color_green", use_container_width=True):
                handle_player_move(1)
                st.rerun()
        
        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            if st.button(f"{colors[2]['emoji']} {colors[2]['name']}", key="color_purple", use_container_width=True):
                handle_player_move(2)
                st.rerun()
        
        with row2_col2:
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
        2. **Watch carefully** as colored squares flash in a sequence horizontally
        3. **Repeat** the sequence by clicking the colors in the same order
        4. **Level Up** after each correct round (completely new sequence each time!)
        5. **Game Over** if you click the wrong color
        
        🧘 **Mindfulness Tip:** Breathe in while watching the sequence, breathe out while repeating it.
        """)
    
    # st.markdown('</div>', unsafe_allow_html=True)


def show_aesthetic_game_selector():
    """Main game selector"""
    show_calm_colors_game()