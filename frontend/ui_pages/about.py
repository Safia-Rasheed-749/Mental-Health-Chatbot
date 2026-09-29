import streamlit as st
from layout_utils import apply_clean_layout


def render_global_footer():
    st.markdown("""
        <style>
        .main .block-container {
            padding-bottom: 0rem !important;
            margin-bottom: 0rem !important;
        }
        .universal-footer-container {
            width: 100vw !important;
            position: relative !important;
            left: 50% !important;
            right: 50% !important;
            margin-left: -50vw !important;
            margin-right: -50vw !important;
            margin-bottom: -6rem !important;
            margin-top: 50px !important;
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            padding: 40px 0px 20px 0px !important;
            border-radius: 0px !important;
            box-sizing: border-box !important;
        }
        .footer-content-inner {
            max-width: 1200px; margin: 0 auto; padding: 0 30px;
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 24px;
        }
        .footer-sec-head { color: #FFFFFF !important; font-size: 1.05rem !important; font-weight: 700 !important; margin-bottom: 12px !important; }
        .footer-sec-text { color: #94A3B8 !important; font-size: 0.88rem !important; line-height: 1.7 !important; margin: 4px 0 !important; }
        .footer-copyright { max-width: 1200px; margin: 30px auto 0; padding: 18px 30px 0; border-top: 1px solid #334155; text-align: center; color: #64748B; font-size: 0.82rem; }
        </style>
        <div class="universal-footer-container">
          <div class="footer-content-inner">
            <div><div class="footer-sec-head">About AI Assistant</div><div class="footer-sec-text">AI-powered emotional support</div><div class="footer-sec-text">24/7 mental wellness companion</div><div class="footer-sec-text">Evidence-based techniques</div><div class="footer-sec-text">Anonymous &amp; secure</div></div>
            <div><div class="footer-sec-head">Resources</div><div class="footer-sec-text">Mental Wellness Guide</div><div class="footer-sec-text">Coping Strategies</div><div class="footer-sec-text">Research &amp; Articles</div></div>
            <div><div class="footer-sec-head">Support</div><div class="footer-sec-text">Privacy Policy</div><div class="footer-sec-text">About</div></div>
            <div><div class="footer-sec-head">Contact</div><div class="footer-sec-text">AI Assistant for Mental Health</div><div class="footer-sec-text">Email: support@aiassistant.com</div></div>
          </div>
          <div class="footer-copyright">© 2026 MindCareAI — Your well-being matters</div>
        </div>
    """, unsafe_allow_html=True)


