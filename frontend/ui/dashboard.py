import streamlit as st

def show_dashboard():
    st.markdown("""
        <style>
        /* Hide Streamlit default elements */
        #MainMenu, footer, header {visibility: hidden !important;}
        
        /* Title container */
        .dashboard-title {
            text-align: center !important;
            margin-bottom: 0px !important;
            display: block !important;
        }
        /* Emoji - keep native color */
        .title-emoji {
            font-size: 45px !important;
            display: inline-block !important;
            margin-right: 10px !important;
        }
        /* Gradient text - no blue fallback */
        .gradient-text {
            font-size: 45px !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            background-clip: text;
            -webkit-background-clip: text;
            color: #333;  /* neutral fallback (not blue) */
            display: inline-block !important;
        }
        @supports (background-clip: text) or (-webkit-background-clip: text) {
            .gradient-text {
                color: transparent;
            }
        }

        .dashboard-sub {
            text-align: center !important;
            font-size: 18px !important;
            color: #555 !important;
            margin-bottom: 40px !important;
        }

        /* Card styling */
        .card {
            background-color: #b3e0ff !important;
            padding: 30px !important;
            border-radius: 15px !important;
            text-align: center !important;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
            margin: 15px !important;
        }
        .icon { font-size: 40px !important; margin-bottom: 15px !important; }
        .title { font-size: 20px !important; font-weight: 600 !important; color: #0077b6 !important; }
        .text { font-size: 14px !important; color: #444 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Emoji + gradient text separated
    st.markdown("""
        <div class="dashboard-title">
            <span class="title-emoji">🧠</span>
            <span class="gradient-text">MindCare AI Dashboard</span>
        </div>
        <div class="dashboard-sub">Your Personal AI Mental Wellness Companion</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    cards = [
        {"icon":"💬", "title":"AI Chat", "text":"Talk with your AI mental wellness companion anytime."},
        {"icon":"📊", "title":"Mood Log", "text":"Track your daily mood and emotional trends."},
        {"icon":"🕒", "title":"Chat History", "text":"Review your previous conversations anytime."},
        {"icon":"📖", "title":"Journal", "text":"Write private thoughts and reflect on your feelings."}
    ]

    cols = [col1, col2, col3, col4]
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="card">
                    <div class="icon">{cards[i]['icon']}</div>
                    <div class="title">{cards[i]['title']}</div>
                    <div class="text">{cards[i]['text']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><center>🌿 Take care of your mental wellness today.</center>", unsafe_allow_html=True)