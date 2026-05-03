# about.py
import streamlit as st
from layout_utils import apply_clean_layout

def show_about_page():
    # Apply global layout – removes header/footer, sets zero top padding
    apply_clean_layout(hide_header_completely=True)
    
    # --- Top spacer to push content away from navbar buttons ---
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    
    # ===== Professional CSS =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0 !important;
            max-width: 1200px !important;
        }
        
        .stApp {
            background: #f6f7fb !important;
        }
        
        /* Main content background — matches MindCare design tokens */
        .main {
            background: #f6f7fb;
        }
        
        /* Professional animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Hero Section - Professional */
        .hero-section {
            background: linear-gradient(135deg, #1a3c5e 0%, #2c5f8a 50%, #1a3c5e 100%);
            border-radius: 16px;
            padding: 60px 40px;
            margin-bottom: 48px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .hero-content h1 {
            font-size: 2.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
        }
        
        .hero-content p {
            font-size: 1.1rem;
            color: #e0e7ff;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
        }
        
        /* Section Headings - Centered - NO LINE */
        .section-title {
            font-size: 1.75rem;
            font-weight: 600;
            color: #1e293b;
            margin: 48px 0 24px 0;
            text-align: center;
            letter-spacing: -0.01em;
        }
        
        /* Mission Cards with colors */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .mission-card {
            border-radius: 12px;
            padding: 28px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .mission-card-1 {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #93c5fd;
        }
        
        .mission-card-2 {
            background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
            border: 1px solid #a5b4fc;
        }
        
        .mission-card-3 {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border: 1px solid #7dd3fc;
        }
        
        .mission-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        }
        
        .mission-icon {
            font-size: 2.5rem;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .mission-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #0f172a;
        }
        
        .mission-text {
            color: #334155;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        /* Architecture Cards with colors */
        .arch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 32px 0;
        }
        
        .arch-item {
            border-radius: 12px;
            padding: 24px 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .arch-item-1 {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #93c5fd;
        }
        
        .arch-item-2 {
            background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
            border: 1px solid #a5b4fc;
        }
        
        .arch-item-3 {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border: 1px solid #7dd3fc;
        }
        
        .arch-item-4 {
            background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
            border: 1px solid #86efac;
        }
        
        .arch-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        }
        
        .arch-icon {
            font-size: 2rem;
            margin-bottom: 12px;
            display: inline-block;
        }
        
        .arch-title {
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
        }
        
        .arch-desc {
            color: #475569;
            font-size: 0.85rem;
        }
        
        /* Flow Card */
        .flow-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 32px;
            margin: 32px 0;
            border: 1px solid #cbd5e1;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .flow-card h3 {
            color: #1e293b;
            margin-bottom: 24px;
            font-size: 1.25rem;
            font-weight: 600;
        }
        
        .flow-steps {
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .flow-step {
            text-align: center;
            flex: 1;
            min-width: 100px;
        }
        
        .flow-icon {
            font-size: 2rem;
            margin-bottom: 8px;
        }
        
        .flow-label {
            font-size: 0.85rem;
            color: #475569;
            font-weight: 500;
        }
        
        .flow-arrow {
            font-size: 1.5rem;
            color: #94a3b8;
        }
        
        /* SDG Cards - No underline on text */
        .sdg-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .sdg-card {
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s ease;
            text-decoration: none !important;
            display: block;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .sdg-card-1 {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border: 1px solid #6ee7b7;
        }
        
        .sdg-card-2 {
            background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
            border: 1px solid #fb923c;
        }
        
        .sdg-card-3 {
            background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
            border: 1px solid #f9a8d4;
        }
        
        .sdg-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        }
        
        .sdg-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #065f46;
            margin-bottom: 12px;
            display: inline-block;
        }
        
        .sdg-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #0f172a;
        }
        
        .sdg-desc {
            color: #334155;
            line-height: 1.5;
            font-size: 0.9rem;
            margin-bottom: 16px;
        }
        
        .sdg-link {
            color: #2563eb;
            text-decoration: none !important;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        
        .sdg-link:hover {
            text-decoration: none !important;
            color: #1d4ed8;
        }
        
        .sdg-card a, .sdg-card a:hover {
            text-decoration: none !important;
        }
        
        /* Stats Cards with colors */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 32px 0;
        }
        
        .stat-card {
            border-radius: 12px;
            padding: 28px 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .stat-card-1 {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #93c5fd;
        }
        
        .stat-card-2 {
            background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
            border: 1px solid #a5b4fc;
        }
        
        .stat-card-3 {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border: 1px solid #7dd3fc;
        }
        
        .stat-card-4 {
            background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
            border: 1px solid #86efac;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #1e40af;
            margin-bottom: 8px;
        }
        
        .stat-label {
            color: #334155;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Team Cards with colors */
        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .team-card {
            border-radius: 12px;
            padding: 28px 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .team-card-1 {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #93c5fd;
        }
        
        .team-card-2 {
            background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
            border: 1px solid #a5b4fc;
        }
        
        .team-card-3 {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border: 1px solid #7dd3fc;
        }
        
        .team-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        }
        
        .team-avatar {
            font-size: 3rem;
            margin-bottom: 16px;
            display: inline-block;
        }
        
        .team-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 4px;
            color: #0f172a;
        }
        
        .team-id {
            color: #475569;
            font-size: 0.85rem;
            margin-bottom: 8px;
        }
        
        .team-role {
            background: #2c5f8a;
            display: inline-block;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            color: white;
        }
        
        /* Supervisor Card - Centered */
        .supervisor-card {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            border-radius: 12px;
            padding: 24px 32px;
            margin: 40px auto;
            border: 1px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            max-width: 700px;
            text-align: center;
        }
        
        .supervisor-icon {
            font-size: 2.5rem;
            background: #2c5f8a;
            border-radius: 50%;
            width: 64px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .supervisor-info {
            flex: 1;
            text-align: left;
        }
        
        .supervisor-name {
            font-size: 1.15rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 4px;
        }
        
        .supervisor-dept {
            color: #475569;
            font-size: 0.9rem;
            margin-top: 2px;
        }
        
        /* References Card */
        .references-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 28px;
            margin: 32px 0;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .references-card ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .references-card li {
            color: #334155;
            margin-bottom: 10px;
            font-size: 0.9rem;
        }
        
        .references-card li a {
            color: #2563eb;
            text-decoration: none;
        }
        
        .references-card li a:hover {
            text-decoration: underline;
        }
        
        /* Footer */
        .footer-container {
            background: #1e293b;
            color: #e2e8f0;
            padding: 48px 40px 24px 40px;
            margin-top: 60px;
            margin-left: -2rem;
            margin-right: -2rem;
            width: calc(100% + 4rem);
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 32px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer-title {
            font-weight: 600;
            margin-bottom: 16px;
            font-size: 0.9rem;
            color: #94a3b8;
            letter-spacing: 0.5px;
        }
        
        .footer-text {
            font-size: 0.85rem;
            color: #cbd5e1;
            margin-bottom: 8px;
            cursor: default;
        }
        
        .footer-bottom {
            text-align: center;
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.75rem;
            color: #64748b;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero-section {
                padding: 40px 24px;
            }
            .hero-content h1 {
                font-size: 1.75rem;
            }
            .section-title {
                font-size: 1.5rem;
            }
            .flow-steps {
                flex-direction: column;
            }
            .flow-arrow {
                transform: rotate(90deg);
            }
            .supervisor-card {
                flex-direction: column;
                text-align: center;
                max-width: 90%;
            }
            .supervisor-info {
                text-align: center;
            }
            .footer-container {
                margin-left: -1rem;
                margin-right: -1rem;
                width: calc(100% + 2rem);
                padding: 32px 20px 20px 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1>AI Assistant for Mental Health</h1>
            <p>An intelligent, compassionate companion designed to provide empathetic and personalized mental health support using cutting-edge artificial intelligence.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mission Section
    st.markdown('<div class="section-title">🎯 Our Mission</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cards-grid">
        <div class="mission-card mission-card-1">
            <div class="mission-icon">🎯</div>
            <div class="mission-title">Accessible Support</div>
            <div class="mission-text">24/7 AI-powered emotional support available to everyone, anywhere, breaking barriers and eliminating social stigma.</div>
        </div>
        <div class="mission-card mission-card-2">
            <div class="mission-icon">🔒</div>
            <div class="mission-title">Privacy First</div>
            <div class="mission-text">Enterprise-grade encryption and secure data storage ensuring your conversations remain completely private and confidential.</div>
        </div>
        <div class="mission-card mission-card-3">
            <div class="mission-icon">🤖</div>
            <div class="mission-title">Advanced AI</div>
            <div class="mission-text">Powered by state-of-the-art Transformer models, RAG architecture, and Whisper for natural voice interaction.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # System Architecture
    st.markdown('<div class="section-title">🏗️ System Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="arch-grid">
        <div class="arch-item arch-item-1"><div class="arch-icon">🖥️</div><div class="arch-title">Frontend</div><div class="arch-desc">Streamlit + Gradio</div></div>
        <div class="arch-item arch-item-2"><div class="arch-icon">⚙️</div><div class="arch-title">Backend</div><div class="arch-desc">FastAPI + PostgreSQL</div></div>
        <div class="arch-item arch-item-3"><div class="arch-icon">🧠</div><div class="arch-title">AI/ML</div><div class="arch-desc">LLMs + RAG + XGBoost</div></div>
        <div class="arch-item arch-item-4"><div class="arch-icon">🎤</div><div class="arch-title">Voice</div><div class="arch-desc">Whisper + gTTS</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture Flow
    st.markdown("""
    <div class="flow-card">
        <h3>🔄 End-to-End Data Flow</h3>
        <div class="flow-steps">
            <div class="flow-step"><div class="flow-icon">📱</div><div class="flow-label">User Interface</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">⚡</div><div class="flow-label">FastAPI Backend</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">🧠</div><div class="flow-label">AI Processing</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">🗄️</div><div class="flow-label">Database</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SDG Goals
    st.markdown('<div class="section-title">🌍 UN Sustainable Development Goals</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sdg-grid">
        <a href="https://sdgs.un.org/goals/goal3" target="_blank" class="sdg-card sdg-card-1">
            <div class="sdg-number">SDG 3</div>
            <div class="sdg-title">Good Health & Well-being</div>
            <div class="sdg-desc">Promoting mental well-being and accessible healthcare for all through AI-powered support.</div>
            <div class="sdg-link">🔗 Learn more about SDG 3 →</div>
        </a>
        <a href="https://sdgs.un.org/goals/goal9" target="_blank" class="sdg-card sdg-card-2">
            <div class="sdg-number">SDG 9</div>
            <div class="sdg-title">Industry, Innovation & Infrastructure</div>
            <div class="sdg-desc">Leveraging cutting-edge AI technology for social welfare and mental health innovation.</div>
            <div class="sdg-link">🔗 Learn more about SDG 9 →</div>
        </a>
        <a href="https://sdgs.un.org/goals/goal10" target="_blank" class="sdg-card sdg-card-3">
            <div class="sdg-number">SDG 10</div>
            <div class="sdg-title">Reduced Inequalities</div>
            <div class="sdg-desc">Making mental healthcare accessible to underserved communities worldwide.</div>
            <div class="sdg-link">🔗 Learn more about SDG 10 →</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Impact Statistics
    st.markdown('<div class="section-title">📊 Impact Statistics</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card stat-card-1"><div class="stat-number">24/7</div><div class="stat-label">Availability</div></div>
        <div class="stat-card stat-card-2"><div class="stat-number">100%</div><div class="stat-label">Anonymous</div></div>
        <div class="stat-card stat-card-3"><div class="stat-number">50+</div><div class="stat-label">Clinical Sources</div></div>
        <div class="stat-card stat-card-4"><div class="stat-number">Real-time</div><div class="stat-label">Crisis Detection</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Development Team
    st.markdown('<div class="section-title">👥 Development Team</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="team-grid">
        <div class="team-card team-card-1"><div class="team-avatar">👩‍💻</div><div class="team-name">Safia Rasheed</div><div class="team-id">BSCS-MC-215</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-2"><div class="team-avatar">👩‍💻</div><div class="team-name">Maria Akram</div><div class="team-id">BSCS-MC-207</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-3"><div class="team-avatar">👩‍💻</div><div class="team-name">Shamsa Akram</div><div class="team-id">BSCS-MC-208</div><div class="team-role">Developer</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Supervisor - Centered
    st.markdown("""
    <div style="display: flex; justify-content: center;">
        <div class="supervisor-card">
            <div class="supervisor-icon">👨‍🏫</div>
            <div class="supervisor-info">
                <div class="supervisor-name">Mr. Faisal Hussain</div>
                <div class="supervisor-dept">Project Supervisor | Department of Computer Science</div>
                <div class="supervisor-dept">National University of Modern Languages (NUML), Multan Campus</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # References
    st.markdown('<div class="section-title">📚 References & Resources</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="references-card">
        <ul>
            <li>📖 <a href="https://www.who.int/health-topics/mental-health" target="_blank">World Health Organization (WHO) - Mental Health Guidelines 2024</a></li>
            <li>📖 <a href="https://www.apa.org/topics/mental-health" target="_blank">American Psychological Association (APA) - Digital Health Standards</a></li>
            <li>📖 <a href="https://www.mayoclinic.org/healthy-lifestyle" target="_blank">Mayo Clinic - Verified Mental Health Resources</a></li>
            <li>📖 <a href="https://www.nimh.nih.gov/" target="_blank">National Institute of Mental Health (NIMH) - Research Publications</a></li>
            <li>📖 <a href="https://www.mentalhealth.gov/" target="_blank">MentalHealth.gov - Evidence-Based Practices</a></li>
            <li>📖 T. Bickmore - "Review of Healthcare Chatbots" (Journal of Medical Internet Research, 2023)</li>
            <li>📖 A. Miner - "Mental-Health Chatbot Safety Study" (JAMA Network, 2019)</li>
            <li>📖 <a href="https://arxiv.org/abs/2304.12210" target="_blank">Recent Advances in Mental Health AI - arXiv Research Paper</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer-container">
        <div class="footer-grid">
            <div class="footer-col">
                <div class="footer-title">About</div>
                <div class="footer-text">AI-powered emotional support</div>
                <div class="footer-text">24/7 mental wellness companion</div>
                <div class="footer-text">Evidence-based techniques</div>
                <div class="footer-text">Anonymous & secure</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Resources</div>
                <div class="footer-text">Mental Wellness Guide</div>
                <div class="footer-text">Coping Strategies</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Legal</div>
                <div class="footer-text">About</div>
                <div class="footer-text">Privacy Policy</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Contact</div>
                <div class="footer-text">AI Assistant for Mental Health</div>
                <div class="footer-text">support@aiassistant.com</div>
            </div>
        </div>
        <div class="footer-bottom">
            © 2026 AI Assistant for Mental Health — Your well-being matters 
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about_page()