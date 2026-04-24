# ui/games.py
import streamlit as st
import random
import time

def show_breathing_game():
    """Interactive breathing bubble game"""
    st.markdown("""
    <style>
    .breath-container {
        text-align: center;
        padding: 20px;
    }
    .bubble {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #4A90E2, #6B5B95);
        border-radius: 50%;
        margin: 40px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(74, 144, 226, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .bubble-text {
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    .instruction {
        color: #475569;
        font-size: 16px;
        margin: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="breath-container">', unsafe_allow_html=True)
    
    if 'breath_count' not in st.session_state:
        st.session_state.breath_count = 0
    if 'breathing' not in st.session_state:
        st.session_state.breathing = False
    
    st.markdown("""
        <div class="bubble" id="bubble">
            <div class="bubble-text">
                🌬️<br>Breathe
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="instruction">✨ Click the bubble to breathe deeply ✨</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🌬️ Take a Deep Breath", use_container_width=True):
            st.session_state.breath_count += 1
            st.balloons()
            st.success(f"🧘 Nice! You've taken {st.session_state.breath_count} mindful breaths!")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_mindful_catcher():
    """Catch calm thoughts, avoid stress"""
    st.markdown("""
    <style>
    .game-status {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px;
    }
    .game-container {
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'misses' not in st.session_state:
        st.session_state.misses = 0
    
    st.markdown(f"""
    <div class="game-status">
        🧘 Calm Thoughts: {st.session_state.score} &nbsp;&nbsp;&nbsp;
        ⚠️ Stress: {st.session_state.misses}/5
    </div>
    """, unsafe_allow_html=True)
    
    # Game grid
    cols = st.columns(3)
    
    items = [
        ("😊", "calm", "Happy Thought"),
        ("🌿", "calm", "Peaceful Moment"),
        ("🌸", "calm", "Gentle Breath"),
        ("⚠️", "stress", "Anxiety"),
        ("💭", "calm", "Quiet Mind"),
        ("❌", "stress", "Negative Loop"),
    ]
    random.shuffle(items)
    
    for i, (emoji, type_, name) in enumerate(items[:6]):
        with cols[i % 3]:
            if st.button(f"{emoji}\n{name}", key=f"catch_{i}", use_container_width=True):
                if type_ == "calm":
                    st.session_state.score += 10
                    st.toast(f"✨ +10 calm energy! ✨", icon="🧘")
                else:
                    st.session_state.misses += 1
                    st.toast(f"😔 -5 energy. Let it go...", icon="🌊")
                
                if st.session_state.misses >= 5:
                    st.error("💙 Take a break? Try the breathing exercise above!")
                    st.session_state.misses = 0
                st.rerun()
    
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.score = 0
        st.session_state.misses = 0
        st.rerun()


def show_slider_puzzle():
    """Relaxing puzzle game"""
    st.markdown("""
    <style>
    .puzzle-title {
        text-align: center;
        color: #4A90E2;
        font-size: 20px;
        margin: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="puzzle-title">🧩 Arrange the peaceful scene 🧩</div>', unsafe_allow_html=True)
    
    # Simple puzzle using columns
    pieces = [
        ("☁️", "Clouds"),
        ("🌞", "Sun"),
        ("🏔️", "Mountains"),
        ("🌊", "Ocean"),
        ("🌳", "Tree"),
        ("🌸", "Flower"),
    ]
    
    cols = st.columns(3)
    for i, (emoji, name) in enumerate(pieces):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #E0F2FE, #BAE6FD);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                margin: 10px;
                cursor: pointer;
            ">
                <div style="font-size: 48px;">{emoji}</div>
                <div style="color: #1e293b; font-size: 14px;">{name}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.info("💙 Peaceful scene coming together naturally... just like your calm mind")


def show_aesthetic_game_selector():
    """Main game selector for landing page"""
    st.markdown("""
    <style>
    .game-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #E0F2FE, #F0F9FF);
        border-radius: 30px;
        margin-bottom: 30px;
    }
    .game-header h2 {
        color: #1e293b;
        font-size: 2rem;
    }
    .game-header p {
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-header">
        <h2>🎮 Mindful Moments</h2>
        <p>Quick games to calm your mind and lift your spirit</p>
        <p style="font-size: 14px;">✨ No login required - play freely ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    game_options = {
        "🌬️ Breathing Bubble": "Deep breathing exercise - reduces anxiety",
        "🎯 Mindful Catcher": "Catch calm thoughts, avoid stress",
        "🧩 Peaceful Puzzle": "Arrange a serene nature scene"
    }
    
    selected_game = st.selectbox(
        "Choose your mindful game",
        list(game_options.keys()),
        format_func=lambda x: f"{x} - {game_options[x]}"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Start Game ✨", use_container_width=True):
            st.session_state.selected_game = selected_game
            st.rerun()
    
    if 'selected_game' in st.session_state:
        st.markdown("---")
        
        if st.session_state.selected_game == "🌬️ Breathing Bubble":
            show_breathing_game()
        elif st.session_state.selected_game == "🎯 Mindful Catcher":
            show_mindful_catcher()
        elif st.session_state.selected_game == "🧩 Peaceful Puzzle":
            show_slider_puzzle()
        
        if st.button("← Back to Games"):
            del st.session_state.selected_game
            st.rerun()
    
    # Call to action for signup
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("💙 **Love these games?** Sign up for more advanced games, track your progress, and unlock daily challenges!")
        if st.button("🚀 Create Free Account", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()