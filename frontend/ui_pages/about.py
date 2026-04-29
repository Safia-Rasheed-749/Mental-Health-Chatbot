# about.py
import streamlit as st
from layout_utils import apply_clean_layout
import base64
import os

def show_about_page():
    # Apply global layout – removes header/footer, sets zero top padding
    apply_clean_layout(hide_header_completely=True)
    
    # --- ADDED: Top spacer to push content away from navbar buttons ---
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    
    # ===== CSS (SAFE - NO NAVBAR BREAK) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding-top: 1.8rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # About page CSS with animations and professional styling
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
    
    .stApp {{ background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%); }}
    
    /* Animations */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-40px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(40px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes zoomIn {{
        from {{
            opacity: 0;
            transform: scale(0.9);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes shine {{
        0% {{ background-position: -100% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    /* Hero Section with Animated Gradient Background */
    .hero-section {{
        position: relative;
        text-align: center;
        padding: 80px 20px;
        margin-bottom: 40px;
        border-radius: 30px;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
        min-height: 450px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite, fadeInUp 0.8s ease-out;
        box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
        color: white;
        max-width: 800px;
        margin: 0 auto;
    }}
    
    .hero-section h1 {{
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        animation: fadeInUp 0.8s ease-out;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }}
    
    .hero-section p {{
        font-size: 1.2rem;
        line-height: 1.7;
        color: white;
        animation: fadeInUp 0.8s ease-out 0.2s both;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
    }}
    
    .section-title {{
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 60px 0 30px;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        display: inline-block;
        width: 100%;
    }}
    
    
    /* Mission Cards - Equal Height Fixed */
    .row-container {{
        display: flex;
        gap: 25px;
        margin: 30px 0;
        flex-wrap: wrap;
    }}
    
    .mission-card {{
        flex: 1;
        min-width: 250px;
        border-radius: 24px;
        padding: 30px 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        animation: fadeInUp 0.8s ease-out;
        display: flex;
        flex-direction: column;
        height: 320px;
        position: relative;
        overflow: hidden;
    }}
    
    .mission-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }}
    
    .mission-card:hover::before {{
        left: 100%;
    }}
    
    .mission-card-1 {{ background: linear-gradient(135deg, #e0f2fe, #bae6fd); }}
    .mission-card-2 {{ background: linear-gradient(135deg, #e0e7ff, #c7d2fe); }}
    .mission-card-3 {{ background: linear-gradient(135deg, #f3e8ff, #e9d5ff); }}
    .mission-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 30px rgba(0, 0, 0, 0.15); }}
    .mission-icon {{ font-size: 3rem; margin-bottom: 20px; display: inline-block; animation: pulse 3s ease-in-out infinite; }}
    .mission-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 15px; color: #0f172a; }}
    .mission-text {{ color: #334155; line-height: 1.6; flex: 1; }}
    
    /* Architecture Grid - Equal Height */
    .arch-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin: 30px 0; }}
    .arch-item {{ border-radius: 20px; padding: 25px 20px; text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05); height: 180px; display: flex; flex-direction: column; justify-content: center; position: relative; overflow: hidden; }}
    .arch-item-1 {{ background: linear-gradient(135deg, #dbeafe, #bfdbfe); }}
    .arch-item-2 {{ background: linear-gradient(135deg, #e0e7ff, #c7d2fe); }}
    .arch-item-3 {{ background: linear-gradient(135deg, #f3e8ff, #e9d5ff); }}
    .arch-item-4 {{ background: linear-gradient(135deg, #dcfce7, #bbf7d0); }}
    .arch-item:hover {{ transform: translateY(-6px) scale(1.02); box-shadow: 0 15px 25px rgba(0, 0, 0, 0.12); }}
    .arch-icon {{ font-size: 2.5rem; margin-bottom: 15px; display: inline-block; }}
    .arch-title {{ font-size: 1.2rem; font-weight: 600; margin-bottom: 5px; color: #1e293b; }}
    .arch-desc {{ color: #475569; font-size: 0.9rem; }}
    
    /* Flow Card */
    .flow-card {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border-radius: 24px; padding: 30px; margin: 30px 0; border: 1px solid rgba(102, 126, 234, 0.2); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05); text-align: center; animation: fadeInUp 0.8s ease-out; transition: all 0.3s ease; }}
    .flow-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1); }}
    .flow-card h3 {{ color: #0f172a; margin-bottom: 20px; font-size: 1.8rem; }}
    
    /* SDG Cards - Equal Height */
    .sdg-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin: 30px 0; }}
    .sdg-card {{ border-radius: 24px; padding: 30px; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05); animation: fadeInUp 0.8s ease-out; text-decoration: none !important; display: flex; flex-direction: column; height: 340px; cursor: pointer; position: relative; overflow: hidden; }}
    .sdg-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }}
    .sdg-card:hover::before {{
        left: 100%;
    }}
    .sdg-card-1 {{ background: linear-gradient(135deg, #d1fae5, #a7f3d0); }}
    .sdg-card-2 {{ background: linear-gradient(135deg, #fed7aa, #fdba74); }}
    .sdg-card-3 {{ background: linear-gradient(135deg, #fce7f3, #fbcfe8); }}
    .sdg-card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 30px rgba(0, 0, 0, 0.12); }}
    .sdg-number {{ font-size: 3rem; font-weight: 800; margin-bottom: 15px; color: #1e293b; }}
    .sdg-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 15px; color: #0f172a; text-decoration: none !important; }}
    .sdg-desc {{ color: #334155; line-height: 1.6; flex: 1; }}
    .sdg-link {{ color: #4f46e5; text-decoration: none !important; font-weight: 600; display: inline-block; margin-top: 15px; transition: all 0.3s ease; }}
    .sdg-link:hover {{ color: #7c3aed; transform: translateX(5px); text-decoration: none !important; }}
    
    /* Stats Cards - Equal Height */
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin: 40px 0; }}
    .stat-card {{ border-radius: 20px; padding: 25px; text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05); animation: zoomIn 0.6s ease-out; height: 140px; display: flex; flex-direction: column; justify-content: center; }}
    .stat-card-1 {{ background: linear-gradient(135deg, #dbeafe, #bfdbfe); }}
    .stat-card-2 {{ background: linear-gradient(135deg, #e0e7ff, #c7d2fe); }}
    .stat-card-3 {{ background: linear-gradient(135deg, #f3e8ff, #e9d5ff); }}
    .stat-card-4 {{ background: linear-gradient(135deg, #dcfce7, #bbf7d0); }}
    .stat-card:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.12); }}
    .stat-number {{ font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; }}
    .stat-label {{ color: #475569; font-size: 1rem; font-weight: 500; }}
    
    /* Team Cards - Equal Height */
    .team-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin: 30px 0; }}
    .team-card {{ border-radius: 24px; padding: 30px 20px; text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05); animation: fadeInUp 0.8s ease-out; height: 300px; display: flex; flex-direction: column; justify-content: center; }}
    .team-card-1 {{ background: linear-gradient(135deg, #e0e7ff, #c7d2fe); }}
    .team-card-2 {{ background: linear-gradient(135deg, #fef3c7, #fde68a); }}
    .team-card-3 {{ background: linear-gradient(135deg, #e0f2fe, #bae6fd); }}
    .team-card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 30px rgba(0, 0, 0, 0.12); }}
    .team-avatar {{ font-size: 4rem; margin-bottom: 15px; display: inline-block; animation: pulse 3s ease-in-out infinite; }}
    .team-name {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 5px; color: #0f172a; }}
    .team-id {{ color: #475569; font-size: 1rem; margin-bottom: 10px; }}
    .team-role {{ background: linear-gradient(135deg, #667eea, #764ba2); display: inline-block; padding: 5px 18px; border-radius: 30px; font-size: 0.9rem; font-weight: 600; color: white; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3); transition: all 0.3s ease; }}
    .team-role:hover {{ transform: scale(1.05); }}
    
    /* Supervisor Card */
    .supervisor-card {{ background: linear-gradient(135deg, #f1f5f9, #e2e8f0); border-radius: 20px; padding: 25px; text-align: center; margin: 40px 0; border: 1px solid rgba(102, 126, 234, 0.3); font-weight: 500; color: #1e293b; font-size: 1.05rem; transition: all 0.3s ease; animation: fadeInUp 0.8s ease-out; display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap; }}
    .supervisor-card:hover {{ transform: scale(1.01); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); }}
    .supervisor-icon {{ font-size: 3.5rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; padding: 10px; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; color: white; animation: pulse 2s ease-in-out infinite; }}
    .supervisor-info {{ text-align: left; }}
    .supervisor-name {{ font-size: 1.3rem; font-weight: 700; color: #0f172a; }}
    .supervisor-dept {{ color: #475569; font-size: 1rem; margin-top: 5px; }}
    
    /* References Card */
    .references-card {{ background: linear-gradient(135deg, #f8fafc, #f1f5f9); border-radius: 24px; padding: 30px; margin: 30px 0; border: 1px solid #e2e8f0; transition: all 0.3s ease; animation: fadeInUp 0.8s ease-out; }}
    .references-card:hover {{ box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08); transform: translateY(-3px); }}
    .references-card ul li {{ color: #475569; margin-bottom: 12px; line-height: 1.5; transition: transform 0.2s ease; padding: 8px 0; border-bottom: 1px solid #e2e8f0; list-style: none; }}
    .references-card ul li:hover {{ transform: translateX(5px); color: #667eea; }}
    .references-card ul li a {{ color: #4f46e5; text-decoration: none; font-weight: 500; transition: color 0.3s ease; }}
    .references-card ul li a:hover {{ text-decoration: underline; color: #7c3aed; }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .arch-grid, .stats-grid, .team-grid, .sdg-container {{ grid-template-columns: 1fr; gap: 15px; }}
        .row-container {{ flex-direction: column; }}
        .hero-section h1 {{ font-size: 2rem; }}
        .section-title {{ font-size: 1.8rem; }}
        .supervisor-card {{ flex-direction: column; text-align: center; }}
        .supervisor-info {{ text-align: center; }}
        .hero-section {{ padding: 50px 20px; min-height: 350px; }}
        .mission-card, .arch-item, .sdg-card, .stat-card, .team-card {{ height: auto; min-height: auto; }}
    }}
    
    /* Footer Styles */
    .footer-container {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: white;
        padding: 60px 40px 30px 40px;
        margin-top: 60px;
        margin-bottom: 0;
        margin-left: -2rem;
        margin-right: -2rem;
        width: calc(100% + 4rem);
        border-radius: 0;
    }}
    
    @media (max-width: 768px) {{
        .footer-container {{
            margin-left: -1rem;
            margin-right: -1rem;
            width: calc(100% + 2rem);
            padding: 60px 20px 30px 20px;
        }}
    }}
    
    .footer-grid {{
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 30px;
    }}
    
    .footer-col {{
        flex: 1;
        min-width: 200px;
    }}
    
    .footer-title {{
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 18px;
        background: linear-gradient(135deg, #a5b4fc 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }}
    
    .footer-text {{
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: block;
    }}
    
    .footer-text:hover {{
        color: #a5b4fc;
        transform: translateX(5px);
    }}
    
    .footer-bottom {{
        text-align: center;
        margin-top: 50px;
        padding-top: 30px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 13px;
        color: #94a3b8;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Hero section with animated gradient background
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1>🧠 AI Assistant for Mental Health</h1>
            <p>Your intelligent, compassionate companion designed to provide empathetic, accessible, and personalized mental health support using cutting-edge artificial intelligence technology.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🎯 Our Mission</div>', unsafe_allow_html=True)
    
    # Mission cards with equal height using flex row
    st.markdown("""
    <div class="row-container">
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

    st.markdown('<div class="section-title">🏗️ System Architecture</div>', unsafe_allow_html=True)
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
        <h3>🔄 End-to-End Architecture Flow</h3>
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

    st.markdown('<div class="section-title">🌍 UN Sustainable Development Goals</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sdg-container">
        <a href="https://sdgs.un.org/goals/goal3" target="_blank" class="sdg-card sdg-card-1">
            <div class="sdg-number">3</div>
            <div class="sdg-title">Good Health & Well-being</div>
            <div class="sdg-desc">Promoting mental well-being and accessible healthcare for all through AI-powered support.</div>
            <div class="sdg-link">🔗 Learn more about SDG 3 →</div>
        </a>
        <a href="https://sdgs.un.org/goals/goal9" target="_blank" class="sdg-card sdg-card-2">
            <div class="sdg-number">9</div>
            <div class="sdg-title">Industry, Innovation & Infrastructure</div>
            <div class="sdg-desc">Leveraging cutting-edge AI and RAG technology for social welfare and mental health innovation.</div>
            <div class="sdg-link">🔗 Learn more about SDG 9 →</div>
        </a>
        <a href="https://sdgs.un.org/goals/goal10" target="_blank" class="sdg-card sdg-card-3">
            <div class="sdg-number">10</div>
            <div class="sdg-title">Reduced Inequalities</div>
            <div class="sdg-desc">Making mental healthcare accessible to underserved communities and breaking geographical barriers.</div>
            <div class="sdg-link">🔗 Learn more about SDG 10 →</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Impact Statistics</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card stat-card-1"><div class="stat-number">24/7</div><div class="stat-label">Availability</div></div>
        <div class="stat-card stat-card-2"><div class="stat-number">100%</div><div class="stat-label">Anonymous</div></div>
        <div class="stat-card stat-card-3"><div class="stat-number">50+</div><div class="stat-label">Clinical Sources</div></div>
        <div class="stat-card stat-card-4"><div class="stat-number">Real-time</div><div class="stat-label">Crisis Detection</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">👥 Development Team</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="team-grid">
        <div class="team-card team-card-1"><div class="team-avatar">👩‍💻</div><div class="team-name">Safia Rasheed</div><div class="team-id">BSCS-MC-215</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-2"><div class="team-avatar">👩‍💻</div><div class="team-name">Maria Akram</div><div class="team-id">BSCS-MC-207</div><div class="team-role">Developer</div></div>
        <div class="team-card team-card-3"><div class="team-avatar">👩‍💻</div><div class="team-name">Shamsa Akram</div><div class="team-id">BSCS-MC-208</div><div class="team-role">Developer</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="supervisor-card">
        <div class="supervisor-icon">👨‍🏫</div>
        <div class="supervisor-info">
            <div class="supervisor-name">Mr. Faisal Hussain</div>
            <div class="supervisor-dept">Project Supervisor | Department of Computer Science</div>
            <div class="supervisor-dept">National University of Modern Languages (NUML), Multan Campus</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📚 References & Resources</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="references-card">
        <ul style="list-style-type: none; padding-left: 0;">
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
                <div class="footer-title">About AI Assistant</div>
                <div class="footer-text">AI-powered emotional support</div>
                <div class="footer-text">24/7 mental wellness companion</div>
                <div class="footer-text">Evidence-based techniques</div>
                <div class="footer-text">Anonymous & secure</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Resources</div>
                <div class="footer-text">Mental Wellness Guide</div>
                <div class="footer-text">Coping Strategies</div>
                <div class="footer-text">Emergency Helplines</div>
                <div class="footer-text">Research & Articles</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Support</div>
                <div class="footer-text">Privacy Policy</div>
                <div class="footer-text">About</div>
            </div>
            <div class="footer-col">
                <div class="footer-title">Contact</div>
                <div class="footer-text">AI Assistant for Mental Health</div>
                <div class="footer-text">Email: support@aiassistant.com</div>
                <div class="footer-text">NUML Multan Campus</div>
            </div>
        </div>
        <div class="footer-bottom">
            © 2026 AI Assistant for Mental Health — Your well-being matters 💙
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 0px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_about_page()