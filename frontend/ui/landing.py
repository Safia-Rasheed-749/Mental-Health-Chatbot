import streamlit as st
import streamlit.components.v1 as components
import os

def show_landing_page():
    # Fix the path to look for assets outside frontend folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # .../frontend/ui/
    frontend_dir = os.path.dirname(current_dir)  # .../frontend/
    project_dir = os.path.dirname(frontend_dir)  # .../Mental-Health-Chatbot/
    
    # Now look for assets folder in the project root
    css_path = os.path.join(project_dir, "assets", "style.css")
    
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    # ================= GLOBAL STYLE =================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Force white background everywhere */
    html, body, #root, .stApp, .main, .block-container, div[data-testid="stVerticalBlock"] {
        background-color: white !important;
        font-family: 'Inter', sans-serif;
    }

    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding-top: 0px !important;
        padding-left: 50px !important;
        padding-right: 50px !important;
        max-width: 1400px;
    }

    /* ===== NAVIGATION BAR ===== */
    .nav-container {
        background: purple !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 10px 30px;
        border-radius: 60px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        margin: 10px 0 30px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Logo styling */
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 26px;
        font-weight: 700;
        color: #6D9EEB !important;      
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .logo-icon {
        font-size: 36px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    /* Streamlit button styling for nav */
    div.stButton > button {
        background : linear-gradient(135deg, #B8D9FF, #6D9EEB) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 8px 25px !important;
        border-radius: 40px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        min-width: 100px;
    }
    
    div.stButton > button:hover {
        background: #6D9EEB  !important;
        color: white !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3) !important;
        border-color: #ff4444 !important;
    }
    
    /* Get Started button special */
    button[key="nav_getstarted"] {
        background: purple !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        padding: 8px 30px !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        min-width: 140px !important;
    }
    
    button[key="nav_getstarted"]:hover {
        background: #ff4444 !important;
        color: white !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3) !important;
        border-color: #ff4444 !important;
    }

    /* HERO SECTION */
    .hero-container {
        background-image: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.55)), url('https://loweryourstress.com/wp-content/uploads/2024/06/Unwind-and-Destress.png');
        background-size: cover;
        background-position: center 30%;
        height: 85vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
        animation: zoomBg 20s infinite alternate ease-in-out;
        border-radius: 30px;
        margin: 20px 0;
    }

    @keyframes zoomBg {
        0% { background-size: 100%; }
        100% { background-size: 110%; }
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 20px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
        max-width: 900px;
        padding: 0 20px;
        animation: fadeUp 1.2s ease-out;
    }

    .hero-title span {
        color: #a5b4fc;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        color: #f1f5f9;
        font-weight: 400;
        max-width: 700px;
        margin-bottom: 30px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
        animation: fadeUp 1.2s 0.2s ease-out both;
    }

    .hero-mission {
        font-size: 1.2rem;
        color: #e2e8f0;
        max-width: 800px;
        margin-bottom: 40px;
        font-style: italic;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 25px;
        line-height: 1.6;
        text-shadow: 0 1px 5px rgba(0,0,0,0.5);
        animation: fadeUp 1.2s 0.4s ease-out both;
    }

    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* GET STARTED BUTTON */
    .button-section {
        display: flex;
        justify-content: center;
        margin: 20px 0 40px 0;
        width: 100%;
        background-color: transparent !important;
        animation: fadeUp 1.2s 0.6s ease-out both;
    }

    .stButton > button {
        background-color: #ef4444 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 18px 45px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3) !important;
        animation: pulse 2.5s infinite;
        width: auto !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(239, 68, 68, 0.4) !important;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }

    /* ===== SECTION TITLES ===== */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #333;
        margin: 60px 0 40px 0;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
    }

    /* FEATURE CARDS */
    .features-section {
        padding: 60px 0;
    }

    .feature-card {
        border-radius: 30px;
        padding: 40px 25px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    .icon-box {
        font-size: 55px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: white;
    }

    .feature-card p {
        color: rgba(255,255,255,0.9);
        flex-grow: 1;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Carousel container */
    .carousel-wrapper {
        max-width: 1400px;
        margin: 40px auto;
        padding: 0 20px;
    }
    .carousel-outer {
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    /* TECH STACK CARDS */
    .tech-card {
        border-radius: 20px;
        padding: 30px 20px;
        height: 200px;
        transition: all 0.3s ease;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        color: white; 
    }
    
    .tech-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    .tech-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .tech-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 5px;
        color: white;
    }
    
    .tech-desc {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
    }


    /* IMPACT STATISTICS CARDS */
    .impact-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        height: 150px;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .impact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4a7db5;
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: #2c3e50;
        font-weight: 500;
    }

    /* ===== EXERCISES SECTION - FULL WIDTH CARDS ===== */
    .exercise-section {
        padding: 15px 0;
    }
    
    .exercise-card {
        border-radius: 25px;
        padding: 25px;
        width: 100%;
        min-height: 300px;
        transition: all 0.4s ease;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 40px;
        margin: 30px 0;
        border: 1px solid rgba(255,255,255,0.3);
        animation: fadeIn 0.8s ease-out;
    }
    
    .exercise-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 25px 50px rgba(0,0,0,0.25);
    }
    
    /* Card 1 - Breathing Exercise */
    .exercise-card-1 {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
    }
    
    /* Card 2 - Mindfulness */
    .exercise-card-2 {
        background: linear-gradient(135deg, #43e97b, #38f9d7);
    }
    
    /* Card 3 - Grounding */
    .exercise-card-3 {
        background: linear-gradient(135deg, #fa709a, #fee140);
    }
    
    .exercise-icon-large {
        font-size: 6rem;
        min-width: 150px;
        text-align: center;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .exercise-content {
        flex: 1;
    }
    
    .exercise-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .exercise-quote {
        font-style: italic;
        font-size: 1.1rem;
        color: rgba(255,255,255,0.95);
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        border-left: 5px solid white;
    }
    
    .exercise-quote-author {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        text-align: right;
        margin-top: 8px;
    }
    
    .exercise-steps {
        list-style: none;
        padding: 0;
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
    }
    
    .exercise-steps li {
        flex: 1 1 calc(50% - 15px);
        padding: 12px 15px;
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.2s ease;
        color: white;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .exercise-steps li:hover {
        background: rgba(255,255,255,0.3);
        transform: translateX(5px);
    }
    
    .step-number {
        background: white;
        color: #333;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    
    .exercise-image-small {
        font-size: 2rem;
        margin-left: 5px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* ===== FOOTER STYLES ===== */
    .footer {
        margin-top: 60px !important;
        text-align: center !important;
        padding: 30px !important;
        color: #666 !important;
        border-top: 2px solid #e0e0e0 !important;
        background-color: #f9f9f9 !important;
        width: 100% !important;
        display: block !important;
        visibility: visible !important;
        position: relative !important;
        z-index: 100 !important;
    }
    
    .footer p {
        color: #666 !important;
        font-size: 1rem !important;
        margin: 5px 0 !important;
        line-height: 1.5 !important;
    }
    
    /* Hide Streamlit elements */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Images */
    .stImage img {
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border: 3px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= NAVIGATION BAR =================
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div class="logo">
                <span class="logo-icon">🧠</span>
                <span>Mind Care AI</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1.2])
        
        with nav_col1:
            if st.button("🏠 Home", key="nav_home", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        
        with nav_col2:
            if st.button("📖 About", key="nav_about", use_container_width=True):
                st.session_state.page = "about"
                st.rerun()
        
        with nav_col3:
            if st.button("🚀 Demo", key="nav_demo", use_container_width=True):
                # ⭐ Reset demo state when starting demo
                st.session_state.demo_messages = []
                st.session_state.demo_count = 0
                st.session_state.page = "demo"
                st.rerun()
        
        with nav_col4:
            if st.button("🚀 Get Started", key="nav_getstarted", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

    # ================= HERO SECTION =================
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">
            Empathetic AI for <br>
            <span>Mental Support</span>
        </h1>
        <p class="hero-subtitle">
            Your personal, safe and intelligent companion for emotional wellbeing.
        </p>
        <div class="hero-mission">
            “Mental health needs have multiplied. Support hasn't.<br>
            Our mission is to make mental health support radically accessible.”
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= GET STARTED BUTTON =================
    st.markdown('<div class="button-section">', unsafe_allow_html=True)
    if st.button("🚀 Get Started", key="get_started_hero"):
        st.session_state.page = "auth"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SLIDING QUOTE CAROUSEL =================
    st.markdown('<div class="carousel-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="carousel-outer">', unsafe_allow_html=True)

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            background: transparent;
            font-family: 'Inter', sans-serif;
        }
        .carousel-container {
            width: 100%;
            overflow: hidden;
            position: relative;
            height: 350px;
            background: transparent;
        }
        .carousel-track {
            display: flex;
            width: 400%;
            height: 100%;
            transition: transform 0.7s ease-in-out;
        }
        .slide {
            width: 25%;
            height: 100%;
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            position: relative;
        }
        .slide::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.2);
        }
        .quote-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(8px);
            border-radius: 40px;
            padding: 30px 50px;
            max-width: 800px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
            z-index: 2;
            margin: 0 20px;
        }
        .quote-text {
            color: #0f172a;
            font-size: 28px;
            font-weight: 500;
            line-height: 1.5;
            font-style: italic;
            margin: 0;
        }
        .quote-author {
            margin-top: 20px;
            color: #334155;
            font-size: 16px;
            font-weight: 400;
        }
    </style>
    </head>
    <body>
    <div class="carousel-container">
        <div class="carousel-track" id="carouselTrack">
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Healing takes time, and asking for help is a courageous step.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Your mental health is a priority. Your happiness is essential.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“It’s okay to not be okay. Just don’t give up.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Healing takes time, and asking for help is a courageous step.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const track = document.getElementById('carouselTrack');
        let currentIndex = 0;
        const totalSlides = 3;
        const slideWidth = 25;

        function moveToNext() {
            currentIndex++;
            track.style.transform = `translateX(-${currentIndex * slideWidth}%)`;

            if (currentIndex === totalSlides) {
                setTimeout(() => {
                    track.style.transition = 'none';
                    track.style.transform = `translateX(0%)`;
                    currentIndex = 0;
                    track.getBoundingClientRect();
                    track.style.transition = 'transform 0.7s ease-in-out';
                }, 700);
            }
        }
        setInterval(moveToNext, 5000);
    </script>
    </body>
    </html>
    """, height=350)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= MENTAL HEALTH EXERCISES SECTION - FULL WIDTH CARDS =================
    st.markdown('<h2 class="section-title">🧘 Mental Wellness Exercises</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 40px;">
   Try these evidence-based exercises to support your mental well-being
    </p>
    """, unsafe_allow_html=True)
    
    # Exercise 1 - Breathing
    st.markdown("""
    <div class="exercise-card exercise-card-1">
        <div class="exercise-icon-large">🌬️</div>
        <div class="exercise-content">
            <div class="exercise-title">Breathing Exercise</div>
            <div class="exercise-quote">
                "Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."
                <div class="exercise-quote-author">— Thich Nhat Hanh</div>
            </div>
            <ul class="exercise-steps">
                <li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li>
                <li><span class="step-number">2</span> Hold your breath for 4 seconds</li>
                <li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li>
                <li><span class="step-number">4</span> Repeat 5-10 times <span class="exercise-image-small">🧘</span></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercise 2 - Mindfulness
    st.markdown("""
    <div class="exercise-card exercise-card-2">
        <div class="exercise-icon-large">🧠</div>
        <div class="exercise-content">
            <div class="exercise-title">Mindfulness</div>
            <div class="exercise-quote">
                "The present moment is filled with joy and happiness. If you are attentive, you will see it."
                <div class="exercise-quote-author">— Thich Nhat Hanh</div>
            </div>
            <ul class="exercise-steps">
                <li><span class="step-number">1</span> Sit comfortably and close your eyes</li>
                <li><span class="step-number">2</span> Focus on your breath without judgment</li>
                <li><span class="step-number">3</span> Notice thoughts and let them pass</li>
                <li><span class="step-number">4</span> Practice for 5-10 minutes daily <span class="exercise-image-small">🧠</span></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercise 3 - Grounding
    st.markdown("""
    <div class="exercise-card exercise-card-3">
        <div class="exercise-icon-large">🌍</div>
        <div class="exercise-content">
            <div class="exercise-title">5-4-3-2-1 Grounding</div>
            <div class="exercise-quote">
                "Grounding is a powerful way to calm anxiety and return to the present moment."
                <div class="exercise-quote-author">— MindCare AI</div>
            </div>
            <ul class="exercise-steps">
                <li><span class="step-number">👁️</span> Acknowledge 5 things you see</li>
                <li><span class="step-number">🫂</span> Acknowledge 4 things you can touch</li>
                <li><span class="step-number">👂</span> Acknowledge 3 things you hear</li>
                <li><span class="step-number">👃</span> Acknowledge 2 things you can smell</li>
                <li><span class="step-number">👅</span> Acknowledge 1 thing you can taste <span class="exercise-image-small">🌿</span></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= CORE FEATURES =================
    st.markdown('<h2 class="section-title">🎯 Core Capabilities</h2>', unsafe_allow_html=True)

    features = [
        {"icon": "💬", "title": "Emotion-Aware Chat", "bg": "linear-gradient(135deg, #FF6B6B, #FF8E8E)"},
        {"icon": "📊", "title": "Mood Analytics", "bg": "linear-gradient(135deg, #4ECDC4, #6CD4CC)"},
        {"icon": "🛡️", "title": "Crisis Detection", "bg": "linear-gradient(135deg, #FFD93D, #FFE15D)"},
        {"icon": "🎤", "title": "Voice Support", "bg": "linear-gradient(135deg, #6C5CE7, #8A7CEE)"},
        {"icon": "📚", "title": "RAG Knowledge", "bg": "linear-gradient(135deg, #A8E6CF, #BCF0DA)"},
        {"icon": "🧘", "title": "Coping Tools", "bg": "linear-gradient(135deg, #ECFDF5, #C8F0E5)"}
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)
    all_cols = row1 + row2

    for i, feature in enumerate(features):
        with all_cols[i]:
            st.markdown(f"""
            <div class="feature-card" style="background: {feature['bg']}">
                <div class="icon-box">{feature['icon']}</div>
                <div class="card-title">{feature['title']}</div>
                <p>AI-powered support tailored to your emotions, with real-time analytics and personalized coping strategies.</p>
            </div>
            """, unsafe_allow_html=True)

    # ================= TECHNOLOGY STACK =================
    st.markdown('<h2 class="section-title">🔧 Technology Stack</h2>', unsafe_allow_html=True)
    
    tech_features = [
        {"icon": "⚡", "title": "Frontend", "desc": "Streamlit", "color": "linear-gradient(135deg, #FF6B6B, #FF8E8E)"},
        {"icon": "🤖", "title": "AI Engine", "desc": "LLM + RAG", "color": "linear-gradient(135deg, #4ECDC4, #6CD4CC)"},
        {"icon": "🗄️", "title": "Backend", "desc": "FastAPI", "color": "linear-gradient(135deg, #FFD93D, #FFE15D)"},
        {"icon": "🎤", "title": "Voice", "desc": "Whisper", "color": "linear-gradient(135deg, #6C5CE7, #8A7CEE)"}
    ]
    
    tech_cols = st.columns(4)
    
    for i, tech in enumerate(tech_features):
        with tech_cols[i]:
            st.markdown(f"""
            <div class="tech-card" style="background: {tech['color']};">
                <div class="tech-icon">{tech['icon']}</div>
                <div class="tech-title">{tech['title']}</div>
                <div class="tech-desc">{tech['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ================= IMPACT STATISTICS =================
    st.markdown('<h2 class="section-title">📊 Impact</h2>', unsafe_allow_html=True)
    
    impact_features = [
        {"number": "24/7", "label": "Availability", "color": "linear-gradient(135deg, #FF6B6B, #FF8E8E)"},
        {"number": "100%", "label": "Anonymous", "color": "linear-gradient(135deg, #4ECDC4, #6CD4CC)"},
        {"number": "50+", "label": "Sources", "color": "linear-gradient(135deg, #FFD93D, #FFE15D)"},
        {"number": "Real-time", "label": "Detection", "color": "linear-gradient(135deg, #6C5CE7, #8A7CEE)"}
    ]
    
    impact_cols = st.columns(4)
    
    for i, impact in enumerate(impact_features):
        with impact_cols[i]:
            st.markdown(f"""
            <div class="impact-card" style="background: {impact['color']};">
                <div class="stat-number" style="color: white;">{impact['number']}</div>
                <div class="stat-label" style="color: white;">{impact['label']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div class="footer">
        <p>© 2026 Mind Care AI | National University of Modern Languages, Islamabad</p>
        <p>Final Year Project | Department of Computer Science</p>
        <p style="font-size: 0.85rem; color: #999;">Supervised by Faisal Hussain</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()