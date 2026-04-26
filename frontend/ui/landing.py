# landing.py
import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from components.navbar import render_navbar
from layout_utils import apply_clean_layout   # ← IMPORT ADDED BACK

def show_landing_page():
    # Apply clean layout – removes header/footer, sets top padding
    apply_clean_layout(hide_header_completely=True)
    #st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True) 

    # ================= PROFESSIONAL CSS (no conflicting padding) =================
    st.markdown("""
    <style>
        /* Remove footer */
        footer, .stApp footer, .css-1lsmgbg, .egzxvld0, .viewerFooter, [data-testid="stFooter"] {
            display: none !important;
        }
        
        /* Enable scrolling */
        .stApp {
            overflow-y: auto !important;
            height: 100vh !important;
        }

        /* Only max-width and margins - padding handled by layout_utils */
        .main .block-container {
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
            background: #4A6FA5;
            border-radius: 10px;
        }
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* ================= PROFESSIONAL COLOR SCHEME ================= */
        /* Hero section */
        .hero-text {
            color: #2C3E50;
            font-size: 1.2rem;
            line-height: 1.7;
            margin-bottom: 30px;
        }
        
        /* Carousel heading */
        .carousel-heading {
            text-align: center;
            margin: 20px 0;
        }
        
        .carousel-heading h2 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1E3A5F 0%, #4A6FA5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }
        
        .carousel-heading p {
            color: #4A6FA5;
            font-size: 1.15rem;
            line-height: 1.7;
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* Section titles */
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1E3A5F 0%, #4A6FA5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 40px 0 20px 0;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            display: block;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #4A6FA5, #7899C7);
            margin: 15px auto 0;
            border-radius: 2px;
        }
        
        /* Section description */
        .section-description {
            text-align: center;
            color: #5A6E7A;
            font-size: 1.1rem;
            line-height: 1.7;
            max-width: 800px;
            margin: 0 auto 40px auto;
            padding: 0 20px;
        }
        
        /* Exercise description */
        .exercise-description {
            text-align: center;
            color: #5A6E7A;
            font-size: 1.05rem;
            line-height: 1.7;
            max-width: 800px;
            margin: 0 auto 40px auto;
            padding: 0 20px;
        }
        
        /* Exercise cards */
        .exercise-card {
            border-radius: 20px;
            padding: 32px;
            width: 100%;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 40px;
            margin-bottom: 30px;
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            flex-wrap: wrap;
        }
        
        .exercise-card-1 { 
            background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%); 
            border-left: 4px solid #5B8C5A;
        }
        .exercise-card-2 { 
            background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%); 
            border-left: 4px solid #4A6FA5;
        }
        .exercise-card-3 { 
            background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%); 
            border-left: 4px solid #C17A5B;
        }
        
        .exercise-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
        }
        
        .exercise-icon-large {
            font-size: 4.5rem;
            min-width: 100px;
            text-align: center;
            animation: gentleBounce 3s ease-in-out infinite;
        }
        
        @keyframes gentleBounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .exercise-content { flex: 1; }
        
        .exercise-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: #1E3A5F;
        }
        
        .exercise-quote {
            font-style: italic;
            font-size: 0.95rem;
            color: #5A6E7A;
            margin-bottom: 20px;
            padding: 14px 18px;
            background: #F8F9FB;
            border-radius: 12px;
            border-left: 3px solid #7899C7;
            line-height: 1.6;
        }
        
        .exercise-description-text {
            font-size: 0.95rem;
            color: #5A6E7A;
            margin-bottom: 18px;
            padding: 8px 0;
            line-height: 1.6;
        }
        
        .exercise-description-text strong {
            color: #1E3A5F;
        }
        
        .exercise-quote-author {
            font-size: 0.85rem;
            color: #7899C7;
            text-align: right;
            margin-top: 6px;
        }
        
        .exercise-steps {
            list-style: none;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .exercise-steps li {
            background: #FFFFFF;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 12px;
            border: 1px solid #E8EEF2;
            transition: all 0.2s ease;
            color: #2C3E50;
        }
        
        .exercise-steps li:hover {
            transform: translateX(4px);
            border-color: #7899C7;
            background: #FAFCFE;
        }
        
        .step-number {
            background: #4A6FA5;
            color: white;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 600;
            flex-shrink: 0;
        }
        
        .exercise-video {
            min-width: 300px;
            max-width: 360px;
        }
        
        .exercise-video video {
            width: 100%;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Feature cards */
        .feature-card-custom {
            background: #FFFFFF;
            padding: 28px 20px;
            border-radius: 16px;
            border: 1px solid #E8EEF2;
            transition: all 0.3s ease;
            text-align: center;
            height: 100%;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        }
        
        .feature-card-custom:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
            border-color: #7899C7;
        }
        
        .feature-card-custom div:first-child {
            font-size: 42px;
            margin-bottom: 12px;
        }
        
        .feature-card-custom div:nth-child(2) {
            font-weight: 700;
            margin: 12px 0 8px;
            font-size: 1.15rem;
            color: #1E3A5F;
        }
        
        .feature-card-custom div:last-child {
            font-size: 0.9rem;
            color: #5A6E7A;
            line-height: 1.5;
        }
        
        /* Tech cards */
        .tech-card-custom {
            background: #F8F9FB;
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #E8EEF2;
            height: 100%;
        }
        
        .tech-card-custom:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
            background: #FFFFFF;
            border-color: #7899C7;
        }
        
        .tech-card-custom div:first-child {
            font-size: 2.5rem;
        }
        
        .tech-card-custom div:nth-child(2) {
            font-weight: 700;
            margin: 12px 0 6px;
            font-size: 1rem;
            color: #1E3A5F;
        }
        
        .tech-card-custom div:last-child {
            font-size: 0.85rem;
            color: #7899C7;
        }
        
        /* Impact cards */
        .impact-card-custom {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FB 100%);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #E8EEF2;
            height: 100%;
        }
        
        .impact-card-custom:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
            border-color: #7899C7;
        }
        
        .stat-number-custom {
            font-size: 2.2rem;
            font-weight: 800;
            color: #4A6FA5;
            margin-bottom: 8px;
        }
        
        .stat-label-custom {
            color: #5A6E7A;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        /* Custom footer */
        .custom-footer {
            text-align: center;
            padding: 40px 0 30px;
            border-top: 1px solid #E8EEF2;
            margin: 50px 0 0 0;
            background: #F8F9FB;
            border-radius: 20px;
            width: 100%;
            clear: both;
        }
        
        .custom-footer p {
            color: #5A6E7A;
            font-size: 0.85rem;
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .carousel-wrapper {
            max-width: 1400px;
            margin: 40px auto;
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
                padding: 24px;
            }
            .exercise-video {
                width: 100%;
                min-width: auto;
            }
            .section-title {
                font-size: 1.8rem;
            }
            .hero-text {
                font-size: 1rem;
            }
            .section-description {
                font-size: 0.95rem;
            }
        }
        
        /* Scroll to top button */
        .scroll-top {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: #4A6FA5;
            color: white;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            text-align: center;
            line-height: 44px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            font-size: 20px;
            transition: all 0.3s ease;
        }
        
        .scroll-top:hover {
            background: #1E3A5F;
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button {
            background: #4A6FA5;
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            width: 100%;
            cursor: pointer;
        }
        
        .stButton > button:hover {
            background: #1E3A5F;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        
        /* General text colors */
        p, li, .stMarkdown {
            color: #2C3E50;
        }
        
        strong {
            color: #1E3A5F;
        }
    </style>
    
    <div class="scroll-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'});">↑</div>
    """, unsafe_allow_html=True)

    # ================= HERO SECTION =================
    col_t, col_v = st.columns([1, 1.2], gap="large")
    with col_t:
        st.markdown(
            '<div style="margin-top: 10px;">'
            '<h1 style="font-size:2.5rem; font-weight:800; background:linear-gradient(135deg, #1E3A5F 0%, #4A6FA5 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; line-height:1.2;">'
            'AI Powered <span style="color:#4A6FA5; -webkit-text-fill-color:#4A6FA5;">Emotional Care</span>'
            '</h1>'
            '<p class="hero-text">'
            'Your compassionate AI companion for mental wellness, available 24/7.<br>'
            'Providing intelligent, stigma-free emotional support whenever you need it.<br>'
            'Experience a safe space where technology meets empathy, helping you navigate life\'s challenges with confidence.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("✨ Try It Yourself", use_container_width=True, key="hero_try"):
            st.session_state.page = "demo"
            st.rerun()

    # ================= CHAT DEMO =================
    with col_v:
        # Wrap the chat demo to prevent layout shift
        st.markdown('<div style="min-height: 460px;">', unsafe_allow_html=True)
        components.html("""
        <div style="background: white; border-radius: 20px; padding: 20px; border: 1px solid #E8EEF2; box-shadow: 0 8px 20px rgba(0,0,0,0.06); height: 380px; overflow: hidden; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; margin: 10px;">
            <div id="chat-box" style="flex: 1; overflow-y: auto; padding-right: 10px; display: flex; flex-direction: column;"></div>
        </div>
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
            
            function createMsg(text, isUser) {
                var msg = document.createElement('div');
                msg.style.display = 'flex';
                msg.style.marginBottom = '12px';
                msg.style.justifyContent = isUser ? 'flex-start' : 'flex-end';
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(10px)';
                msg.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                
                var bubble = document.createElement('div');
                bubble.style.padding = '10px 14px';
                bubble.style.borderRadius = isUser ? '0 15px 15px 15px' : '15px 0 15px 15px';
                bubble.style.fontSize = '14px';
                bubble.style.maxWidth = '80%';
                bubble.style.wordWrap = 'break-word';
                
                if (isUser) { 
                    bubble.style.background = '#F0F3F7'; 
                    bubble.style.color = '#1E3A5F';
                    bubble.innerText = "👤 " + text; 
                } else { 
                    bubble.style.background = '#4A6FA5'; 
                    bubble.style.color = 'white'; 
                    bubble.innerText = "🧠 " + text; 
                }
                
                msg.appendChild(bubble);
                return msg;
            }
            
            function animateMessage(msg) {
                msg.style.opacity = '1';
                msg.style.transform = 'translateY(0)';
            }
            
            function clearChat() {
                return new Promise(function(resolve) {
                    box.style.opacity = '0';
                    setTimeout(function() {
                        while(box.firstChild) box.removeChild(box.firstChild);
                        box.style.opacity = '1';
                        resolve();
                    }, 300);
                });
            }
            
            async function playConversation() {
                if (!isActive) return;
                var conv = conversations[convIndex];
                for (var i = 0; i < conv.length; i++) {
                    var userMsg = createMsg(conv[i].u, true);
                    box.appendChild(userMsg);
                    animateMessage(userMsg);
                    box.scrollTop = box.scrollHeight;
                    await new Promise(function(resolve) { setTimeout(resolve, 1500); });
                    
                    var botMsg = createMsg(conv[i].a, false);
                    box.appendChild(botMsg);
                    animateMessage(botMsg);
                    box.scrollTop = box.scrollHeight;
                    if (i < conv.length - 1) await new Promise(function(resolve) { setTimeout(resolve, 1500); });
                }
                await new Promise(function(resolve) { setTimeout(resolve, 2000); });
                await clearChat();
                convIndex = (convIndex + 1) % conversations.length;
                setTimeout(playConversation, 500);
            }
            
            setTimeout(playConversation, 500);
        })();
        </script>
        """, height=460)
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= CAROUSEL HEADING =================
    st.markdown("""
    <div class="carousel-heading">
        <h2>🤖 AI-Powered Mental Wellness Journey</h2>
        <p>Experience compassionate AI support that understands your emotions, provides evidence-based guidance, 
        and helps you navigate life's challenges with empathy and care.</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= QUOTE CAROUSEL =================
    st.markdown('<div class="carousel-wrapper"><div class="carousel-outer">', unsafe_allow_html=True)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; background: transparent; font-family: 'Inter', sans-serif; }
            .carousel-container { width: 100%; overflow: hidden; position: relative; height: 450px; background: transparent; }
            .carousel-track { display: flex; width: 400%; height: 100%; transition: transform 0.7s ease-in-out; }
            .slide { width: 25%; height: 100%; background-size: cover; background-position: center; display: flex; align-items: center; justify-content: center; flex-shrink: 0; position: relative; }
            .quote-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(8px); border-radius: 32px; padding: 32px 48px; max-width: 680px; box-shadow: 0 20px 40px -12px rgba(0,0,0,0.25); text-align: center; border: 1px solid rgba(255,255,255,0.5); z-index: 2; margin: 0 20px; }
            .quote-text { color: #1E3A5F; font-size: 24px; font-weight: 500; line-height: 1.5; font-style: italic; margin: 0; text-shadow: 1px 1px 2px rgba(255,255,255,0.5); }
            .quote-author { margin-top: 20px; color: #4A6FA5; font-size: 15px; font-weight: 600; }
            @media (max-width: 768px) {
                .quote-card { padding: 20px 24px; margin: 0 15px; }
                .quote-text { font-size: 18px; }
            }
        </style>
    </head>
    <body>
    <div class="carousel-container">
        <div class="carousel-track" id="carouselTrack">
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1559757175-5700dde675bc?q=80&w=2069&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">"Mental health is not a destination, but a journey of self-discovery and healing."</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1932&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">"AI-powered emotional support is transforming mental healthcare, making it accessible 24/7 for everyone."</p>
                    <p class="quote-author">— MindCare AI Research</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1999&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">"Your mental health journey matters. Let AI be your compassionate companion along the way."</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1584515933487-779824d29309?q=80&w=2070&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">"Technology meets empathy. Our AI chatbot understands, listens, and supports your emotional well-being."</p>
                    <p class="quote-author">— MindCare AI Team</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        var track = document.getElementById('carouselTrack');
        var currentIndex = 0;
        var totalSlides = 3;
        var slideWidth = 25;
        function moveToNext() {
            currentIndex++;
            track.style.transform = 'translateX(-' + (currentIndex * slideWidth) + '%)';
            if (currentIndex === totalSlides) {
                setTimeout(function() {
                    track.style.transition = 'none';
                    track.style.transform = 'translateX(0%)';
                    currentIndex = 0;
                    track.offsetHeight;
                    track.style.transition = 'transform 0.7s ease-in-out';
                }, 700);
            }
        }
        setInterval(moveToNext, 5000);
    </script>
    </body>
    </html>
    """, height=470)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ================= MENTAL WELLNESS EXERCISES =================
    st.markdown('<h2 class="section-title">🧘 Mental Wellness Exercises</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="exercise-description">
        <strong>🧠 Evidence-based practices for emotional balance</strong><br><br>
        These scientifically-backed exercises are designed to reduce anxiety, improve focus, 
        and build emotional resilience. Our AI companion guides you through each practice 
        with personalized tips and gentle encouragement.
    </div>
    """, unsafe_allow_html=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    video_path_1 = os.path.join(BASE_DIR, "../../assets/videos/videobreathe.mp4")
    video_path_2 = os.path.join(BASE_DIR, "../../assets/videos/video1.mp4")

    video_available_1 = False
    video_base64_1 = ""
    try:
        if os.path.exists(video_path_1):
            with open(video_path_1, "rb") as video_file:
                video_base64_1 = base64.b64encode(video_file.read()).decode()
            video_available_1 = True
    except Exception:
        pass

    video_available_2 = False
    video_base64_2 = ""
    try:
        if os.path.exists(video_path_2):
            with open(video_path_2, "rb") as video_file:
                video_base64_2 = base64.b64encode(video_file.read()).decode()
            video_available_2 = True
    except Exception:
        pass

    # Exercise 1
    if video_available_1:
        st.markdown(f"""
        <div class="exercise-card exercise-card-1">
            <div class="exercise-icon-large">🌬️</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindful Breathing Exercise</div>
                <div class="exercise-quote">"Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🌿 Why it helps:</strong> Deep breathing activates your parasympathetic nervous system, reducing cortisol levels and calming anxiety. Regular practice improves emotional regulation and stress resilience.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li><li><span class="step-number">2</span> Hold your breath for 4 seconds</li><li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li><li><span class="step-number">4</span> Repeat 5-10 times</li></ul>
            </div>
            <div class="exercise-video"><video autoplay muted loop playsinline><source src="data:video/mp4;base64,{video_base64_1}" type="video/mp4"></video></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exercise-card exercise-card-1">
            <div class="exercise-icon-large">🌬️</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindful Breathing Exercise</div>
                <div class="exercise-quote">"Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🌿 Why it helps:</strong> Deep breathing activates your parasympathetic nervous system, reducing cortisol levels and calming anxiety. Regular practice improves emotional regulation and stress resilience.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li><li><span class="step-number">2</span> Hold your breath for 4 seconds</li><li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li><li><span class="step-number">4</span> Repeat 5-10 times</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exercise 2
    if video_available_2:
        st.markdown(f"""
        <div class="exercise-card exercise-card-2">
            <div class="exercise-icon-large">🧠</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindfulness Meditation</div>
                <div class="exercise-quote">"The present moment is filled with joy and happiness. If you are attentive, you will see it."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🎯 Why it helps:</strong> Mindfulness rewires your brain for greater emotional regulation and reduces stress. Studies show it decreases anxiety by 40% and improves focus and self-awareness.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Sit comfortably and close your eyes</li><li><span class="step-number">2</span> Focus on your breath without judgment</li><li><span class="step-number">3</span> Notice thoughts and let them pass</li><li><span class="step-number">4</span> Practice for 5-10 minutes daily</li></ul>
            </div>
            <div class="exercise-video"><video autoplay muted loop playsinline><source src="data:video/mp4;base64,{video_base64_2}" type="video/mp4"></video></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exercise-card exercise-card-2">
            <div class="exercise-icon-large">🧠</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindfulness Meditation</div>
                <div class="exercise-quote">"The present moment is filled with joy and happiness. If you are attentive, you will see it."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🎯 Why it helps:</strong> Mindfulness rewires your brain for greater emotional regulation and reduces stress. Studies show it decreases anxiety by 40% and improves focus and self-awareness.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Sit comfortably and close your eyes</li><li><span class="step-number">2</span> Focus on your breath without judgment</li><li><span class="step-number">3</span> Notice thoughts and let them pass</li><li><span class="step-number">4</span> Practice for 5-10 minutes daily</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exercise 3
    st.markdown("""
    <div class="exercise-card exercise-card-3">
        <div class="exercise-icon-large">🌍</div>
        <div class="exercise-content">
            <div class="exercise-title">5-4-3-2-1 Grounding Technique</div>
            <div class="exercise-quote">"Grounding is a powerful way to calm anxiety and return to the present moment."<div class="exercise-quote-author">— MindCare AI</div></div>
            <div class="exercise-description-text"><strong>⚡ Why it helps:</strong> This evidence-based technique interrupts anxiety spirals by engaging all five senses. Provides immediate relief during panic attacks or overwhelming emotions. Perfect for high-stress situations.</div>
            <ul class="exercise-steps"><li><span class="step-number">👁️</span> Acknowledge 5 things you see around you</li><li><span class="step-number">🫂</span> Acknowledge 4 things you can physically touch</li><li><span class="step-number">👂</span> Acknowledge 3 distinct sounds you hear</li><li><span class="step-number">👃</span> Acknowledge 2 different smells in your environment</li><li><span class="step-number">👅</span> Acknowledge 1 thing you can taste or focus on your breath</li></ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= FEATURES SECTION =================
    st.markdown('<h2 class="section-title">🎯 Core Capabilities</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        <strong>🤖 Intelligent features designed for your emotional well-being</strong><br><br>
        Our AI-powered chatbot combines cutting-edge technology with compassionate care. From real-time emotion detection 
        to personalized coping strategies, every feature is crafted to support your mental health journey.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="feature-card-custom"><div>💬</div><div>Sentiment Analysis</div><div>Real-time emotion detection</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="feature-card-custom"><div>📊</div><div>Mood Tracking</div><div>Visual progress analytics</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="feature-card-custom"><div>🛡️</div><div>Crisis Guard</div><div>High-risk keyword detection</div></div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4: st.markdown('<div class="feature-card-custom"><div>🎤</div><div>Voice Support</div><div>Speech-to-text interaction</div></div>', unsafe_allow_html=True)
    with col5: st.markdown('<div class="feature-card-custom"><div>📚</div><div>RAG Knowledge</div><div>WHO verified guidelines</div></div>', unsafe_allow_html=True)
    with col6: st.markdown('<div class="feature-card-custom"><div>🧘</div><div>Coping Tools</div><div>Meditation & CBT techniques</div></div>', unsafe_allow_html=True)

    # ================= TECH STACK SECTION =================
    st.markdown('<h2 class="section-title">🔧 Technology Stack</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        <strong>⚙️ Built with cutting-edge technology for reliability and scale</strong><br><br>
        Our platform leverages modern AI architectures and industry-standard frameworks to deliver fast, 
        secure, and intelligent emotional support.
    </div>
    """, unsafe_allow_html=True)

    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    with tech_col1: st.markdown('<div class="tech-card-custom"><div>⚡</div><div>Frontend</div><div>Streamlit</div></div>', unsafe_allow_html=True)
    with tech_col2: st.markdown('<div class="tech-card-custom"><div>🤖</div><div>AI Engine</div><div>LLM + RAG</div></div>', unsafe_allow_html=True)
    with tech_col3: st.markdown('<div class="tech-card-custom"><div>🗄️</div><div>Backend</div><div>FastAPI</div></div>', unsafe_allow_html=True)
    with tech_col4: st.markdown('<div class="tech-card-custom"><div>🎤</div><div>Voice</div><div>Whisper</div></div>', unsafe_allow_html=True)

    # ================= IMPACT SECTION =================
    st.markdown('<h2 class="section-title">📊 Impact</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        <strong>📈 Making mental health support accessible to everyone</strong><br><br>
        Our platform breaks barriers in mental healthcare by providing 24/7 anonymous support, 
        reducing stigma, and reaching underserved communities.
    </div>
    """, unsafe_allow_html=True)

    imp_col1, imp_col2, imp_col3, imp_col4 = st.columns(4)
    with imp_col1: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">24/7</div><div class="stat-label-custom">Availability</div></div>', unsafe_allow_html=True)
    with imp_col2: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">100%</div><div class="stat-label-custom">Anonymous</div></div>', unsafe_allow_html=True)
    with imp_col3: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">50+</div><div class="stat-label-custom">Sources</div></div>', unsafe_allow_html=True)
    with imp_col4: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">Real-time</div><div class="stat-label-custom">Detection</div></div>', unsafe_allow_html=True)

    # ================= CUSTOM FOOTER =================
    st.markdown("""
    <div class="custom-footer">
        <p>© 2026 Mind Care AI | National University of Modern Languages, Islamabad</p>
        <p>Final Year Project | Department of Computer Science</p>
        <p>Supervised by Faisal Hussain</p>
        <p style="margin-top: 16px;">🌟 Your mental well-being is our priority. Reach out anytime.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()