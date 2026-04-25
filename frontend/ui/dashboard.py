import streamlit as st

def show_dashboard():
    # --- Remove top white space ---
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: -0.5rem !important;
        }
        .main .block-container > :first-child {
            margin-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Dashboard styling with soft pastel cards ---
    st.markdown("""
        <style>
        #MainMenu, footer {visibility: hidden !important;}
        
        .dashboard-title {
            text-align: center !important;
            margin-bottom: 0px !important;
            display: block !important;
        }
        .title-emoji {
            font-size: 45px !important;
            display: inline-block !important;
            margin-right: 10px !important;
        }
        .gradient-text {
            font-size: 45px !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            background-clip: text;
            -webkit-background-clip: text;
            color: #333;
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

        /* Card base styling */
        .card {
            padding: 30px !important;
            border-radius: 15px !important;
            text-align: center !important;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
            margin: 15px !important;
        }
        .icon { font-size: 40px !important; margin-bottom: 15px !important; }
        .title { font-size: 20px !important; font-weight: 600 !important; color: #0077b6 !important; }
        .text { font-size: 14px !important; color: #444 !important; }

        /* Soft, calm pastel colors */
        .card-chat { background-color: #FADADD !important; }      /* very light pink */
        .card-mood { background-color: #D4F1F9 !important; }      /* very light blue */
        .card-history { background-color: #FEE3D4 !important; }    /* very light peach */
        .card-journal { background-color: #E6D5F5 !important; }    /* very light lavender */
        </style>
    """, unsafe_allow_html=True)

    # Title
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
        {"icon":"💬", "title":"AI Chat", "text":"Talk with your AI mental wellness companion anytime.", "class":"card-chat"},
        {"icon":"📊", "title":"Mood Log", "text":"Track your daily mood and emotional trends.", "class":"card-mood"},
        {"icon":"🕒", "title":"Chat History", "text":"Review your previous conversations anytime.", "class":"card-history"},
        {"icon":"📖", "title":"Journal", "text":"Write private thoughts and reflect on your feelings.", "class":"card-journal"}
    ]

    cols = [col1, col2, col3, col4]
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="card {cards[i]['class']}">
                    <div class="icon">{cards[i]['icon']}</div>
                    <div class="title">{cards[i]['title']}</div>
                    <div class="text">{cards[i]['text']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><center>🌿 Take care of your mental wellness today.</center>", unsafe_allow_html=True)