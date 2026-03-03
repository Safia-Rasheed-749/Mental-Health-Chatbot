import streamlit as st
import streamlit.components.v1 as components

def show_landing_page():
    # ================= GLOBAL STYLE =================
    st.markdown("""
    <style>
    /* Force light blue background everywhere */
    html, body, #root, .stApp, .main, .block-container, div[data-testid="stVerticalBlock"] {
        background-color: #add8e6 !important;
    }

    header {visibility:hidden;}
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}

    .block-container {
        padding-top: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        max-width: 100%;
    }

    /* Top bar */
    .top-bar {
        background-color: #add8e6;
        padding: 15px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        box-sizing: border-box;
        position: relative;
    }

    .left-section {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* Hamburger icon (static) */
    .hamburger {
        font-size: 30px;
        color: #000;
        cursor: pointer;
        user-select: none;
        display: inline-block;
    }

    /* Logo */
    .logo {
        font-size: 28px;
        font-weight: 800;
        color: #000;
        display: inline-block;
    }

    /* Style the segmented control to look like toggle buttons */
    div[data-testid="stSegmentedControl"] {
        background-color: rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 40px !important;
        padding: 4px !important;
        width: fit-content !important;
    }
    div[data-testid="stSegmentedControl"] > div {
        gap: 0px !important;
    }
    div[data-testid="stSegmentedControl"] label {
        padding: 8px 24px !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        color: #000 !important;
        transition: all 0.2s ease !important;
        background: transparent !important;
        border: none !important;
        font-size: 1rem !important;
    }
    div[data-testid="stSegmentedControl"] label:hover {
        background: rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stSegmentedControl"] label[data-checked="true"] {
        background: #ef4444 !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3) !important;
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

    /* BUTTON STYLE */
    .button-section {
        display: flex;
        justify-content: center;
        margin: 40px 0 60px 0;
        width: 100%;
        background-color: transparent !important;
    }

    .stButton > button {
        background-color: #ef4444 !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 18px 45px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        animation: pulse 2.5s infinite;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }

    /* FEATURE CARDS */
    .features-section {
        padding: 100px 40px;
        background-color: transparent !important;
    }

    .feature-card {
        border-radius: 30px;
        padding: 40px 25px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: none;
        margin-bottom: 20px;
    }

    .feature-card:hover {
        transform: none;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    .feature-card:hover .icon-box {
        transform: none;
    }

    .icon-box {
        font-size: 55px;
        margin-bottom: 20px;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1));
        transition: none;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #1e293b;
    }

    .feature-card p {
        color: #475569;
        flex-grow: 1;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Carousel container */
    .carousel-wrapper {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
        background-color: transparent !important;
    }
    .carousel-outer {
        border: 2px solid #e2e8f0;
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    /* Additional features */
    .extra-features-section {
        padding: 60px 40px;
        background-color: transparent !important;
    }
    .extra-feature-item {
        text-align: center;
        padding: 0 20px;
        border-right: 1px solid #d4c9c0;
    }
    .extra-feature-item:last-child {
        border-right: none;
    }
    .extra-icon {
        font-size: 48px;
        margin-bottom: 15px;
    }
    .extra-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .extra-desc {
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    @media (max-width: 768px) {
        .extra-feature-item {
            border-right: none;
            border-bottom: 1px solid #d4c9c0;
            padding-bottom: 30px;
            margin-bottom: 30px;
        }
        .extra-feature-item:last-child {
            border-bottom: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= TOP BAR WITH HAMBURGER (LEFT) AND TOGGLE BUTTONS (RIGHT) =================
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 15px;">
            <span class="hamburger">☰</span>
            <span class="logo">🧠 MindCare AI</span>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Segmented control as toggle buttons
        nav_mode = st.segmented_control(
            "",
            options=["Home", "About", "Demo"],
            default="Home",
            label_visibility="collapsed",
            key="nav_toggle"
        )

        if nav_mode == "About":
            st.session_state.page = "about"
            st.rerun()
        elif nav_mode == "Demo":
            st.info("Demo Page Coming Soon!")
        # Home does nothing (stays on landing page)

    # ================= HERO SECTION =================
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">
            Empathetic AI for <br>
            <span style="color: #a5b4fc;">Mental Support</span>
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
            font-family: 'Segoe UI', system-ui, sans-serif;
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
            letter-spacing: 0.5px;
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

    # ================= CORE FEATURES =================
    st.markdown('<div class="features-section">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-weight:800; color:#1e293b; margin-bottom: 50px;'>Core Capabilities</h2>", unsafe_allow_html=True)

    features = [
        {"icon": "💬", "title": "Emotion-Aware Chat", "bg": "linear-gradient(145deg, #E0F2FE, #B8E1FF)"},
        {"icon": "📊", "title": "Mood Analytics", "bg": "linear-gradient(145deg, #DCFCE7, #B8F0C0)"},
        {"icon": "🛡️", "title": "Crisis Detection", "bg": "linear-gradient(145deg, #FEE2E2, #FFC7C7)"},
        {"icon": "🎤", "title": "Voice Support", "bg": "linear-gradient(145deg, #F3E8FF, #E2CCFF)"},
        {"icon": "📚", "title": "RAG Knowledge", "bg": "linear-gradient(145deg, #FEF3C7, #FFE5A0)"},
        {"icon": "🧘", "title": "Coping Tools", "bg": "linear-gradient(145deg, #ECFDF5, #C8F0E5)"}
    ]

    row1 = st.columns(3, gap="large")
    for i, feature in enumerate(features[:3]):
        with row1[i]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card" style="background: {feature['bg']}">
                    <div class="icon-box">{feature['icon']}</div>
                    <div class="card-title">{feature['title']}</div>
                    <p>AI-powered support tailored to your emotions, with real-time analytics and personalized coping strategies.</p>
                </div>
                """, unsafe_allow_html=True)

    row2 = st.columns(3, gap="large")
    for i, feature in enumerate(features[3:]):
        with row2[i]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card" style="background: {feature['bg']}">
                    <div class="icon-box">{feature['icon']}</div>
                    <div class="card-title">{feature['title']}</div>
                    <p>AI-powered support tailored to your emotions, with real-time analytics and personalized coping strategies.</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= ADDITIONAL FEATURES =================
    st.markdown('<div class="extra-features-section">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; font-weight:700; color:#1e293b; margin-bottom: 40px;'>More Features</h3>", unsafe_allow_html=True)

    extra_cols = st.columns(3, gap="medium")

    with extra_cols[0]:
        st.markdown("""
        <div class="extra-feature-item">
            <div class="extra-icon">📓</div>
            <div class="extra-title">Mood Tracking & Journaling</div>
            <div class="extra-desc">Log your daily mood, write private journal entries, and visualize emotional patterns over time.</div>
        </div>
        """, unsafe_allow_html=True)

    with extra_cols[1]:
        st.markdown("""
        <div class="extra-feature-item">
            <div class="extra-icon">🆘</div>
            <div class="extra-title">Emergency Escalation</div>
            <div class="extra-desc">Automatic detection of crisis language with immediate helpline info and optional Twilio SMS/call.</div>
        </div>
        """, unsafe_allow_html=True)

    with extra_cols[2]:
        st.markdown("""
        <div class="extra-feature-item">
            <div class="extra-icon">🎤</div>
            <div class="extra-title">Voice Interaction</div>
            <div class="extra-desc">Speak naturally using Whisper STT and hear responses with gTTS – full voice conversations.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()