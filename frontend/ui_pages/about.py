# about.py
import streamlit as st
from layout_utils import apply_clean_layout

def show_about_page():
    # Apply global layout – removes header/footer, sets zero top padding
    apply_clean_layout(hide_header_completely=True)
    
    # --- ADDED: Top spacer to push content away from navbar buttons ---
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

    # About page CSS (no layout overrides, only styling)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
    .stApp { background: #ffffff; }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #f0f9ff, #e6f0fa);
        border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .hero-section p {
        color: #334155;
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.7;
    }
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 60px 0 30px;
        color: #0f172a;
    }
    .mission-card {
        border-radius: 24px;
        padding: 30px;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
    }
    .mission-card-1 { background: #fff0f0; }
    .mission-card-2 { background: #e6f9f5; }
    .mission-card-3 { background: #fef9e3; }
    .mission-card:hover { transform: translateY(-5px); box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1); }
    .mission-icon { font-size: 3rem; margin-bottom: 20px; }
    .mission-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 15px; color: #0f172a; }
    .mission-text { color: #334155; line-height: 1.6; }
    
    .arch-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin: 30px 0; }
    .arch-item { border-radius: 20px; padding: 25px 20px; text-align: center; transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05); }
    .arch-item-1 { background: #e6f0ff; }
    .arch-item-2 { background: #f0e6ff; }
    .arch-item-3 { background: #ffe6f0; }
    .arch-item-4 { background: #e6fff0; }
    .arch-item:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1); }
    .arch-icon { font-size: 2.5rem; margin-bottom: 15px; }
    .arch-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 5px; color: #1e293b; }
    .arch-desc { color: #475569; font-size: 0.9rem; }
    
    .flow-card { background: #f8fafc; border-radius: 24px; padding: 30px; margin: 30px 0; border: 1px solid #e2e8f0; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03); text-align: center; }
    .flow-card h3 { color: #0f172a; margin-bottom: 20px; }
    
    .sdg-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin: 30px 0; }
    .sdg-card { border-radius: 24px; padding: 30px; transition: all 0.4s ease; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05); }
    .sdg-card-1 { background: #e6faf5; }
    .sdg-card-2 { background: #fff5e6; }
    .sdg-card-3 { background: #ffe6f5; }
    .sdg-card:hover { transform: translateY(-5px); box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1); }
    .sdg-number { font-size: 3rem; font-weight: 800; margin-bottom: 15px; color: #1e293b; }
    .sdg-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 15px; color: #0f172a; }
    .sdg-desc { color: #334155; line-height: 1.6; }
    
    .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin: 40px 0; }
    .stat-card { border-radius: 20px; padding: 25px; text-align: center; transition: all 0.2s ease; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05); }
    .stat-card-1 { background: #e6f0ff; }
    .stat-card-2 { background: #f0e6ff; }
    .stat-card-3 { background: #ffe6f0; }
    .stat-card-4 { background: #e6fff0; }
    .stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.08); }
    .stat-number { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
    .stat-label { color: #475569; font-size: 1rem; }
    
    .team-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin: 30px 0; }
    .team-card { border-radius: 24px; padding: 30px 20px; text-align: center; transition: all 0.3s ease; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05); }
    .team-card-1 { background: #eef2ff; }
    .team-card-2 { background: #fef3c7; }
    .team-card-3 { background: #e0f2fe; }
    .team-card:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1); }
    .team-avatar { font-size: 4rem; margin-bottom: 15px; }
    .team-name { font-size: 1.3rem; font-weight: 700; margin-bottom: 5px; color: #0f172a; }
    .team-id { color: #475569; font-size: 1rem; margin-bottom: 10px; }
    .team-role { background: linear-gradient(135deg, #4f46e5, #818cf8); display: inline-block; padding: 5px 18px; border-radius: 30px; font-size: 0.9rem; font-weight: 600; color: white; }
    
    .supervisor-card { background: #f1f5f9; border-radius: 20px; padding: 20px; text-align: center; margin: 40px 0; border: 1px solid #e2e8f0; font-weight: 500; color: #1e293b; font-size: 1.05rem; }
    .references-card { background: #f8fafc; border-radius: 24px; padding: 30px; margin: 30px 0; border: 1px solid #e2e8f0; }
    .references-card li { color: #475569; margin-bottom: 12px; line-height: 1.5; }
    .footer { text-align: center; padding: 30px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 60px; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

    # Page content
    st.markdown("""
    <div class="hero-section">
        <h1>About MindCareAI</h1>
        <p>A specialized AI-powered conversational assistant designed at NUML Multan to provide empathetic, accessible, and safe mental health support to individuals experiencing stress, anxiety, or emotional distress.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Our Mission</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="mission-card mission-card-1"><div class="mission-icon">🎯</div><div class="mission-title">Accessible Support</div><div class="mission-text">24/7 emotional support available to everyone, anywhere, without social stigma or barriers.</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="mission-card mission-card-2"><div class="mission-icon">🔒</div><div class="mission-title">Privacy First</div><div class="mission-text">Bank-level encryption and secure PostgreSQL storage ensuring your conversations stay completely private.</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="mission-card mission-card-3"><div class="mission-icon">🤖</div><div class="mission-title">Advanced AI</div><div class="mission-text">Powered by cutting-edge Transformer models, RAG architecture, and Whisper for voice interaction.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">System Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="arch-grid">
        <div class="arch-item arch-item-1"><div class="arch-icon">🖥️</div><div class="arch-title">Frontend</div><div class="arch-desc">Streamlit + Gradio</div></div>
        <div class="arch-item arch-item-2"><div class="arch-icon">⚙️</div><div class="arch-title">Backend</div><div class="arch-desc">FastAPI + PostgreSQL</div></div>
        <div class="arch-item arch-item-3"><div class="arch-icon">🧠</div><div class="arch-title">AI/ML</div><div class="arch-desc">LLMs + RAG + XGBoost</div></div>
        <div class="arch-item arch-item-4"><div class="arch-icon">🎤</div><div class="arch-title">Voice</div><div class="arch-desc">Whisper + gTTS</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="flow-card">
        <h3>End-to-End Architecture Flow</h3>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="text-align: center;"><div style="font-size: 2rem;">📱</div><div>User Interface</div></div>
            <div style="font-size: 2rem; color: #94a3b8;">→</div>
            <div style="text-align: center;"><div style="font-size: 2rem;">⚡</div><div>FastAPI Backend</div></div>
            <div style="font-size: 2rem; color: #94a3b8;">→</div>
            <div style="text-align: center;"><div style="font-size: 2rem;">🧠</div><div>AI Processing</div></div>
            <div style="font-size: 2rem; color: #94a3b8;">→</div>
            <div style="text-align: center;"><div style="font-size: 2rem;">🗄️</div><div>Database</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">UN Sustainable Development Goals</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sdg-container">
        <div class="sdg-card sdg-card-1"><div class="sdg-number">3</div><div class="sdg-title">Good Health</div><div class="sdg-desc">Promoting mental well-being and accessible healthcare for all through AI-powered support.</div></div>
        <div class="sdg-card sdg-card-2"><div class="sdg-number">9</div><div class="sdg-title">Innovation</div><div class="sdg-desc">Leveraging cutting-edge AI and RAG technology for social welfare and mental health innovation.</div></div>
        <div class="sdg-card sdg-card-3"><div class="sdg-number">10</div><div class="sdg-title">Reduced Inequalities</div><div class="sdg-desc">Making mental healthcare accessible to underserved communities and breaking geographical barriers.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Impact Statistics</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card stat-card-1"><div class="stat-number">24/7</div><div class="stat-label">Availability</div></div>
        <div class="stat-card stat-card-2"><div class="stat-number">100%</div><div class="stat-label">Anonymous</div></div>
        <div class="stat-card stat-card-3"><div class="stat-number">50+</div><div class="stat-label">Clinical Sources</div></div>
        <div class="stat-card stat-card-4"><div class="stat-number">Real-time</div><div class="stat-label">Crisis Detection</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Development Team</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="team-grid">
        <div class="team-card team-card-1"><div class="team-avatar">👩‍💻</div><div class="team-name">Safia Rasheed</div><div class="team-id">BSCS-MC-215</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-2"><div class="team-avatar">👩‍💻</div><div class="team-name">Maria Akram</div><div class="team-id">BSCS-MC-207</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-3"><div class="team-avatar">👩‍💻</div><div class="team-name">Shamsa Akram</div><div class="team-id">BSCS-MC-208</div><div class="team-role">Developer</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="supervisor-card">
        👨‍🏫 Supervised By: <strong>Faisal Hussain</strong> | Department of Computer Science, NUML Multan Campus
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div class="footer">
        © 2026 MindCareAI | National University of Modern Languages, Multan Campus<br>
        Final Year Project | Department of Computer Science
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about_page()