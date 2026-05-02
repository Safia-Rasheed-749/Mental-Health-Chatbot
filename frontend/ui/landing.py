# landing.py - With 3 New Images in Carousel (No Overlay)
import streamlit as st
import streamlit.components.v1 as components
import base64
import os
# from components.navbar import render_navbar  # Import navbar



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

        /* 🔥 REMOVE EXTRA GAP ABOVE CONTENT */
        .main {
            padding-top: 1.8rem !important;
        }
        
        /* Remove footer */
        footer, .stApp footer, .css-1lsmgbg, .egzxvld0, .viewerFooter, [data-testid="stFooter"] {
            display: none !important;
        }
        
        /* Enable scrolling */
        .stApp {
            overflow-y: auto !important;
            height: 100vh !important;
            background: radial-gradient(circle at top left, rgba(139,92,246,0.10), transparent 30%), radial-gradient(circle at bottom right, rgba(99,102,241,0.08), transparent 30%), #f8fafc;
        }
        .main .block-container {
            padding: 1rem 2rem 0rem 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        html, body {
            overflow-y: auto !important;
            height: 100% !important;
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
            margin-top: 70px;
            padding-right: 20px;
        }
        
        .hero-title {
            font-size: 3.4rem;
            font-weight: 800;
            line-height: 1.08;
            letter-spacing: -2px;
            color: #0f172a;
            max-width: 420px;
            margin-bottom: 22px;
            margin-top: 100px !important;
            animation: fadeInUp 0.8s ease-out;
        }
        .hero-title span {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-description {
            font-size: 20px !important;
            line-height: 1.9;
            color: #475569;
            max-width: 420px;
            margin-bottom: 18px;
            font-weight: 400;
            animation: fadeInUp 0.8s ease-out 0.1s both;
        }

        .hero-trust {
            color: #475569 !important;
            font-size: 17px !important;
            margin-top: 18px;
            letter-spacing: 0.3px;
        }

        .highlight-text {
            background: linear-gradient(90deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
            padding: 10px 14px;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            display: inline-block;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }
        
        .hero-button-wrapper {
            margin-top: 25px;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
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
            color: #475569;
            font-size: 1.0rem;
            line-height: 1.9;
            margin-bottom: 20px;
            font-weight: 400;
            letter-spacing: 0.3px;
            max-width: 720px;
            opacity: 0.9;
            text-shadow: 0px 1px 1px rgba(0,0,0,0.04);
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
        
        .section-title {
            text-align: center;
            font-size: 2.1rem;
            font-weight: 700;
            color: #0f172a;
            margin: 80px 0 15px 0;
            position: relative;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .section-description {
            text-align: center;
            color: #3b82f6;
            font-size: 18px;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto 35px auto;
            padding: 0 20px;
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
            animation: fadeInUp 0.8s ease-out;
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
            animation: fadeInUp 0.8s ease-out;
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
            color: #64748b;
            line-height: 1.4;
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
            animation: fadeInUp 0.8s ease-out;
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
            animation: fadeInUp 0.8s ease-out;
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
        
        .carousel-wrapper {
            max-width: 1400px;
            margin: 35px auto;
            padding: 0 20px;
        }
        
        .carousel-outer {
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
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
        .stButton > button {
            background: #8b5cf6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 16px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            width: fit-content !important;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
        }
        div.stButton > button{
                margin: 0 30px !important;
                }
        
        .stButton > button:hover {
            background: #7c3aed;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        }
        
        p, li, .stMarkdown {
            color: #334155;
        }
        
        strong {
            color: #3b82f6;
        }
        
        .footer-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: white;
            padding: 60px 40px 30px 40px;
            margin-top: 60px;
            margin-bottom: 0;
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
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 30px;
        }
        
        .footer-col {
            flex: 1;
            min-width: 220px;
        }
        
        .footer-title {
            font-weight: 700;
            margin-bottom: 15px;
            font-size: 16px;
            background: linear-gradient(135deg, #a5b4fc 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .footer-text {
            font-size: 13px;
            color: #cbd5e1;
            margin-bottom: 8px;
            transition: color 0.3s ease;
            cursor: pointer;
        }
        
        .footer-text:hover {
            color: #a5b4fc;
        }
        
        .footer-bottom {
            text-align: center;
            margin-top: 40px;
            font-size: 12px;
            color: #94a3b8;
        }
        /* ================= WHO WE SERVE SECTION ================= */

.who-section {
    margin: 80px 0 40px 0;
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
    color: #475569;
    line-height: 1.7;
    margin-bottom: 18px;
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

    
    </style>
    
    """, unsafe_allow_html=True)
    
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

    # ================= HERO SECTION =================
    col_t, col_v = st.columns([1, 1.2], gap="large")
    with col_t:
        st.markdown("""
        <h1 class="hero-title">
            A Healing space for your <span>mind</span>
        </h1>
        <p class="hero-description">
            Talk, reflect, and find support through emotionally intelligent AI.
        </p>
        <p class="hero-trust"> You're not alone. We listen to you without judgement</p>
        <div class="hero-button-wrapper"></div>
        """, unsafe_allow_html=True)
        
        # Button changed to "Learn More" and goes to about page
        if st.button(" Learn more", key="hero_learn_more", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= CHAT DEMO WITH TYPING ANIMATION =================
    with col_v:
        components.html("""
        <div style="background: rgba(255,255,255,0.68); backdrop-filter: blur(22px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 10px 40px rgba(15,23,42,0.06), 0 2px 12px rgba(15,23,42,0.04); border-radius: 34px; height: 320px; overflow: hidden; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; margin: 80px 10px 10px 10px;">
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
            if st.button(" Start Chatting", use_container_width=True, key="chat_try_btn"):
                st.session_state.page = "demo"
                st.rerun()
        
       # ================= HOW IT WORKS =================
    st.markdown('<h2 class="section-title"> How It Works</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: -20px 0 20px 0;">
        <p style="color: #3b82f6; font-size: 19px; margin: 40px auto;">Your journey to better mental health begins here</p>
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
    # ================= WHO WE SERVE =================
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
    # ================= CAROUSEL FIRST (UPPER) =================
    st.markdown("""
    <div class="carousel-heading">
        <h2> Your AI-Powered Mental Wellness Journey</h2>
        <p>Experience compassionate AI support that understands your emotions, provides evidence-based guidance, 
        and helps you navigate life's challenges with empathy and care.</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= QUOTE CAROUSEL WITH 3 NEW IMAGES (NO OVERLAY) =================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # NEW IMAGE PATHS - Updated with your 3 new images
    image_path_1 = os.path.join(BASE_DIR, "../../assets/images/WhatsApp Image 2026-04-29 at 7.58.14 PM.jpeg")
    image_path_2 = os.path.join(BASE_DIR, "../../assets/images/WhatsApp Image 2026-04-29 at 7.58.15 PM.jpeg")
    image_path_3 = os.path.join(BASE_DIR, "../../assets/images/WhatsApp Image 2026-04-29 at 8.00.27 PM.jpeg")
    
    def get_image_base64(image_path):
        """Convert image file to base64 string"""
        try:
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode()
                    return f"data:image/jpeg;base64,{image_base64}", True
            else:
                return "", False
        except Exception:
            return "", False
    
    img_base64_1, img_available_1 = get_image_base64(image_path_1)
    img_base64_2, img_available_2 = get_image_base64(image_path_2)
    img_base64_3, img_available_3 = get_image_base64(image_path_3)
    
    # Use first image as fallback if others not available
    fallback_img = img_base64_1 if img_available_1 else ""
    
    st.markdown('<div class="carousel-wrapper"><div class="carousel-outer">', unsafe_allow_html=True)

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: transparent; font-family: 'Inter', sans-serif; }}
            .carousel-container {{ width: 100%; overflow: hidden; position: relative; height: 400px; background: transparent; }}
            .carousel-track {{ display: flex; width: 400%; height: 100%; transition: transform 0.7s ease-in-out; }}
            .slide {{ width: 25%; height: 100%; background-size: cover; background-position: center; background-repeat: no-repeat; display: flex; align-items: center; justify-content: center; flex-shrink: 0; position: relative; }}
            .quote-card {{ background: rgba(255,255,255,0.72); backdrop-filter: blur(18px); border-radius: 28px; padding: 24px 34px; max-width: 560px; box-shadow: 0 8px 30px rgba(15,23,42,0.06); text-align: center; border: 1px solid rgba(255,255,255,0.5); z-index: 2; margin: 0 20px; position: relative; animation: fadeInUp 0.8s ease-out; }}
            .quote-text {{ color: #1e293b; font-size: 1.15rem; line-height: 1.8; font-weight: 500; font-style: italic; margin: 0; }}
            .quote-author {{ margin-top: 30px; color: #667eea; font-size: 14px; font-weight: 600; }}
            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (max-width: 768px) {{
                .carousel-container {{ height: 350px; }}
                .quote-card {{ padding: 20px 24px; margin: 0 15px; }}
                .quote-text {{ font-size: 18px; }}
            }}
        </style>
    </head>
    <body>
    <div class="carousel-container">
        <div class="carousel-track" id="carouselTrack">
            <div class="slide" style="background-image: url('{img_base64_1 if img_available_1 else fallback_img}');">
                <div class="quote-card">
                    <p class="quote-text">"Mental health is not a destination, but a journey of self-discovery and healing."</p>
                    <p class="quote-author">— AI Assistant for Mental Health</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('{img_base64_2 if img_available_2 else fallback_img}');">
                <div class="quote-card">
                    <p class="quote-text">"AI-powered emotional support is transforming mental healthcare, making it accessible 24/7 for everyone."</p>
                    <p class="quote-author">— AI Assistant Research</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('{img_base64_3 if img_available_3 else fallback_img}');">
                <div class="quote-card">
                    <p class="quote-text">"Your mental health journey matters. Let AI be your compassionate companion along the way."</p>
                    <p class="quote-author">— AI Assistant Team</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('{img_base64_1 if img_available_1 else fallback_img}');">
                <div class="quote-card">
                    <p class="quote-text">"Technology meets empathy. Our AI understands, listens, and supports your emotional well-being."</p>
                    <p class="quote-author">— AI Assistant</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        var track = document.getElementById('carouselTrack');
        var currentIndex = 0;
        var totalSlides = 3;
        var slideWidth = 25;
        function moveToNext() {{
            currentIndex++;
            track.style.transform = 'translateX(-' + (currentIndex * slideWidth) + '%)';
            if (currentIndex === totalSlides) {{
                setTimeout(function() {{
                    track.style.transition = 'none';
                    track.style.transform = 'translateX(0%)';
                    currentIndex = 0;
                    track.offsetHeight;
                    track.style.transition = 'transform 0.7s ease-in-out';
                }}, 700);
            }}
        }}
        setInterval(moveToNext, 5000);
    </script>
    </body>
    </html>
    """, height=420)

    st.markdown('</div></div>', unsafe_allow_html=True)

    
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
            © 2026 AI Assistant for Mental Health — Your well-being matters 
        </div>
    </div>
    """, unsafe_allow_html=True)
    

    
    st.markdown('<div style="height: 0px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()