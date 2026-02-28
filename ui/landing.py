import streamlit as st
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

    # Professional CSS with Colored Boxes - NO BACKGROUND IMAGE
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Simple Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Remove default padding/margin */
    .main > div {
        padding-top: 0px !important;
    }
    
    .block-container {
        padding-top: 20px !important;
        padding-left: 50px !important;
        padding-right: 50px !important;
        max-width: 1400px;
    }
    
    /* ===== NAVIGATION BAR ===== */
    .nav-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 30px;
        border-radius: 60px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
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
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .logo-icon {
        font-size: 36px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    /* Streamlit button styling */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 8px 25px !important;
        border-radius: 40px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        min-width: 120px;
    }
    
    div.stButton > button:hover {
        background: white !important;
        color: #0f172a !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(255,255,255,0.1) !important;
        border-color: white !important;
    }
    
    /* Get Started button special */
    button[key="nav_getstarted"] {
        background: linear-gradient(135deg, #ff8c8c, #ff6b6b) !important;
        border: none !important;
        color: white !important;
        padding: 8px 30px !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
        min-width: 140px !important;
    }
    
    button[key="nav_getstarted"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6) !important;
    }
    
    /* Hero section buttons */
    button[key="hero_start1"], button[key="hero_start2"], button[key="hero_start3"] {
        background: linear-gradient(135deg, #ffb3b3, #ff9e9e) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 10px 25px rgba(255, 179, 179, 0.4) !important;
    }
    
    button[key="hero_learn1"], button[key="hero_learn2"], button[key="hero_learn3"] {
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        padding: 12px 30px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Hero Section */
    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        line-height: 1.1;
        margin-bottom: 20px;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.3);
    }
    
    .highlight {
        color: #fff2b5;
    }
    
    .hero-text {
        color: white;
        font-size: 1.2rem;
        line-height: 1.6;
        margin: 20px 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 50px;
        backdrop-filter: blur(10px);
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: 500;
        border-radius: 40px;
        padding: 8px 25px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255,255,255,0.2) !important;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 60px 0 40px 0;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
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
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 2px;
    }
    
    /* ===== CORE FEATURES CARDS ===== */
    .feature-card {
        border-radius: 20px;
        padding: 30px 20px;
        height: 280px;
        transition: all 0.3s ease;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .feature-icon {
        font-size: 2.8rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: white;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        line-height: 1.5;
        color: rgba(255,255,255,0.9);
    }
    
    /* ===== TECHNOLOGY STACK CARDS ===== */
    .tech-card {
        border-radius: 20px;
        padding: 30px 20px;
        height: 200px;
        transition: all 0.3s ease;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
    }
    
    .tech-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
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
    
    /* ===== SDG CARDS ===== */
    .sdg-card {
        border-radius: 20px;
        padding: 30px;
        height: 180px;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    
    .sdg-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .sdg-number {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }
    
    .sdg-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
    }
    
    /* ===== IMPACT STATISTICS CARDS ===== */
    .impact-card {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        height: 150px;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .impact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFD700;
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: white;
        font-weight: 500;
    }
    
    /* ===== SYSTEM ARCHITECTURE CARDS ===== */
    .arch-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 30px;
        height: 100%;
        transition: all 0.3s ease;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .arch-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.2);
    }
    
    .arch-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: white;
        text-align: center;
        position: relative;
    }
    
    .arch-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: white;
        border-radius: 2px;
    }
    
    .arch-list {
        list-style: none;
        padding: 0;
    }
    
    .arch-list li {
        margin: 15px 0;
        padding: 10px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .arch-list li:hover {
        background: rgba(255,255,255,0.1);
        transform: translateX(5px);
    }
    
    .arch-icon {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Hide Streamlit elements */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Images */
    .stImage img {
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
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
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1.5])
        
        with nav_col1:
            if st.button("🏠 Home", key="nav_home", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        
        with nav_col2:
            if st.button("📖 About Us", key="nav_about", use_container_width=True):
                st.session_state.page = "about"
                st.rerun()
        
        with nav_col3:
            if st.button("🚀 Get Started", key="nav_getstarted", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

    # ================= HERO SECTION WITH SLIDER - PERFECTLY RELEVANT AI MENTAL HEALTH IMAGES =================
    tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "📊 Mood Tracking", "🛡️ Crisis Support"])
    
    with tab1:
        hero_col1, hero_col2 = st.columns([1.1, 1], gap="large")
        
        with hero_col1:
            st.markdown("""
            <h1>
                Empathetic AI for <br>
                <span class="highlight">Mental Wellness</span>
            </h1>
            <p class="hero-text">
                Experience 24/7 emotional support with our advanced AI chatbot. 
                Trained on clinical psychology principles to provide empathetic, 
                evidence-based conversations.
            </p>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🚀 Get Started", key="hero_start1", use_container_width=True):
                    st.session_state.page = "auth"
                    st.rerun()
            with btn_col2:
                if st.button("📚 Learn More", key="hero_learn1", use_container_width=True):
                    st.session_state.page = "about"
                    st.rerun()
        
        with hero_col2:
            st.image(
                "https://img.freepik.com/free-vector/chatbot-concept-illustration_114360-4893.jpg",
                use_container_width=True,
                caption="AI Mental Health Assistant"
            )
    
    with tab2:
        hero_col1, hero_col2 = st.columns([1.1, 1], gap="large")
        
        with hero_col1:
            st.markdown("""
            <h1>
                Track Your <br>
                <span class="highlight">Emotional Journey</span>
            </h1>
            <p class="hero-text">
                Visualize your mood patterns with beautiful analytics. 
                Identify triggers, track progress, and gain insights into your emotional well-being.
            </p>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🚀 Get Started", key="hero_start2", use_container_width=True):
                    st.session_state.page = "auth"
                    st.rerun()
            with btn_col2:
                if st.button("📚 Learn More", key="hero_learn2", use_container_width=True):
                    st.session_state.page = "about"
                    st.rerun()
        
        with hero_col2:
            st.image(
                "https://img.freepik.com/free-vector/mood-tracker-concept-illustration_114360-8745.jpg",
                use_container_width=True,
                caption="Mood Analytics Dashboard"
            )
    
    with tab3:
        hero_col1, hero_col2 = st.columns([1.1, 1], gap="large")
        
        with hero_col1:
            st.markdown("""
            <h1>
                Emergency <br>
                <span class="highlight">Crisis Support</span>
            </h1>
            <p class="hero-text">
                Advanced detection systems identify crisis situations instantly. 
                Immediate connection to helplines and emergency contacts when you need it most.
            </p>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🚀 Get Started", key="hero_start3", use_container_width=True):
                    st.session_state.page = "auth"
                    st.rerun()
            with btn_col2:
                if st.button("📚 Learn More", key="hero_learn3", use_container_width=True):
                    st.session_state.page = "about"
                    st.rerun()
        
        with hero_col2:
            st.image(
                "https://img.freepik.com/free-vector/crisis-support-concept-illustration_114360-8765.jpg",
                use_container_width=True,
                caption="24/7 Crisis Helpline"
            )

    # ================= SYSTEM ARCHITECTURE SECTION =================
    st.markdown('<h2 class="section-title">🏗️ System Architecture</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 40px;">
        Explore how our conversational AI delivers immediate, empathetic responses during moments of crisis or stress
    </p>
    """, unsafe_allow_html=True)
    
    arch_col1, arch_col2, arch_col3 = st.columns(3)
    
    with arch_col1:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-icon">📱</div>
            <div class="arch-title">Frontend Layer</div>
            <ul class="arch-list">
                <li>🖥️ <strong>Streamlit/Gradio:</strong> Chat interface</li>
                <li>🎤 <strong>Voice Support:</strong> Whisper STT + gTTS TTS</li>
                <li>📊 <strong>Mood Tracking:</strong> Interactive charts</li>
                <li>📝 <strong>Journaling:</strong> Personal reflections</li>
                <li>🎨 <strong>Responsive UI:</strong> User-friendly design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with arch_col2:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-icon">⚙️</div>
            <div class="arch-title">Backend Layer</div>
            <ul class="arch-list">
                <li>⚡ <strong>FastAPI:</strong> REST API endpoints</li>
                <li>🗄️ <strong>PostgreSQL:</strong> User data & mood logs</li>
                <li>🔐 <strong>Authentication:</strong> Secure login system</li>
                <li>📈 <strong>Analytics:</strong> Mood pattern analysis</li>
                <li>🔄 <strong>Session Management:</strong> User sessions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with arch_col3:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-icon">🧠</div>
            <div class="arch-title">AI/ML Layer</div>
            <ul class="arch-list">
                <li>🤖 <strong>LLM Integration:</strong> Context-aware responses</li>
                <li>📚 <strong>RAG Pipeline:</strong> LangChain + FAISS</li>
                <li>😊 <strong>Emotion Classification:</strong> XGBoost/Transformers</li>
                <li>🚨 <strong>Crisis Detection:</strong> Self-harm intent</li>
                <li>📞 <strong>Twilio API:</strong> Emergency escalation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture Flow Image
    st.markdown("""
    <div style="margin: 40px 0; text-align: center;">
        <img src="https://miro.medium.com/v2/resize:fit:1400/1*LJUpUoHrEoyQlZb6Gk9ejA.png" 
             style="width: 100%; max-width: 800px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
        <p style="color: white; margin-top: 15px;">End-to-End Architecture Flow</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= CORE FEATURES =================
    st.markdown('<h2 class="section-title">🎯 Core Features</h2>', unsafe_allow_html=True)

    core_features = [
        {"icon": "🧠", "title": "AI-Powered Support", "color": "linear-gradient(135deg, #FF6B6B, #FF8E8E)",
         "text": "Advanced LLM with RAG technology for empathetic, context-aware conversations."},
        {"icon": "📊", "title": "Mood Analytics", "color": "linear-gradient(135deg, #4ECDC4, #6CD4CC)",
         "text": "Real-time mood tracking with beautiful visualizations and pattern recognition."},
        {"icon": "🛡️", "title": "Crisis Detection", "color": "linear-gradient(135deg, #FFD93D, #FFE15D)",
         "text": "AI-powered suicide and self-harm detection with instant emergency escalation."},
        {"icon": "🎤", "title": "Voice Interaction", "color": "linear-gradient(135deg, #6C5CE7, #8A7CEE)",
         "text": "Natural conversations with Whisper STT and gTTS for accessible support."},
        {"icon": "📚", "title": "Clinical Knowledge", "color": "linear-gradient(135deg, #A8E6CF, #BCF0DA)",
         "text": "Evidence-based responses from WHO, APA, and verified mental health resources."},
        {"icon": "🔐", "title": "Privacy First", "color": "linear-gradient(135deg, #FF9F1C, #FFB347)",
         "text": "Bank-level encryption and anonymous conversations for complete privacy."}
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)
    all_cols = row1 + row2

    for i, feature in enumerate(core_features):
        with all_cols[i]:
            st.markdown(f"""
            <div class="feature-card" style="background: {feature['color']};">
                <div class="feature-icon">{feature['icon']}</div>
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-desc">{feature['text']}</div>
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

    # ================= SDG GOALS =================
    st.markdown('<h2 class="section-title">🌍 UN SDG Goals</h2>', unsafe_allow_html=True)
    
    sdg_features = [
        {"number": "3", "title": "Good Health", "color": "linear-gradient(135deg, #4ECDC4, #6CD4CC)"},
        {"number": "9", "title": "Innovation", "color": "linear-gradient(135deg, #FFD93D, #FFE15D)"},
        {"number": "10", "title": "Reduced Inequalities", "color": "linear-gradient(135deg, #FF6B6B, #FF8E8E)"}
    ]
    
    sdg_cols = st.columns(3)
    
    for i, sdg in enumerate(sdg_features):
        with sdg_cols[i]:
            st.markdown(f"""
            <div class="sdg-card" style="background: {sdg['color']};">
                <div class="sdg-number">{sdg['number']}</div>
                <div class="sdg-title">{sdg['title']}</div>
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
    <div style="margin-top:60px; text-align:center; padding:30px; color:white; border-top:1px solid rgba(255,255,255,0.1);">
        <p>© 2026 Mind Care AI | NUML, Islamabad</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()