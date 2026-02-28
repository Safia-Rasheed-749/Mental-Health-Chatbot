import streamlit as st

def show_about_page():
    # Custom CSS for Sky Blue Theme
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sky Blue Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #87CEEB 0%, #5F9EA0 100%);
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
    
    /* ===== GLASSMORPHISM NAVIGATION BAR ===== */
    .nav-container {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 10px 30px;
        border-radius: 60px;
        box-shadow: 0 8px 32px rgba(135, 206, 235, 0.3);
        margin: 15px 0 30px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }
    
    /* Logo styling */
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        font-size: 32px;
        background: linear-gradient(135deg, #87CEEB, #5F9EA0);
        padding: 8px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 10px rgba(135, 206, 235, 0.3);
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Navigation buttons - FIXED: No extra Back to Home button */
    div.stButton > button {
        border-radius: 30px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        height: 45px !important;
    }
    
    button[key^="nav"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
    }
    
    button[key^="nav"]:hover {
        background: white !important;
        color: #5F9EA0 !important;
        transform: translateY(-2px) !important;
    }
    
    button[key="nav_getstarted_about"] {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.4) !important;
    }
    
    /* Section Titles with Sky Blue Gradient */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF, #E0FFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
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
        background: linear-gradient(90deg, #87CEEB, #5F9EA0);
        border-radius: 2px;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 30px;
        color: white;
        transition: all 0.3s ease;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(135, 206, 235, 0.2);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255,255,255,0.5);
        box-shadow: 0 20px 40px rgba(135, 206, 235, 0.3);
    }
    
    /* Problem-Solution Cards */
    .problem-card {
        background: rgba(255, 182, 193, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 182, 193, 0.3);
        border-radius: 20px;
        padding: 25px;
        color: white;
        height: 250px;
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    
    .problem-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 182, 193, 0.6);
        background: rgba(255, 182, 193, 0.3);
    }
    
    .solution-card {
        background: rgba(144, 238, 144, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(144, 238, 144, 0.3);
        border-radius: 20px;
        padding: 25px;
        color: white;
        height: 250px;
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    
    .solution-card:hover {
        transform: translateY(-5px);
        border-color: rgba(144, 238, 144, 0.6);
        background: rgba(144, 238, 144, 0.3);
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px 20px;
        height: 200px;
        transition: all 0.3s ease;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(255,255,255,0.5);
        box-shadow: 0 15px 30px rgba(135, 206, 235, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* SDG Cards */
    .sdg-card {
        border-radius: 25px;
        padding: 30px;
        color: white;
        transition: all 0.4s ease;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .sdg-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
        z-index: 1;
    }
    
    .sdg-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(135, 206, 235, 0.4);
    }
    
    .sdg-number {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 10px;
        position: relative;
        z-index: 2;
    }
    
    .sdg-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 20px;
        position: relative;
        z-index: 2;
    }
    
    /* Tech Cards */
    .tech-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        height: 160px;
        margin: 10px 0;
    }
    
    .tech-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255,255,255,0.5);
        background: rgba(255,255,255,0.25);
    }
    
    .tech-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .tech-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .tech-desc {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
    }
    
    /* Team Cards */
    .team-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        height: 200px;
        margin: 10px 0;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.3);
        border-color: rgba(255,255,255,0.5);
    }
    
    .team-avatar {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    .team-name {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .team-role {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit elements */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # ===== NAVIGATION BAR (No extra Back to Home button) =====
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="logo">
            <span class="logo-icon">🧠</span>
            <span class="logo-text">Mind Care AI</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nav_cols = st.columns([1, 1, 1.5])
        
        with nav_cols[0]:
            if st.button("🏠 Home", key="nav_home_about", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        
        with nav_cols[1]:
            if st.button("📖 About", key="nav_about_about", use_container_width=True):
                st.session_state.page = "about"
                st.rerun()
        
        with nav_cols[2]:
            if st.button("🚀 Get Started", key="nav_getstarted_about", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

    # ===== HERO TITLE =====
    st.markdown("""
    <h1 style="text-align:center; font-size:3.5rem; color:white; margin:40px 0; text-shadow:2px 2px 15px rgba(135,206,235,0.5);">
        About <span style="background:linear-gradient(135deg, #FFFFFF, #E0FFFF); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Mind Care AI</span>
    </h1>
    """, unsafe_allow_html=True)

    # ===== PROJECT OVERVIEW =====
    st.markdown("""
    <div class="glass-card">
        <h2 style="color:white; margin-bottom:20px; font-size:2rem;">🎯 Project Overview</h2>
        <p style="color:rgba(255,255,255,0.95); font-size:1.2rem; line-height:1.8;">
            <strong>Mind Care AI</strong> is a Final Year Project (FYP) developed by students of the 
            <strong>Department of Computer Science</strong> at the <strong>National University of Modern Languages (NUML), Islamabad.</strong>
        </p>
        <p style="color:rgba(255,255,255,0.95); font-size:1.1rem; line-height:1.8; margin-top:20px;">
            The project aims to create an <strong>AI-powered conversational assistant for mental health support</strong> that provides empathetic, accessible, 
            and safe emotional support to individuals experiencing stress, anxiety, or emotional distress.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== PROBLEM STATEMENT WITH SOLUTIONS =====
    st.markdown("""
    <h2 style="text-align:center; font-size:2.2rem; color:white; margin:50px 0 30px 0; text-shadow:0 2px 10px rgba(135,206,235,0.3);">
        Problem & Solution
    </h2>
    """, unsafe_allow_html=True)
    
    # Problem 1 with Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="problem-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">😶</div>
            <h3 style="color:white;">High Stigma</h3>
            <p style="color:rgba(255,255,255,0.9);">
                People avoid visiting therapists or discussing emotional struggles openly due to social stigma and fear of judgment.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">💬</div>
            <h3 style="color:white;">Anonymous Support</h3>
            <p style="color:rgba(255,255,255,0.9);">
                100% anonymous conversations with no personal data required. Users can freely express themselves without fear.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem 2 with Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="problem-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">⏰</div>
            <h3 style="color:white;">Lack of Immediate Support</h3>
            <p style="color:rgba(255,255,255,0.9);">
                During emotional breakdowns or panic attacks, professional help is not always immediately available.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🤖</div>
            <h3 style="color:white;">24/7 AI Support</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Our AI chatbot is available 24/7, providing instant emotional support whenever users need it most.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem 3 with Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="problem-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🔍</div>
            <h3 style="color:white;">Poor-Quality Information</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Online searches often result in unreliable, misleading, or generic mental-health advice.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">📚</div>
            <h3 style="color:white;">RAG Knowledge Base</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Evidence-based responses from WHO, APA, and verified mental health resources using RAG technology.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem 4 with Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="problem-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🤖</div>
            <h3 style="color:white;">Emotionally Insensitive Bots</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Most chatbots respond generically without detecting user emotions or distress levels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🧠</div>
            <h3 style="color:white;">Emotion-Aware AI</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Real-time sentiment analysis and emotion detection for empathetic, personalized responses.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem 5 with Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="problem-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🚨</div>
            <h3 style="color:white;">Lack of Emergency Detection</h3>
            <p style="color:rgba(255,255,255,0.9);">
                Tools fail to recognize suicidal language or self-harm intent in critical situations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <div style="font-size:2.5rem; margin-bottom:10px;">🛡️</div>
            <h3 style="color:white;">Crisis Detection</h3>
            <p style="color:rgba(255,255,255,0.9);">
                AI-powered suicide and self-harm detection with instant emergency escalation via Twilio.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ===== KEY FEATURES =====
    st.markdown('<h2 class="section-title">✨ Key Features</h2>', unsafe_allow_html=True)
    
    features = [
        ("🧠", "Emotion-Aware AI", "Real-time sentiment analysis and empathetic responses"),
        ("📊", "Mood Tracking", "Track emotional patterns with visual charts"),
        ("🛡️", "Crisis Detection", "Suicide and self-harm intent detection"),
        ("🎤", "Voice Support", "Whisper speech-to-text and gTTS voice responses"),
        ("📚", "RAG Knowledge", "Evidence-based responses from WHO and APA"),
        ("🔐", "Privacy First", "Secure authentication and encrypted storage")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features[:3]):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features[3:]):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ===== SDG GOALS =====
    st.markdown('<h2 class="section-title">🌍 UN SDG Goals</h2>', unsafe_allow_html=True)
    
    # SDG 3
    st.markdown("""
    <div class="sdg-card" style="background: linear-gradient(135deg, #4caf50, #2e7d32);">
        <div class="sdg-number">3</div>
        <div class="sdg-title">GOOD HEALTH AND WELL-BEING</div>
        <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px;">
            <ul style="color: white; line-height: 1.8;">
                <li>Provides accessible mental health support to all individuals</li>
                <li>Offers 24/7 emotional support and crisis intervention</li>
                <li>Promotes mental well-being through mood tracking and journaling</li>
                <li>Early detection of mental health issues through sentiment analysis</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # SDG 9
    st.markdown("""
    <div class="sdg-card" style="background: linear-gradient(135deg, #ff9800, #ed6c02);">
        <div class="sdg-number">9</div>
        <div class="sdg-title">INDUSTRY, INNOVATION AND INFRASTRUCTURE</div>
        <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px;">
            <ul style="color: white; line-height: 1.8;">
                <li>Leverages cutting-edge AI technologies including LLMs and RAG</li>
                <li>Demonstrates innovative application of AI in healthcare</li>
                <li>Creates scalable digital infrastructure for mental health support</li>
                <li>Integrates FastAPI, Streamlit, Whisper, and Twilio technologies</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # SDG 10
    st.markdown("""
    <div class="sdg-card" style="background: linear-gradient(135deg, #e91e63, #c2185b);">
        <div class="sdg-number">10</div>
        <div class="sdg-title">REDUCED INEQUALITIES</div>
        <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px;">
            <ul style="color: white; line-height: 1.8;">
                <li>Provides free/affordable mental health support to underserved communities</li>
                <li>Breaks down geographical barriers - accessible anywhere with internet</li>
                <li>Reduces stigma through anonymous and private conversations</li>
                <li>Voice support for users with low literacy or visual impairments</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== TECHNICAL ARCHITECTURE =====
    st.markdown('<h2 class="section-title">🔧 Technical Architecture</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.15); backdrop-filter:blur(10px); border-radius:25px; padding:30px; margin:20px 0; border:1px solid rgba(255,255,255,0.3);">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center;">
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🖥️</div>
                <h4 style="color: white;">Frontend</h4>
                <p style="color: rgba(255,255,255,0.9);">Streamlit • Gradio</p>
            </div>
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 10px;">⚙️</div>
                <h4 style="color: white;">Backend</h4>
                <p style="color: rgba(255,255,255,0.9);">FastAPI • PostgreSQL</p>
            </div>
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🤖</div>
                <h4 style="color: white;">AI/ML</h4>
                <p style="color: rgba(255,255,255,0.9);">LLMs • RAG • XGBoost</p>
            </div>
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🎤</div>
                <h4 style="color: white;">Voice</h4>
                <p style="color: rgba(255,255,255,0.9);">Whisper • gTTS</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== TEAM SECTION =====
    st.markdown('<h2 class="section-title">👥 Development Team</h2>', unsafe_allow_html=True)
    
    team_cols = st.columns(4)
    
    with team_cols[0]:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👨‍🏫</div>
            <div class="team-name">Faisal Hussain</div>
            <div class="team-role">Supervisor</div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_cols[1]:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Safia Rasheed</div>
            <div class="team-role">BSCS-MC-215</div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_cols[2]:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Maria Akram</div>
            <div class="team-role">BSCS-MC-207</div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_cols[3]:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Shamsa Akram</div>
            <div class="team-role">BSCS-MC-208</div>
        </div>
        """, unsafe_allow_html=True)

    # ===== REFERENCES =====
    st.markdown('<h2 class="section-title">📚 References</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <ul style="color: white; line-height: 2.2; font-size:1.1rem;">
            <li>World Health Organization (WHO) - Mental Health Guidelines 2023</li>
            <li>American Psychological Association (APA) - Digital Health Standards</li>
            <li>Mayo Clinic - Verified Mental Health Resources</li>
            <li>T. Bickmore - Review of Healthcare Chatbots and their Limitations (2023)</li>
            <li>A. Miner - Study on Mental-Health Chatbot Safety and Emergency Gaps (2019)</li>
            <li>United Nations - Sustainable Development Goals (SDG) Report 2024</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ===== FOOTER =====
    st.markdown("""
    <div style="margin-top:60px; text-align:center; padding:30px; color:rgba(255,255,255,0.8); border-top:1px solid rgba(255,255,255,0.3);">
        <p>© 2026 Mind Care AI | National University of Modern Languages, Islamabad</p>
        <p style="font-size:0.8rem;">Final Year Project | Department of Computer Science</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about_page()