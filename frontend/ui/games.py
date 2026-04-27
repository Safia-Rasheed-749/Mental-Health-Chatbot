# ui/games.py
import streamlit as st
import time
import random
from layout_utils import apply_clean_layout

def show_calm_colors_game():
    apply_clean_layout(hide_header_completely=True)

    # ===== SAFE CSS =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }

        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== TITLE =====
    st.markdown("""
    <div style="text-align:center;">
        <h1>🎨 Calm Colors Game</h1>
        <p>🧘 Watch the sequence & repeat it</p>
    </div>
    """, unsafe_allow_html=True)

    # ===== SESSION STATE =====
    if 'memory_game_initialized' not in st.session_state:
        st.session_state.memory_game_initialized = True
        st.session_state.game_active = False
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False
        st.session_state.game_message = "Click Start Game"

    colors = [
        {"name": "Blue", "color": "#4A90E2", "emoji": "💙"},
        {"name": "Green", "color": "#34D399", "emoji": "💚"},
        {"name": "Purple", "color": "#A855F7", "emoji": "💜"},
        {"name": "Orange", "color": "#ff8c00", "emoji": "🧡"},
    ]

    # ===== FUNCTIONS =====
    def start_game():
        st.session_state.game_active = True
        st.session_state.game_sequence = [random.randint(0, 3)]
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.waiting_for_player = False
        st.session_state.is_playing_sequence = True

    def reset_game():
        st.session_state.game_active = False
        st.session_state.game_sequence = []
        st.session_state.player_index = 0
        st.session_state.game_level = 1
        st.session_state.game_score = 0
        st.session_state.is_playing_sequence = False
        st.session_state.waiting_for_player = False

    def handle_click(i):
        if not st.session_state.game_active:
            return

        expected = st.session_state.game_sequence[st.session_state.player_index]

        if i == expected:
            st.session_state.player_index += 1

            if st.session_state.player_index == len(st.session_state.game_sequence):
                st.session_state.game_score += 10
                st.session_state.game_level += 1
                st.session_state.player_index = 0

                new_seq = [random.randint(0, 3) for _ in range(st.session_state.game_level)]
                st.session_state.game_sequence = new_seq
                st.session_state.waiting_for_player = False
                st.session_state.is_playing_sequence = True
        else:
            reset_game()

    # ===== BUTTONS =====
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if not st.session_state.game_active:
            if st.button("🎮 Start Game", use_container_width=True):
                start_game()
                st.rerun()
        else:
            if st.button("🔄 Reset", use_container_width=True):
                reset_game()
                st.rerun()

    # ===== COLOR BUTTONS =====
    if st.session_state.game_active:
        st.markdown("### 🎨 Choose Colors")

        cols = st.columns(4)

        for i in range(4):
            with cols[i]:
                if st.button(f"{colors[i]['emoji']} {colors[i]['name']}", key=i):
                    handle_click(i)
                    st.rerun()

    # ===== SCORE =====
    if st.session_state.game_active:
        st.markdown(f"""
        <div style="text-align:center;">
            <h4>Level: {st.session_state.game_level} | Score: {st.session_state.game_score}</h4>
        </div>
        """, unsafe_allow_html=True)


def show_aesthetic_game_selector():
    show_calm_colors_game()