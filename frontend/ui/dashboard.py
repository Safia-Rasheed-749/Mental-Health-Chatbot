import streamlit as st

def show_dashboard():

    # FIX: Hide ONLY the hamburger menu and footer, NOT the header
    st.markdown("""
        <style>
        /* Hide only the hamburger menu (top-right) */
        #MainMenu {visibility: hidden;}
        
        /* Hide the footer */
        footer {visibility: hidden;}
        
        /* DO NOT hide header - it contains the sidebar collapse button! */
        /* header {visibility: hidden;}  ← REMOVED THIS LINE */
        
        /* Optional: Make header less intrusive but still visible */
        header {
            background: transparent !important;
            box-shadow: none !important;
        }
        
        /* Your existing dashboard styles */
        .dashboard-title{
            text-align:center;
            font-size:40px;
            font-weight:bold;
            background: linear-gradient(90deg,#4facfe,#00f2fe);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            margin-bottom:10px;
        }

        .dashboard-sub{
            text-align:center;
            font-size:18px;
            color:#555;
            margin-bottom:50px;
        }

        .card{
            background-color:#b3e0ff;
            padding:30px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 4px 10px rgba(0,0,0,0.1);
            margin:15px;
            transition:none;
        }

        .icon{
            font-size:40px;
            margin-bottom:15px;
        }

        .title{
            font-size:20px;
            font-weight:600;
            color:#0077b6;
            margin-bottom:10px;
        }

        .text{
            font-size:14px;
            color:#444;
        }
        </style>
    """, unsafe_allow_html=True)

    # Dashboard Title
    st.markdown('<div class="dashboard-title">🧠 MindCare AI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-sub">Your Personal AI Mental Wellness Companion</div>', unsafe_allow_html=True)

    # Cards in two rows of two columns each
    rows = []
    for _ in range(2):
        rows.append(st.columns(2, gap="large"))

    # Card contents
    cards = [
        {"icon":"💬", "title":"AI Chat", "text":"Talk with your AI mental wellness companion anytime."},
        {"icon":"📊", "title":"Mood Log", "text":"Track your daily mood and emotional trends."},
        {"icon":"🕒", "title":"Chat History", "text":"Review your previous conversations anytime."},
        {"icon":"📖", "title":"Journal", "text":"Write private thoughts and reflect on your feelings."}
    ]

    for i, row in enumerate(rows):
        with row[0]:
            st.markdown(f"""
                <div class="card">
                    <div class="icon">{cards[i*2]['icon']}</div>
                    <div class="title">{cards[i*2]['title']}</div>
                    <div class="text">{cards[i*2]['text']}</div>
                </div>
            """, unsafe_allow_html=True)
        with row[1]:
            st.markdown(f"""
                <div class="card">
                    <div class="icon">{cards[i*2+1]['icon']}</div>
                    <div class="title">{cards[i*2+1]['title']}</div>
                    <div class="text">{cards[i*2+1]['text']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<center>🌿 Take care of your mental wellness today.</center>", unsafe_allow_html=True)