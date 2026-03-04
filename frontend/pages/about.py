import streamlit as st

def show_about_page():
    # Professional CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* White Background */
    .stApp {
        background: #ffffff;
    }
    
    /* Hide Streamlit Branding */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Main Container */
    .block-container {
        padding: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 50px 20px;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e293b, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    
    .hero-section p {
        color: #4a5568;
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.8;
    }
    
    /* Section Titles */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 50px 0 30px;
        color: #1e293b;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #818cf8);
        border-radius: 2px;
    }
    
    /* Mission Cards - Colors as they were */
    .mission-card-1 {
        background: #1e2a3a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #ff6b6b;
    }
    
    .mission-card-2 {
        background: #2a2a3a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #4ecdc4;
    }
    
    .mission-card-3 {
        background: #2a3a2a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #ffe66d;
    }
    
    .mission-card-1:hover, .mission-card-2:hover, .mission-card-3:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .mission-icon {
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .mission-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .mission-text {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    /* Architecture Cards - Colors as they were */
    .arch-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 30px 0;
    }
    
    .arch-item-1 {
        background: #162b38;
        border-radius: 15px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border-bottom: 3px solid #4facfe;
    }
    
    .arch-item-2 {
        background: #382b38;
        border-radius: 15px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border-bottom: 3px solid #a18cd1;
    }
    
    .arch-item-3 {
        background: #2b3838;
        border-radius: 15px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border-bottom: 3px solid #fbc2eb;
    }
    
    .arch-item-4 {
        background: #382b2b;
        border-radius: 15px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border-bottom: 3px solid #ff9a9e;
    }
    
    .arch-item-1:hover, .arch-item-2:hover, .arch-item-3:hover, .arch-item-4:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    }
    
    .arch-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .arch-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .arch-desc {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
    /* Flow Card */
    .flow-card {
        background: #f8f9fa;
        border-radius: 20px;
        padding: 30px;
        color: #1e293b;
        margin: 30px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    /* SDG Cards - Colors as they were */
    .sdg-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin: 30px 0;
    }
    
    .sdg-card-1 {
        background: #1a3a2a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        transition: all 0.4s ease;
        border-right: 5px solid #4ecdc4;
    }
    
    .sdg-card-2 {
        background: #2a2a3a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        transition: all 0.4s ease;
        border-right: 5px solid #ffe66d;
    }
    
    .sdg-card-3 {
        background: #3a1a2a;
        border-radius: 20px;
        padding: 30px;
        color: white;
        transition: all 0.4s ease;
        border-right: 5px solid #ff6b6b;
    }
    
    .sdg-card-1:hover, .sdg-card-2:hover, .sdg-card-3:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    .sdg-number {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .sdg-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .sdg-desc {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    /* Stats Cards - Colors as they were */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 40px 0;
    }
    
    .stat-card-1 {
        background: #162b38;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        border-top: 3px solid #4facfe;
    }
    
    .stat-card-2 {
        background: #2b2b38;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        border-top: 3px solid #a18cd1;
    }
    
    .stat-card-3 {
        background: #2b382b;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        border-top: 3px solid #fbc2eb;
    }
    
    .stat-card-4 {
        background: #382b2b;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        border-top: 3px solid #ff9a9e;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
    }
    
    /* Team Cards - Colors as they were */
    .team-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin: 30px 0;
    }
    
    .team-card-1 {
        background: #1e2a3a;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .team-card-2 {
        background: #2a1e2a;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .team-card-3 {
        background: #1e2a2a;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .team-card-1:hover, .team-card-2:hover, .team-card-3:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border-color: rgba(0, 0, 0, 0.1);
    }
    
    .team-avatar {
        font-size: 4rem;
        margin-bottom: 15px;
    }
    
    .team-name {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .team-id {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin-bottom: 10px;
    }
    
    .team-role {
        background: linear-gradient(135deg, #4f46e5, #818cf8);
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        color: white;
    }
    
    /* Supervisor Card */
    .supervisor-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: #1e293b;
        margin: 40px 0;
        border: 1px solid #e2e8f0;
        font-weight: 600;
    }
    
    /* References Card */
    .references-card {
        background: #f8f9fa;
        border-radius: 20px;
        padding: 30px;
        color: #1e293b;
        margin: 30px 0;
        border: 1px solid #e2e8f0;
    }
    
    .references-card li {
        color: #4a5568;
        margin-bottom: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= HERO SECTION =================
    st.markdown("""
    <div class="hero-section">
        <h1>About MindCareAI</h1>
        <p>A specialized AI-powered conversational assistant designed at NUML Islamabad to provide empathetic, accessible, and safe mental health support to individuals experiencing stress, anxiety, or emotional distress.</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= MISSION CARDS =================
    st.markdown('<div class="section-title">Our Mission</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="mission-card-1">
            <div class="mission-icon">🎯</div>
            <div class="mission-title">Accessible Support</div>
            <div class="mission-text">24/7 emotional support available to everyone, anywhere, without social stigma or barriers.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="mission-card-2">
            <div class="mission-icon">🔒</div>
            <div class="mission-title">Privacy First</div>
            <div class="mission-text">Bank-level encryption and secure PostgreSQL storage ensuring your conversations stay completely private.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="mission-card-3">
            <div class="mission-icon">🤖</div>
            <div class="mission-title">Advanced AI</div>
            <div class="mission-text">Powered by cutting-edge Transformer models, RAG architecture, and Whisper for voice interaction.</div>
        </div>
        """, unsafe_allow_html=True)

    # ================= SYSTEM ARCHITECTURE =================
    st.markdown('<div class="section-title">System Architecture</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="arch-grid">
        <div class="arch-item-1">
            <div class="arch-icon">🖥️</div>
            <div class="arch-title">Frontend</div>
            <div class="arch-desc">Streamlit + Gradio</div>
        </div>
        <div class="arch-item-2">
            <div class="arch-icon">⚙️</div>
            <div class="arch-title">Backend</div>
            <div class="arch-desc">FastAPI + PostgreSQL</div>
        </div>
        <div class="arch-item-3">
            <div class="arch-icon">🧠</div>
            <div class="arch-title">AI/ML</div>
            <div class="arch-desc">LLMs + RAG + XGBoost</div>
        </div>
        <div class="arch-item-4">
            <div class="arch-icon">🎤</div>
            <div class="arch-title">Voice</div>
            <div class="arch-desc">Whisper + gTTS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture Flow
    st.markdown("""
    <div class="flow-card">
        <h3 style="color: #1e293b; margin-bottom: 20px; text-align: center;">End-to-End Architecture Flow</h3>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="text-align: center; color: #4a5568;">
                <div style="font-size: 2rem;">📱</div>
                <div>User Interface</div>
            </div>
            <div style="font-size: 2rem; color: #4a5568;">→</div>
            <div style="text-align: center; color: #4a5568;">
                <div style="font-size: 2rem;">⚡</div>
                <div>FastAPI Backend</div>
            </div>
            <div style="font-size: 2rem; color: #4a5568;">→</div>
            <div style="text-align: center; color: #4a5568;">
                <div style="font-size: 2rem;">🧠</div>
                <div>AI Processing</div>
            </div>
            <div style="font-size: 2rem; color: #4a5568;">→</div>
            <div style="text-align: center; color: #4a5568;">
                <div style="font-size: 2rem;">🗄️</div>
                <div>Database</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= SDG GOALS =================
    st.markdown('<div class="section-title">UN Sustainable Development Goals</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sdg-container">
        <div class="sdg-card-1">
            <div class="sdg-number">3</div>
            <div class="sdg-title">Good Health</div>
            <div class="sdg-desc">Promoting mental well-being and accessible healthcare for all through AI-powered support.</div>
        </div>
        <div class="sdg-card-2">
            <div class="sdg-number">9</div>
            <div class="sdg-title">Innovation</div>
            <div class="sdg-desc">Leveraging cutting-edge AI and RAG technology for social welfare and mental health innovation.</div>
        </div>
        <div class="sdg-card-3">
            <div class="sdg-number">10</div>
            <div class="sdg-title">Reduced Inequalities</div>
            <div class="sdg-desc">Making mental healthcare accessible to underserved communities and breaking geographical barriers.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SDG Impact Summary
    st.markdown("""
    <div class="flow-card">
        <h3 style="color: #1e293b; margin-bottom: 20px;">📊 Our SDG Commitment</h3>
        <p style="color: #4a5568; line-height: 1.8;">
            Through MindCareAI, we actively contribute to the UN's 2030 Agenda by making mental health support accessible, 
            leveraging technological innovation, and reducing inequalities in healthcare access.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ================= KEY STATISTICS =================
    st.markdown('<div class="section-title">Impact Statistics</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card-1">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-card-2">
            <div class="stat-number">100%</div>
            <div class="stat-label">Anonymous</div>
        </div>
        <div class="stat-card-3">
            <div class="stat-number">50+</div>
            <div class="stat-label">Clinical Sources</div>
        </div>
        <div class="stat-card-4">
            <div class="stat-number">Real-time</div>
            <div class="stat-label">Crisis Detection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= TEAM SECTION =================
    st.markdown('<div class="section-title">Development Team</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="team-grid">
        <div class="team-card-1">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Safia Rasheed</div>
            <div class="team-id">BSCS-MC-215</div>
            <div class="team-role">Developer</div>
        </div>
        <div class="team-card-2">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Maria Akram</div>
            <div class="team-id">BSCS-MC-207</div>
            <div class="team-role">Developer</div>
        </div>
        <div class="team-card-3">
            <div class="team-avatar">👩‍💻</div>
            <div class="team-name">Shamsa Akram</div>
            <div class="team-id">BSCS-MC-208</div>
            <div class="team-role">Developer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Supervisor
    st.markdown("""
    <div class="supervisor-card">
        👨‍🏫 Supervised By: Faisal Hussain | Department of Computer Science, NUML Islamabad
    </div>
    """, unsafe_allow_html=True)

    # ================= REFERENCES =================
    st.markdown('<div class="section-title">References</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="references-card">
        <ul style="list-style-type: none; padding-left: 0;">
            <li>📚 World Health Organization (WHO) - Mental Health Guidelines 2023</li>
            <li>📚 American Psychological Association (APA) - Digital Health Standards</li>
            <li>📚 Mayo Clinic - Verified Mental Health Resources</li>
            <li>📚 T. Bickmore - Review of Healthcare Chatbots (2023)</li>
            <li>📚 A. Miner - Mental-Health Chatbot Safety Study (2019)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div class="footer">
        © 2026 MindCareAI | National University of Modern Languages, Islamabad<br>
        Final Year Project | Department of Computer Science
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about_page()