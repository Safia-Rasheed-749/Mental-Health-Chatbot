# landing.py — public marketing page (design tokens via app.py)
import streamlit as st
import streamlit.components.v1 as components



def show_landing_page():
    # render_navbar()
    # ================= PROFESSIONAL CSS WITH ANIMATIONS & GRADIENTS =================
    st.markdown("""
    <style>
        /* 🔥 REMOVE STREAMLIT TOP SPACE */
        header {
            visibility: hidden;
            height: 0px;
        }

        [data-testid="stHeader"] {
            display: none;
        }

        /* Do NOT pad .main — that pushed the whole page (navbar) down. Space = below navbar only. */
        .main {
            padding-top: 0 !important;
        }
        [data-testid="stHorizontalBlock"]:has(h1.hero-title) {
            margin-top: 2.25rem !important;
        }
        /* Hero row CTAs: keep label on one line (desktop) */
        [data-testid="stHorizontalBlock"]:has(h1.hero-title) .stButton > button {
            white-space: nowrap !important;
        }
        @media (max-width: 520px) {
            [data-testid="stHorizontalBlock"]:has(h1.hero-title) .stButton > button {
                white-space: normal !important;
            }
        }
        
        /* Remove footer */
        footer, .stApp footer, .css-1lsmgbg, .egzxvld0, .viewerFooter, [data-testid="stFooter"] {
            display: none !important;
        }
        
        /* min-height only — fixed 100vh caused extra empty scroll below footer */
        .stApp {
            overflow-y: auto !important;
            min-height: 100vh !important;
            background: radial-gradient(circle at top left, rgba(124,58,237,0.06), transparent 32%), radial-gradient(circle at bottom right, rgba(99,102,241,0.05), transparent 32%), #f6f7fb !important;
        }
        .main .block-container {
            padding: 0.5rem 2rem 0 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        html, body {
            overflow-y: auto !important;
            min-height: 100% !important;
            scroll-behavior: smooth;
        }
        
        .element-container:has(iframe) {
            margin-bottom: 0 !important;
            overflow: visible !important;
        }
        
        iframe {
            display: block;
            width: 100%;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #E8EEF2;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* ================= HERO SECTION STYLING ================= */
        .hero-container {
            margin-top: 24px;
            padding-right: 20px;
        }
        
        .hero-title {
            font-size: clamp(2.75rem, 5vw, 4.1rem);
            font-weight: 800;
            line-height: 1.06;
            letter-spacing: -0.045em;
            color: #0f172a;
            max-width: 520px;
            margin-bottom: 22px;
            margin-top: 12px !important;
            animation: fadeInUp 0.35s ease-out;
        }
        .hero-title span.accent-word {
            color: #5b21b6;
            -webkit-text-fill-color: #5b21b6;
            background: none;
        }
        
        .hero-description {
            font-size: 19px !important;
            line-height: 1.75;
            color: #334155;
            max-width: 440px;
            margin-bottom: 16px;
            font-weight: 500;
            animation: fadeInUp 0.35s ease-out 0.05s both;
        }

        .hero-trust {
            color: #334155 !important;
            font-size: 17px !important;
            margin-top: 18px;
            letter-spacing: 0.02em;
            font-weight: 500;
        }

        .highlight-text {
            background: linear-gradient(90deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
            padding: 10px 14px;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            display: inline-block;
            animation: fadeInUp 0.4s ease-out 0.2s both;
        }
        
        .hero-button-wrapper {
            margin-top: 25px;
        }
        
        /* Animations — short to reduce overlap with Streamlit rerenders */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* ================= REDUCED FONT SIZES ================= */
        .hero-text {
            color: #334155;
            font-size: 1.0rem;
            line-height: 1.9;
            margin-bottom: 20px;
            font-weight: 500;
            letter-spacing: 0.02em;
            max-width: 720px;
            opacity: 1;
        }
        
       
        
        .section-title {
            text-align: center;
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 700;
            color: #0f172a;
            margin: 56px 0 12px 0;
            position: relative;
        }
        
        .section-description {
            text-align: center;
            color: #475569;
            font-size: 17px;
            line-height: 1.65;
            max-width: 800px;
            margin: 0 auto 28px auto;
            padding: 0 20px;
            font-weight: 500;
        }
        .section-description strong {
            color: #0f172a;
            font-weight: 700;
        }
        
        .exercise-description {
            text-align: center;
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto 35px auto;
            padding: 0 20px;
        }
        
        .exercise-card {
            border-radius: 28px;
            padding: 34px;
            width: 100%;
            transition: all 0.35s ease;
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 30px;
            margin-bottom: 45px;
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
            flex-wrap: wrap;
            animation: fadeInUp 0.4s ease-out;
            background: rgba(255, 255, 255, 0.72);
            backdrop-filter: blur(20px);
        }
        
        .exercise-card-1 { background: linear-gradient(135deg, rgba(209,250,229,0.6), rgba(167,243,208,0.4)); border: 1px solid rgba(52,211,153,0.2); }
        .exercise-card-2 { background: linear-gradient(135deg, rgba(219,234,254,0.6), rgba(191,219,254,0.4)); border: 1px solid rgba(96,165,250,0.2); }
        .exercise-card-3 { background: linear-gradient(135deg, rgba(254,243,199,0.6), rgba(253,230,138,0.4)); border: 1px solid rgba(251,191,36,0.2); }
        
        .exercise-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
        }
        
        .exercise-icon-large {
            font-size: 3.8rem;
            min-width: 85px;
            text-align: center;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes gentleBounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .exercise-content { flex: 1; }
        
        .exercise-title {
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .exercise-quote {
            font-style: italic;
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 15px;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            border-left: 3px solid #3b82f6;
            line-height: 1.5;
        }
        
        .exercise-description-text {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 15px;
            padding: 6px 0;
            line-height: 1.5;
        }
        
        .exercise-description-text strong {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .exercise-quote-author {
            font-size: 0.75rem;
            color: #94a3b8;
            text-align: right;
            margin-top: 6px;
        }
        
        .exercise-steps {
            list-style: none;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .exercise-steps li {
            background: rgba(255, 255, 255, 0.8);
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid rgba(203, 213, 225, 0.5);
            transition: all 0.3s ease;
            color: #334155;
        }
        
        .exercise-steps li:hover {
            transform: translateX(6px);
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.05);
        }
        
        .step-number {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 600;
            flex-shrink: 0;
        }
        
        .exercise-video {
            min-width: 280px;
            max-width: 320px;
        }
        
        .exercise-video video {
            width: 100%;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .exercise-video video:hover {
            transform: scale(1.02);
        }
        
        .feature-card-custom {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 24px;
            padding: 28px 22px;
            transition: 0.35s ease;
            text-align: center;
            height: 100%;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
            margin-bottom: 30px;
            animation: fadeInUp 0.4s ease-out;
        }
        
        .feature-card-custom:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
            border-color: rgba(139, 92, 246, 0.2);
            background: rgba(255, 255, 255, 0.85);
        }
        
        .feature-card-custom div:first-child {
            font-size: 42px;
            margin-bottom: 10px;
            display: inline-block;
        }
        
        .feature-card-custom div:nth-child(2) {
            font-weight: 700;
            margin: 10px 0 6px;
            font-size: 1.1rem;
            color: #0f172a;
            -webkit-text-fill-color: #0f172a;
            background: none;
        }
        
        .feature-card-custom div:last-child {
            font-size: 16.5px;
            color: #475569;
            line-height: 1.45;
            font-weight: 500;
        }
        
        .tech-card-custom {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 20px 12px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(203, 213, 225, 0.3);
            height: 100%;
            margin-bottom: 30px;
            animation: fadeInUp 0.4s ease-out;
        }
        
        .tech-card-custom:hover {
            transform: translateY(-6px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.95);
            border-color: #3b82f6;
        }
        
        .tech-card-custom div:first-child {
            font-size: 2.2rem;
            animation: float 3s ease-in-out infinite;
            display: inline-block;
        }
        
        .tech-card-custom div:nth-child(2) {
            font-weight: 700;
            margin: 10px 0 5px;
            font-size: 0.9rem;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tech-card-custom div:last-child {
            font-size: 0.75rem;
            color: #64748b;
        }
        
        .impact-card-custom {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 28px 12px;
            text-align: center;
            transition: all 0.35s ease;
            border: 1px solid rgba(148, 163, 184, 0.12);
            height: 100%;
            animation: fadeInUp 0.4s ease-out;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
        }
        
        .impact-card-custom:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
            border-color: rgba(139, 92, 246, 0.2);
        }
        
        .stat-number-custom {
            font-size: 2.3rem;
            font-weight: 700;
            color: #8b5cf6;
            -webkit-text-fill-color: #8b5cf6;
            background: none;
            margin-bottom: 6px;
        }
        
        .stat-label-custom {
            color: #64748b;
            font-weight: 500;
            font-size: 0.8rem;
        }
        
        
        
        @media (max-width: 768px) {
            .exercise-card {
                flex-direction: column;
                text-align: center;
                padding: 20px;
            }
            .exercise-video {
                width: 100%;
                min-width: auto;
            }
            .section-title {
                font-size: 1.6rem;
            }
            .hero-text {
                font-size: 0.9rem;
            }
            .section-description {
                font-size: 0.85rem;
            }
        }
        /* Primary CTAs use global blue (layout_utils); do not override all .stButton here */

        section.main p,
        section.main li,
        section.main .stMarkdown p {
            color: #1e293b;
            font-weight: 500;
        }
        
        strong {
            color: #5b21b6;
        }
        
        /* Static footer — same pattern as About page (solid bar, grid, calm typography) */
        .footer-container {
            background: #1e293b;
            color: #e2e8f0;
            padding: 48px 40px 28px 40px;
            margin-top: 60px;
            margin-bottom: 0 !important;
            margin-left: -2rem;
            margin-right: -2rem;
            width: calc(100% + 4rem);
            border-radius: 0;
        }
        
        @media (max-width: 768px) {
            .footer-container {
                margin-left: -1rem;
                margin-right: -1rem;
                width: calc(100% + 2rem);
                padding: 60px 20px 30px 20px;
            }
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 32px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer-col {
            min-width: 0;
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

        /* ================= WHO WE SERVE SECTION ================= */

.who-section {
    margin: 48px 0 32px 0;
}

/* Heading */
.who-section h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 20px;
    line-height: 1.3;
}

/* Left side paragraphs */
.who-section p {
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.7;
    margin-bottom: 18px;
    font-weight: 500;
}

/* Highlight titles (Students, Professionals...) */
.who-section strong {
    font-size: 1.05rem;
    color: #1e293b;
    font-weight: 600;
}

/* ================= WHO WE SERVE - RIGHT SIDE BOX ================= */
.who-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
    backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 12px 28px;
    border: 1px solid rgba(139, 92, 246, 0.15);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    margin-top: 10px;
}

.who-box:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.1);
    border-color: rgba(139, 92, 246, 0.25);
}

.who-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(203, 213, 225, 0.3);
}

.who-item:last-child {
    border-bottom: none;
}

.who-icon {
    font-size: 1.8rem;
    min-width: 45px;
    text-align: center;
}

.who-text {
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.5;
    margin: 0;
}



@media (max-width: 768px) {
    .who-box {
        padding: 24px 20px;
        margin-top: 20px;
    }
    .who-item {
        padding: 12px 0;
    }
    .who-icon {
        font-size: 1.5rem;
        min-width: 38px;
    }
}

    .who-section h2 {
        font-size: 1.6rem;
    }
     .how-it-works-spacing {
    margin-bottom: 60px;
}
    .who-we-serve-spacing {
    margin-top: 20px;
}
    #Overlay Caousel
    .slider-section {
        margin: 60px 0 40px 0;
        text-align: center;
    }
    .slider-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.1);
        padding: 6px 18px;
        border-radius: 40px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #8b5cf6;
        margin-bottom: 20px;
    }
    .slider-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .slider-sub {
        color: #64748b;
        font-size: 0.95rem;
        max-width: 600px;
        margin: 0 auto 40px auto;
    }
    .carousel-heading {
            text-align: center;
            margin: 20px 0;
        }
        
        .carousel-heading h2 {
            font-size: 2rem;
            font-weight: 700;
            color: #0f172a;
            -webkit-text-fill-color: #0f172a;
            background: none;
            margin-bottom: 12px;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .carousel-heading p {
            color: #64748b;
            font-size: 17px;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
    
    """, unsafe_allow_html=True)
    
    # ===== CSS (SAFE - NO NAVBAR BREAK) =====
    st.markdown("""
    <style>
        header, footer, .stDeployButton {
            display: none !important;
        }

        /* Hero spacing comes from .main padding above; avoid double tightening here */
        .main .block-container {
            padding-top: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ================= HERO SECTION =================
    col_t, col_v = st.columns([1, 1.2], gap="large")
    with col_t:
        st.markdown("""
        <h1 class="hero-title">
            A healing space for your <span class="accent-word">mind</span>
        </h1>
        <p class="hero-description">
            Talk, reflect, and find support through emotionally intelligent AI.
        </p>
        <p class="hero-trust"> You're not alone. We listen to you without judgement</p>
        <div class="hero-button-wrapper"></div>
        """, unsafe_allow_html=True)
        # Compact CTA — not full column width
        _hb1, _hb2, _hb3 = st.columns([0.85, 1.45, 1.7])
        with _hb2:
            if st.button("Learn more", key="hero_learn_more", use_container_width=True, type="primary"):
                st.session_state.page = "about"
                st.rerun()

    # ================= CHAT DEMO WITH TYPING ANIMATION =================
    with col_v:
        components.html("""
        <div style="background: rgba(255,255,255,0.68); backdrop-filter: blur(22px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 10px 40px rgba(15,23,42,0.06), 0 2px 12px rgba(15,23,42,0.04); border-radius: 34px; height: 320px; overflow: hidden; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; margin: 8px 10px 10px 10px;">
            <div id="chat-box" style="flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px;"></div>
        </div>
        <style>
            @keyframes bounce {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-8px); }
            }
            .typing-indicator {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 10px 14px;
                border-radius: 20px;
                border-bottom-right-radius: 4px;
            }
            .typing-dot {
                width: 8px;
                height: 8px;
                background: white;
                border-radius: 50%;
                animation: bounce 1.4s ease-in-out infinite;
            }
            .typing-dot:nth-child(1) { animation-delay: 0s; }
            .typing-dot:nth-child(2) { animation-delay: 0.2s; }
            .typing-dot:nth-child(3) { animation-delay: 0.4s; }
            .message-bubble {
                max-width: 85%;
                word-wrap: break-word;
                line-height: 1.4;
            }
            .user-bubble {
                background: #f1f5f9;
                color: #1e293b;
                padding: 10px 14px;
                border-radius: 18px;
                border-bottom-left-radius: 4px;
                display: inline-block;
            }
            .bot-bubble {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 10px 14px;
                border-radius: 18px;
                border-bottom-right-radius: 4px;
                display: inline-block;
                min-width: 60px;
            }
            .message-row {
                display: flex;
                width: 100%;
                margin-bottom: 8px;
            }
            .user-row {
                justify-content: flex-end;
            }
            .bot-row {
                justify-content: flex-start;
            }
            /* NO ANIMATION ON MESSAGES - INSTANT APPEAR */
        </style>
        <script>
        (function() {
            var box = document.getElementById('chat-box');
            if (!box) return;
            
            var conversations = [
                [
                    {u: "I'm really stressed about my project deadlines.", a: "That sounds overwhelming. Let's break it into smaller tasks. Write down what needs to be done first."},
                    {u: "I can't focus at all.", a: "Try a short 2-minute breathing pause. It helps reset your focus. Breathe in for 4, hold for 4, out for 6."},
                    {u: "What if I miss the deadline?", a: "Worst case, communicate early with your manager. Most deadlines can be negotiated. You're not alone in this."}
                ],
                [
                    {u: "I feel anxious about my presentation tomorrow.", a: "Practice out loud 3 times tonight. It builds confidence and reduces anxiety."},
                    {u: "What if I forget my lines?", a: "Keep bullet points on index cards as backup. You'll do great! Take deep breaths before starting."},
                    {u: "Thanks, that helps.", a: "You're welcome! Get good rest tonight. A fresh mind performs better."}
                ],
                [
                    {u: "My team isn't cooperating well.", a: "Have you tried a quick 5-min standup meeting to align everyone?"},
                    {u: "They ignore my suggestions.", a: "Try asking 'What if we tried...' instead of giving direct orders. People respond better to questions."},
                    {u: "That might work.", a: "Lead with curiosity. It opens conversations and builds trust. You've got this!"}
                ]
            ];
            
            var convIndex = 0;
            var isActive = true;
            
            function createUserMessage(text) {
                var row = document.createElement('div');
                row.className = 'message-row user-row';
                
                var bubble = document.createElement('div');
                bubble.className = 'message-bubble user-bubble';
                bubble.innerText = "👤 " + text;
                
                row.appendChild(bubble);
                return row;
            }
            
            function createBotMessageContainer() {
                var row = document.createElement('div');
                row.className = 'message-row bot-row';
                
                var bubble = document.createElement('div');
                bubble.className = 'message-bubble bot-bubble';
                bubble.innerText = "🧠 ";
                
                row.appendChild(bubble);
                return {row: row, bubble: bubble};
            }
            
            function createTypingIndicator() {
                var row = document.createElement('div');
                row.className = 'message-row bot-row';
                
                var indicator = document.createElement('div');
                indicator.className = 'typing-indicator';
                for (var i = 0; i < 3; i++) {
                    var dot = document.createElement('div');
                    dot.className = 'typing-dot';
                    indicator.appendChild(dot);
                }
                
                row.appendChild(indicator);
                return row;
            }
            
            function typeTextWithDelay(bubble, fullText, callback) {
                bubble.innerText = "🧠 ";
                var currentText = "🧠 ";
                var charIndex = 0;
                
                function addNextChar() {
                    if (charIndex < fullText.length) {
                        currentText += fullText.charAt(charIndex);
                        bubble.innerText = currentText;
                        charIndex++;
                        box.scrollTop = box.scrollHeight;
                        setTimeout(addNextChar, 32);
                    } else {
                        if (callback) callback();
                    }
                }
                
                addNextChar();
            }
            
            function removeTypingIndicator(indicator, callback) {
                if (indicator && indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
                if (callback) callback();
            }
            
            function clearChat() {
                return new Promise(function(resolve) {
                    while(box.firstChild) box.removeChild(box.firstChild);
                    resolve();
                });
            }
            
            async function playConversation() {
                if (!isActive) return;
                var conv = conversations[convIndex];
                
                for (var i = 0; i < conv.length; i++) {
                    // Show user message (instantly)
                    var userMsg = createUserMessage(conv[i].u);
                    box.appendChild(userMsg);
                    box.scrollTop = box.scrollHeight;
                    await new Promise(function(resolve) { setTimeout(resolve, 1500); });
                    
                    // Show typing indicator
                    var typingIndicator = createTypingIndicator();
                    box.appendChild(typingIndicator);
                    box.scrollTop = box.scrollHeight;
                    
                    // Wait 2 seconds
                    await new Promise(function(resolve) { setTimeout(resolve, 2000); });
                    
                    // Remove typing indicator instantly
                    removeTypingIndicator(typingIndicator);
                    
                    // Create bot message container (INSTANTLY VISIBLE - no animation)
                    var botContainer = createBotMessageContainer();
                    box.appendChild(botContainer.row);
                    box.scrollTop = box.scrollHeight;
                    
                    // Start typing animation character by character
                    await new Promise(function(resolve) {
                        typeTextWithDelay(botContainer.bubble, conv[i].a, resolve);
                    });
                    
                    if (i < conv.length - 1) {
                        await new Promise(function(resolve) { setTimeout(resolve, 1000); });
                    }
                }
                
                await new Promise(function(resolve) { setTimeout(resolve, 2000); });
                await clearChat();
                convIndex = (convIndex + 1) % conversations.length;
                setTimeout(playConversation, 500);
            }
            
            setTimeout(playConversation, 500);
        })();
        </script>
        """, height=420)
        st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
    
        # Centered button using columns
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1.5, 1])
        with btn_col2:
            if st.button(" Start Chatting", use_container_width=True, key="chat_try_btn", type="primary"):
                st.session_state.page = "demo"
                st.rerun()
        
       # ================= HOW IT WORKS =================
    st.markdown('<div class="how-it-works-spacing">', unsafe_allow_html=True)

    st.markdown('<h2 class="section-title"> How It Works</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 8px 0 24px 0;">
        <p style="color: #64748b; font-size: 17px; margin: 0 auto;">Your journey to better mental health begins here</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🗣️</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a; margin-bottom: 8px;">Share freely</div>
            <div style="font-size: 16px; color: #64748b; line-height: 1.5;">Talk about what's on your mind. No judgment, just listening.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🧠</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a; margin-bottom: 8px;">AI understands</div>
            <div style="font-size: 16px; color: #64748b; line-height: 1.5;">Advanced emotion detection that truly gets how you feel.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">💡</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a; margin-bottom: 8px;">Get support</div>
            <div style="font-size: 16px; color: #64748b; line-height: 1.5;">Receive personalized coping strategies and guidance.</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="mc-section-spacer"></div>', unsafe_allow_html=True)

    # ================= INTERACTIVE WELLNESS SPOTLIGHT (after How it works — engagement before audience) =================
    st.markdown("""
    <div class="spotlight-heading">
        <h2>Explore what you need right now</h2>
        <p>Choose a focus area — see an insight and a small step you can try in the moment.</p>
    </div>
    """, unsafe_allow_html=True)

    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin:0; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: transparent; }
  .ws-wrap { max-width: 920px; margin: 0 auto; padding: 4px 8px 12px; }
  .ws-pills { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 18px; }
  .ws-pill {
    border: 1px solid rgba(15,23,42,0.12);
    background: rgba(255,255,255,0.95);
    color: #0f172a;
    padding: 10px 20px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    font-family: inherit;
  }
  .ws-pill:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(15,23,42,0.08); }
  .ws-pill.active {
    color: #fff;
    border-color: transparent;
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    box-shadow: 0 10px 28px rgba(124,58,237,0.35);
  }
  .ws-panel {
    border-radius: 24px;
    padding: 26px 24px 24px;
    min-height: 200px;
    border: 1px solid rgba(15,23,42,0.08);
    transition: background 0.35s ease, border-color 0.35s ease;
  }
  .ws-quote { font-size: 1.12rem; line-height: 1.7; color: #0f172a; font-style: italic; margin: 0 0 14px; }
  .ws-tip { font-size: 15px; color: #475569; line-height: 1.65; margin: 0; }
  .ws-tip strong { color: #7c3aed; }
  .ws-emoji { font-size: 2.25rem; margin-bottom: 10px; display: block; }
  .ws-hint { font-size: 12px; color: #94a3b8; margin-top: 16px; text-align: center; }
</style>
</head>
<body>
<div class="ws-wrap">
  <div class="ws-pills" id="pills"></div>
  <div class="ws-panel" id="panel">
    <span class="ws-emoji" id="emoji">🌿</span>
    <p class="ws-quote" id="quote"></p>
    <p class="ws-tip" id="tip"></p>
  </div>
  <p class="ws-hint">Tap a topic to switch insights instantly.</p>
</div>
<script>
var topics = [
  { label: 'Calm', emoji: '🌿', grad: 'linear-gradient(135deg, rgba(124,58,237,0.11), rgba(99,102,241,0.07))',
    quote: '"Small pauses between tasks make space for clarity and peace."',
    tip: '<strong>Try now:</strong> Inhale for 4 counts, hold for 2, exhale for 6. Repeat three times.' },
  { label: 'Focus', emoji: '🎯', grad: 'linear-gradient(135deg, rgba(59,130,246,0.12), rgba(14,165,233,0.07))',
    quote: '"One clear step forward beats ten distracted attempts."',
    tip: '<strong>Try now:</strong> Set a 12-minute timer and work on a single micro-task only.' },
  { label: 'Rest', emoji: '🌙', grad: 'linear-gradient(135deg, rgba(99,102,241,0.11), rgba(30,64,175,0.07))',
    quote: '"Rest is not a reward — it is part of sustainable strength."',
    tip: '<strong>Try now:</strong> Dim screens 45 minutes before bed; keep the room slightly cool.' },
  { label: 'Connect', emoji: '💬', grad: 'linear-gradient(135deg, rgba(16,185,129,0.12), rgba(124,58,237,0.06))',
    quote: '"Reaching out is a sign of courage, not weakness."',
    tip: '<strong>Try now:</strong> Send one short message to someone you trust today.' }
];
var idx = 0;
function render() {
  var t = topics[idx];
  document.getElementById('emoji').textContent = t.emoji;
  document.getElementById('quote').textContent = t.quote;
  document.getElementById('tip').innerHTML = t.tip;
  document.getElementById('panel').style.background = t.grad;
  var pills = document.querySelectorAll('.ws-pill');
  for (var i = 0; i < pills.length; i++) {
    pills[i].classList.toggle('active', i === idx);
  }
}
function buildPills() {
  var el = document.getElementById('pills');
  topics.forEach(function(topic, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'ws-pill' + (i === 0 ? ' active' : '');
    b.textContent = topic.label;
    b.addEventListener('click', function() { idx = i; render(); });
    el.appendChild(b);
  });
}
buildPills();
render();
</script>
</body>
</html>
        """,
        height=400,
        scrolling=False,
    )
    st.markdown('<div class="mc-section-spacer"></div>', unsafe_allow_html=True)

    # ================= WHO WE SERVE =================
    st.markdown('<div class="who-we-serve-spacing">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <h2>Who We Serve?</h2>
        
        <p><strong>Students</strong><br>
        Feeling overwhelmed with studies, exams, or pressure.</p>

        <p><strong>Professionals</strong><br>
        Managing stress, burnout, or work-life balance.</p>
        
        <p><strong>💔 Those going through hard times</strong><br>
        Breakups, loss, loneliness — you don't have to go through it alone.</p>

        <p><strong>Anyone feeling anxious</strong><br>
        Looking for a safe space to talk and reflect.</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="who-box">
            <div class="who-item">
                <div class="who-icon">🌙</div>
                <div class="who-text"><strong>Can't sleep?</strong> — Overthinking keeping you awake at night</div>
            </div>
            <div class="who-item">
                <div class="who-icon">💼</div>
                <div class="who-text"><strong>Burned out?</strong> — Work stress affecting your mental health</div>
            </div>
            <div class="who-item">
                <div class="who-icon">🎓</div>
                <div class="who-text"><strong>Exam pressure?</strong> — Academic anxiety holding you back</div>
            </div>
            <div class="who-item">
                <div class="who-icon">💔</div>
                <div class="who-text"><strong>Feeling lonely?</strong> — Need someone who truly listens</div>
            </div>
            
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="mc-section-spacer"></div>', unsafe_allow_html=True)

    # ================= TRUST & SAFETY =================
    st.markdown('<h2 class="section-title"> Trust & Safety</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-description">
    Your well-being and privacy are our top priorities.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card-custom">
            <div>🔐</div>
            <div>Private & Anonymous</div>
            <div>Your conversations are not stored permanently and remain confidential.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card-custom">
            <div>⚠️</div>
            <div>Not a Replacement for Therapy</div>
            <div>This AI provides support but does not replace professional medical advice.</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div class="mc-section-spacer"></div>', unsafe_allow_html=True)

    # ================= CORE CAPABILITIES =================
    st.markdown('<h2 class="section-title">Core Capabilities</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-description">
        <strong>⚡ Intelligent features designed for your emotional well-being</strong><br><br>
        Our AI-powered assistant combines cutting-edge technology with compassionate care for personalized support.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card-custom"><div>💬</div><div>Sentiment Analysis</div><div>Real-time emotion detection</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card-custom"><div>📊</div><div>Mood Tracking</div><div>Visual progress analytics</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card-custom"><div>🛡️</div><div>Crisis Guard</div><div>High-risk keyword detection</div></div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="feature-card-custom"><div>🎤</div><div>Voice Support</div><div>Speech-to-text interaction</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="feature-card-custom"><div>📚</div><div>RAG Knowledge</div><div>WHO verified guidelines</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="feature-card-custom"><div>🧘</div><div>Coping Tools</div><div>Meditation & CBT techniques</div></div>', unsafe_allow_html=True)
       
    # ================= IMPACT SECTION =================
    st.markdown('<h2 class="section-title"> Impact</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-description">
        <strong>📈 Making mental health support accessible to everyone</strong><br><br>
        24/7 anonymous support reducing stigma and reaching underserved communities.
    </div>
    """, unsafe_allow_html=True)

    imp_col1, imp_col2, imp_col3, imp_col4 = st.columns(4)
    with imp_col1:
        st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">24/7</div><div class="stat-label-custom">Availability</div></div>', unsafe_allow_html=True)
    with imp_col2:
        st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">100%</div><div class="stat-label-custom">Anonymous</div></div>', unsafe_allow_html=True)
    with imp_col3:
        st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">50+</div><div class="stat-label-custom">Sources</div></div>', unsafe_allow_html=True)
    with imp_col4:
        st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">Real-time</div><div class="stat-label-custom">Detection</div></div>', unsafe_allow_html=True)

    # ================= FULL FOOTER =================
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
            </div>
        </div>
        <div class="footer-bottom">
            © 2026 MindCareAI — Your well-being matters
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()