def show_about_page():
    apply_clean_layout(hide_header_completely=True)

    st.markdown(
        """
        <style>
          header,footer,.stDeployButton{display:none!important}
          .main .block-container{max-width:1200px!important;padding:5rem 2rem 0!important;overflow:visible!important}
          .stApp,.main{background:linear-gradient(180deg,#F8FAFC 0%,#F4F3FF 100%)!important}
          .about-hero{padding:clamp(32px,6vw,58px) 28px;border-radius:26px;text-align:center;color:#fff;
            background:linear-gradient(135deg,#1E1B4B 0%,#312E81 52%,#6366F1 100%);
            box-shadow:0 18px 48px rgba(49,46,129,.2);margin:0 0 42px}
          .about-hero h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:750;letter-spacing:-.035em;color:#fff!important;margin:0 0 14px}
          .about-hero p{font-size:1.08rem;line-height:1.7;color:#E0E7FF;max-width:800px;margin:0 auto}
          .section-title{text-align:center;color:#1E1B4B;font-size:1.8rem;font-weight:750;letter-spacing:-.025em;margin:42px 0 22px}
          .mission-grid,.arch-grid,.sdg-grid,.team-grid{display:grid;gap:18px;margin:0 0 28px}
          .mission-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
          .arch-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
          .sdg-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
          .team-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
          .about-card,.team-card,.flow-card,.references-card{background:rgba(255,255,255,.86);backdrop-filter:blur(12px);
            border:1px solid #E2E8F0;border-radius:20px;box-shadow:0 8px 26px rgba(15,23,42,.055);}
          .about-card{height:100%;box-sizing:border-box;padding:26px 24px;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
          .about-card:hover,.team-card:hover{transform:translateY(-3px);border-color:#C7D2FE;box-shadow:0 14px 32px rgba(99,102,241,.12)}
          .mission-card{min-height:210px}
          .icon-box{display:grid;place-items:center;width:50px;height:50px;border-radius:16px;background:#EEF2FF;color:#6366F1;font-size:25px;margin-bottom:16px}
          .card-title{font-size:1.18rem;font-weight:700;color:#1E1B4B;margin-bottom:9px}
          .card-desc{font-size:.94rem;color:#4B5563;line-height:1.6}
          .arch-card{text-align:center;padding:22px 16px}
          .arch-card .icon-box{margin:0 auto 12px}
          .flow-card{padding:25px;margin:10px 0 34px;text-align:center}
          .flow-card h3{font-size:1.2rem;color:#1E1B4B;margin:0 0 18px}
          .flow-steps{display:flex;justify-content:center;align-items:center;gap:18px;flex-wrap:wrap;color:#475569;font-size:.92rem}
          .flow-step{padding:12px 16px;border-radius:14px;background:#F8FAFC;border:1px solid #E2E8F0}
          .flow-arrow{color:#6366F1;font-weight:800}
          .sdg-card{height:100%;box-sizing:border-box;padding:24px;border-radius:20px;border:1px solid;display:block;text-decoration:none!important;transition:transform .2s ease,box-shadow .2s ease}
          .sdg-card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(15,23,42,.1)}
          .sdg-card-3{background:linear-gradient(135deg,#ECFDF5,#D1FAE5);border-color:#A7F3D0}
          .sdg-card-9{background:linear-gradient(135deg,#FFF7ED,#FFEDD5);border-color:#FED7AA}
          .sdg-card-10{background:linear-gradient(135deg,#FDF2F8,#FCE7F3);border-color:#FBCFE8}
          .sdg-card h3{font-size:1.35rem;margin:0 0 7px}
          .sdg-card h4{font-size:1rem;margin:0 0 10px}
          .sdg-card p{font-size:.92rem;line-height:1.55;margin:0}
          .sdg-link{display:block;margin-top:14px;font-size:.85rem;font-weight:650}
          .team-card{text-align:center;padding:28px 18px;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
          .team-avatar{font-size:2.7rem;margin-bottom:10px}
          .team-name{font-size:1.12rem;font-weight:700;color:#1E1B4B;margin-bottom:4px}
          .team-id{font-size:.87rem;color:#6B7280;margin-bottom:12px}
          .team-role{display:inline-block;background:#EEF2FF;color:#4F46E5;padding:5px 14px;border-radius:999px;font-size:.82rem;font-weight:650}
          .supervisor-card{display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;max-width:760px;margin:28px auto;padding:22px;border-radius:20px;background:#fff;border:1px solid #E2E8F0;box-shadow:0 6px 20px rgba(15,23,42,.05);text-align:center}
          .supervisor-icon{display:grid;place-items:center;width:58px;height:58px;border-radius:18px;background:#EEF2FF;font-size:28px}
          .supervisor-name{font-weight:700;color:#1E1B4B;font-size:1.08rem}
          .supervisor-dept{color:#64748B;font-size:.9rem;line-height:1.5;margin-top:3px}
          .references-card{padding:25px 28px;margin:0 0 30px}
          .references-card ul{padding-left:22px;margin:0}
          .references-card li{color:#475569;margin:0 0 10px;font-size:.91rem;line-height:1.5}
          .references-card li:last-child{margin-bottom:0}
          .references-card a{color:#4F46E5;text-decoration:none}
          .references-card a:hover{text-decoration:underline}
          .site-footer{position:relative;width:100vw;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;background:#0F172A;color:#F8FAFC;padding:50px 0 25px;border-radius:0;box-sizing:border-box;margin-top:28px;margin-bottom:-5rem}
          .site-footer-grid{max-width:1160px;margin:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
          .site-footer-title{font-size:.85rem;font-weight:700;color:#A5B4FC;margin-bottom:12px;letter-spacing:.04em}
          .site-footer-text{font-size:.83rem;color:#CBD5E1;margin:0 0 7px;line-height:1.4}
          .site-footer-bottom{text-align:center;border-top:1px solid rgba(255,255,255,.12);margin-top:26px;padding:18px 0 0;font-size:.75rem;color:#94A3B8}
          .stats-footer{margin:20px 0 0;padding:35px 20px;background:#fff;border:1px solid #E2E8F0;border-radius:20px;box-shadow:0 4px 20px rgba(0,0,0,.04);color:#1E1B4B;box-sizing:border-box}
          .stats-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
          .stat-item{text-align:center;padding:8px}
          .stat-number{font-size:clamp(1.8rem,3vw,2.5rem);font-weight:850;line-height:1.15;margin-bottom:7px;color:#4338CA}
          .stat-label{font-size:.79rem;color:#6B7280;font-weight:600;text-transform:uppercase;letter-spacing:.08em}
          @media(max-width:760px){.main .block-container{padding:5rem 1rem 0!important}.mission-grid,.sdg-grid{grid-template-columns:1fr}.arch-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.team-grid{grid-template-columns:1fr}.stats-inner{grid-template-columns:repeat(2,minmax(0,1fr))}.site-footer-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.section-title{font-size:1.5rem}}
          @media(max-width:440px){.stats-inner,.site-footer-grid{grid-template-columns:1fr}.flow-steps{gap:8px}.flow-arrow{transform:rotate(90deg)}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    <section class="about-hero">
      <h1>AI Assistant for Mental Health</h1>
      <p>An intelligent, compassionate companion designed to provide empathetic and personalized mental health support using cutting-edge artificial intelligence.</p>
    </section>
    <h2 class="section-title">🎯 Our Mission</h2>
    <div class="mission-grid">
      <article class="about-card mission-card"><div class="icon-box">🎯</div><div class="card-title">Accessible Support</div><div class="card-desc">24/7 AI-powered emotional support available to everyone, anywhere, breaking barriers and eliminating social stigma.</div></article>
      <article class="about-card mission-card"><div class="icon-box">🔒</div><div class="card-title">Privacy First</div><div class="card-desc">Enterprise-grade encryption and secure data storage ensuring your conversations remain completely private and confidential.</div></article>
      <article class="about-card mission-card"><div class="icon-box">🤖</div><div class="card-title">Advanced AI</div><div class="card-desc">Powered by state-of-the-art Transformer models, RAG architecture, and Whisper for natural voice interaction.</div></article>
    </div>
    <h2 class="section-title">🏗️ System Architecture</h2>
    <div class="arch-grid">
      <article class="about-card arch-card"><div class="icon-box">🖥️</div><div class="card-title">Frontend</div><div class="card-desc"><b>Streamlit + Gradio</b></div></article>
      <article class="about-card arch-card"><div class="icon-box">⚙️</div><div class="card-title">Backend</div><div class="card-desc"><b>FastAPI + PostgreSQL</b></div></article>
      <article class="about-card arch-card"><div class="icon-box">🧠</div><div class="card-title">AI / ML</div><div class="card-desc"><b>LLMs + RAG + XGBoost</b></div></article>
      <article class="about-card arch-card"><div class="icon-box">🎤</div><div class="card-title">Voice</div><div class="card-desc"><b>Whisper + gTTS</b></div></article>
    </div>
    <section class="flow-card"><h3>🔄 End-to-End Data Flow</h3><div class="flow-steps">
      <div class="flow-step">📱 <b>User Interface</b></div><span class="flow-arrow">➔</span>
      <div class="flow-step">⚡ <b>FastAPI Backend</b></div><span class="flow-arrow">➔</span>
      <div class="flow-step">🧠 <b>AI Processing</b></div><span class="flow-arrow">➔</span>
      <div class="flow-step">🗄️ <b>Database</b></div>
    </div></section>
    <h2 class="section-title">🌏 UN Sustainable Development Goals</h2>
    <div class="sdg-grid">
      <a href="https://sdgs.un.org/goals/goal3" target="_blank" class="sdg-card sdg-card-3"><h3 style="color:#065F46">SDG 3</h3><h4 style="color:#047857">Good Health &amp; Well-being</h4><p style="color:#064E3B">Promoting mental well-being and accessible healthcare for all through AI-powered support.</p><span class="sdg-link" style="color:#047857">👁️ Learn more about SDG 3 →</span></a>
      <a href="https://sdgs.un.org/goals/goal9" target="_blank" class="sdg-card sdg-card-9"><h3 style="color:#9A3412">SDG 9</h3><h4 style="color:#C2410C">Industry, Innovation &amp; Infrastructure</h4><p style="color:#7C2D12">Leveraging cutting-edge AI technology for social welfare and mental health innovation.</p><span class="sdg-link" style="color:#C2410C">👁️ Learn more about SDG 9 →</span></a>
      <a href="https://sdgs.un.org/goals/goal10" target="_blank" class="sdg-card sdg-card-10"><h3 style="color:#9D174D">SDG 10</h3><h4 style="color:#BE185D">Reduced Inequalities</h4><p style="color:#831843">Making mental healthcare accessible to underserved communities worldwide.</p><span class="sdg-link" style="color:#BE185D">👁️ Learn more about SDG 10 →</span></a>
    </div>
    <div class="supervisor-card"><div class="supervisor-icon">👨‍🏫</div><div><div class="supervisor-name">Mr. Faisal Hussain</div><div class="supervisor-dept">Project Supervisor | Department of Computer Science</div><div class="supervisor-dept">National University of Modern Languages (NUML), Multan Campus</div></div></div>
    <h2 class="section-title">📚 References &amp; Resources</h2>
    <div class="references-card"><ul>
      <li>📖 <a href="https://www.who.int/health-topics/mental-health" target="_blank">World Health Organization (WHO) - Mental Health Guidelines 2024</a></li>
      <li>📖 <a href="https://www.apa.org/topics/mental-health" target="_blank">American Psychological Association (APA) - Digital Health Standards</a></li>
      <li>📖 <a href="https://www.mayoclinic.org/healthy-lifestyle" target="_blank">Mayo Clinic - Verified Mental Health Resources</a></li>
      <li>📖 <a href="https://www.nimh.nih.gov/" target="_blank">National Institute of Mental Health (NIMH) - Research Publications</a></li>
      <li>📖 <a href="https://www.mentalhealth.gov/" target="_blank">MentalHealth.gov - Evidence-Based Practices</a></li>
      <li>📖 <a href="https://arxiv.org/abs/2304.12210" target="_blank">Recent Advances in Mental Health AI - arXiv Research Paper</a></li>
    </ul></div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">👥 Development Team</h2><div class="team-grid">'
                '<article class="team-card"><div class="team-avatar">👩‍💻</div><div class="team-name">Safia Rasheed</div><div class="team-id">BSCS-MC-215</div><span class="team-role">Developer</span></article>'
                '<article class="team-card"><div class="team-avatar">👩‍💻</div><div class="team-name">Maria Akram</div><div class="team-id">BSCS-MC-207</div><span class="team-role">Developer</span></article>'
                '<article class="team-card"><div class="team-avatar">👩‍💻</div><div class="team-name">Shamsa Akram</div><div class="team-id">BSCS-MC-208</div><span class="team-role">Developer</span></article></div>',
                unsafe_allow_html=True)

    st.markdown("""
    <section class="stats-footer">
      <h2 style="color:#1E1B4B;font-weight:700;margin:0 0 25px;font-size:1.8rem;text-align:center">📊 Impact Statistics</h2>
      <div class="stats-inner">
        <div class="stat-item"><div class="stat-number">24/7</div><div class="stat-label">Availability</div></div>
        <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Anonymous</div></div>
        <div class="stat-item"><div class="stat-number">50+</div><div class="stat-label">Clinical Sources</div></div>
        <div class="stat-item"><div class="stat-number">Real-time</div><div class="stat-label">Crisis Detection</div></div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    render_global_footer()


if __name__ == "__main__":
    show_about_page()
