import streamlit as st
import streamlit.components.v1 as components
from layout_utils import apply_clean_layout


def show_dashboard():
    # Invisible anchor at the very top of the dashboard
    st.markdown('<div id="dashboard-top-anchor" style="position: absolute; top: 0;"></div>', unsafe_allow_html=True)
    
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
    # Force scroll to top using multiple attempts (works after login)
    components.html(
        """
        <script>
            function scrollToTop() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                var anchor = document.getElementById('dashboard-top-anchor');
                if (anchor) anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            scrollToTop();
            for (var i = 1; i <= 20; i++) {
                setTimeout(scrollToTop, i * 80);
            }
            window.addEventListener('load', function() { scrollToTop(); });
        </script>
        """,
        height=0,
        scrolling=False
    )
    
    apply_clean_layout(hide_header_completely=False)

    # Custom CSS (unchanged)
    st.markdown("""
        <style>
        .main .block-container > :first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .element-container:first-child,
        .stMarkdown:first-child {
            margin-top: 0 !important;
        }
        .dashboard-title {
            text-align: center !important;
            margin: 0 !important;
            padding: 0 !important;
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
            color: transparent;
            display: inline-block !important;
        }
        .dashboard-sub {
            text-align: center !important;
            font-size: 18px !important;
            color: #555 !important;
            margin-bottom: 30px !important;
            margin-top: 0 !important;
        }
        .card {
            padding: 30px !important;
            border-radius: 15px !important;
            text-align: center !important;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
            margin: 15px !important;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .icon { font-size: 40px !important; margin-bottom: 15px !important; }
        .title { font-size: 20px !important; font-weight: 600 !important; color: #0077b6 !important; }
        .text { font-size: 14px !important; color: #444 !important; }

        .card-chat { background-color: #FADADD !important; }
        .card-mood { background-color: #D4F1F9 !important; }
        .card-history { background-color: #FEE3D4 !important; }
        .card-journal { background-color: #E6D5F5 !important; }
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

    # Cards layout
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