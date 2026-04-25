# landing.py
import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from components.navbar import render_navbar   # import shared navbar

def show_landing_page():
    # ================= STYLE ENGINE (page‑specific CSS only) =================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Section Titles - WITHOUT underline */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E293B;
        margin: 60px 0 20px 0;
        position: relative;
    }
    
    /* ===== EXERCISES SECTION - VERTICAL ===== */
    .exercise-card {
        border-radius: 25px;
        padding: 30px;
        width: 100%;
        transition: all 0.4s ease;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 40px;
        margin-bottom: 30px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }
    .exercise-card-1 { background: #F3E8FF; border-left: 8px solid #A855F7; }
    .exercise-card-2 { background: #DBEAFE; border-left: 8px solid #3B82F6; }
    .exercise-card-3 { background: #CCFBF1; border-left: 8px solid #14B8A6; }
    .exercise-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -12px rgba(0,0,0,0.12);
    }
    .exercise-icon-large {
        font-size: 5rem;
        min-width: 120px;
        text-align: center;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }
    .exercise-content { flex: 1; }
    .exercise-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #1E293B;
    }
    .exercise-quote {
        font-style: italic;
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 20px;
        padding: 12px 16px;
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        border-left: 4px solid #6366F1;
    }
    .exercise-quote-author {
        font-size: 0.8rem;
        color: #64748B;
        text-align: right;
        margin-top: 8px;
    }
    .exercise-steps {
        list-style: none;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .exercise-steps li {
        background: white;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 1px solid #E2E8F0;
    }
    .step-number {
        background: #1E40AF;
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: bold;
        flex-shrink: 0;
    }
    .exercise-image-small { font-size: 1.2rem; margin-left: 5px; }
    
    /* Video styles */
    .exercise-video {
        min-width: 300px;
        max-width: 350px;
    }
    
    .exercise-video video {
        width: 100%;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Feature card */
    .feature-card-custom {
        background: #FFFFFF;
        padding: 25px 20px;
        border-radius: 20px;
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
    }
    .feature-card-custom:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    }
    .tech-card-custom {
        border-radius: 20px;
        padding: 25px 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #F1F5F9;
        background: white;
        height: 100%;
    }
    .tech-card-custom:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        background: #F5F3FF;
    }
    .impact-card-custom {
        background: white;
        border-radius: 20px;
        padding: 25px 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #F1F5F9;
        height: 100%;
    }
    .impact-card-custom:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #F5F3FF, #FFFFFF);
    }
    .stat-number-custom {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E40AF;
        margin-bottom: 5px;
    }
    .stat-label-custom {
        color: #64748B;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        padding: 40px 0 30px;
        border-top: 1px solid #F1F5F9;
        margin-top: 60px;
        background: #FAFAFA;
        border-radius: 20px;
    }
    .footer p {
        color: #94A3B8;
        font-size: 0.9rem;
        margin: 8px 0;
    }
    .carousel-wrapper {
        max-width: 1400px;
        margin: 40px auto;
        padding: 0 20px;
    }
    .carousel-outer {
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= SHARED NAVBAR =================
    # render_navbar()  # Uncomment if you have navbar component

    # ================= HERO SECTION =================
    col_t, col_v = st.columns([1, 1.2], gap="large")
    with col_t:
        st.markdown('<div style="margin-top: 10px;"><h1 style="font-size:3.5rem; font-weight:800; color:#1E293B; line-height:1.1;"> AI Powered <span style="color:#1E40AF;">Emotional Care</span></h1><p style="color: #64748B; font-size: 1.1rem; margin-bottom:30px;">Your personal space for mental calm. Designed at NUML to provide intelligent, empathetic support whenever you need it.</p></div>', unsafe_allow_html=True)
        if st.button("✨ Try It Yourself", use_container_width=True, key="hero_try"):
            st.session_state.page = "demo"; st.rerun()

    with col_v:
        components.html("""
        <div style="background: white; border-radius: 20px; padding: 20px; border: 2px solid #E2E8F0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); height: 340px; overflow: hidden; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; margin: 10px;">
            <div id="chat-box" style="flex: 1; overflow-y: auto; padding-right: 10px;"></div>
        </div>
        <script>
        const box = document.getElementById('chat-box');
        const conversations = [
            [{u: "I'm really stressed about my project deadlines.", a: "That sounds overwhelming. Let's break it into smaller tasks."},{u: "I can't focus at all.", a: "Try a short 2-minute breathing pause. It helps reset your focus."},{u: "What if I miss the deadline?", a: "Worst case, you communicate early with your manager. Most deadlines can be negotiated."}],
            [{u: "I feel anxious about my presentation tomorrow.", a: "Practice out loud 3 times tonight. It builds confidence."},{u: "What if I forget my lines?", a: "Keep bullet points on index cards as backup. You'll do great!"},{u: "Thanks, that helps.", a: "You're welcome! Get good rest tonight."}],
            [{u: "My team isn't cooperating well.", a: "Have you tried a quick 5-min standup meeting?"},{u: "They ignore my suggestions.", a: "Try asking 'What if we tried...' instead of giving direct orders."},{u: "That might work.", a: "Lead with curiosity. It opens conversations."}]
        ];
        let convIndex = 0, msgIndex = 0, isPlaying = true;
        function createMsg(text, isUser) {
            const msg = document.createElement('div');
            msg.style.display = 'flex';
            msg.style.marginBottom = '12px';
            msg.style.justifyContent = isUser ? 'flex-start' : 'flex-end';
            const bubble = document.createElement('div');
            bubble.style.padding = '10px 14px';
            bubble.style.borderRadius = isUser ? '0 15px 15px 15px' : '15px 0 15px 15px';
            bubble.style.fontSize = '14px';
            bubble.style.maxWidth = '75%';
            bubble.style.transition = 'all 0.3s ease';
            if (isUser) { bubble.style.background = '#F1F5F9'; bubble.innerText = "👤 " + text; }
            else { bubble.style.background = '#1E40AF'; bubble.style.color = 'white'; bubble.innerText = "🧠 " + text; }
            msg.appendChild(bubble);
            return msg;
        }
        function clearChat() {
            return new Promise((resolve) => {
                box.style.opacity = '0';
                setTimeout(() => { while(box.firstChild) box.removeChild(box.firstChild); box.style.opacity = '1'; resolve(); }, 500);
            });
        }
        async function playConversation() {
            if (!isPlaying) return;
            const conv = conversations[convIndex];
            for (let i = 0; i < conv.length; i++) {
                const userMsg = createMsg(conv[i].u, true);
                box.appendChild(userMsg);
                box.scrollTop = box.scrollHeight;
                await new Promise(resolve => setTimeout(resolve, 1500));
                const botMsg = createMsg(conv[i].a, false);
                box.appendChild(botMsg);
                box.scrollTop = box.scrollHeight;
                if (i < conv.length - 1) await new Promise(resolve => setTimeout(resolve, 1500));
            }
            await new Promise(resolve => setTimeout(resolve, 2000));
            await clearChat();
            convIndex = (convIndex + 1) % conversations.length;
            setTimeout(playConversation, 500);
        }
        playConversation();
        </script>
        """, height=400)

    # ================= QUOTE CAROUSEL =================
    st.markdown('<div class="carousel-wrapper"><div class="carousel-outer">', unsafe_allow_html=True)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head><style>
        body { margin:0; background:transparent; font-family:'Inter',sans-serif; }
        .carousel-container { width:100%; overflow:hidden; position:relative; height:350px; background:transparent; }
        .carousel-track { display:flex; width:400%; height:100%; transition:transform 0.7s ease-in-out; }
        .slide { width:25%; height:100%; background-size:cover; background-position:center; display:flex; align-items:center; justify-content:center; flex-shrink:0; position:relative; }
        .slide::before { content:""; position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.2); }
        .quote-card { background:rgba(255,255,255,0.85); backdrop-filter:blur(8px); border-radius:40px; padding:30px 50px; max-width:800px; box-shadow:0 20px 40px rgba(0,0,0,0.2); text-align:center; border:1px solid rgba(255,255,255,0.3); z-index:2; margin:0 20px; }
        .quote-text { color:#0f172a; font-size:28px; font-weight:500; line-height:1.5; font-style:italic; margin:0; }
        .quote-author { margin-top:20px; color:#334155; font-size:16px; }
    </style></head>
    <body>
    <div class="carousel-container"><div class="carousel-track" id="carouselTrack">
        <div class="slide" style="background-image:linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.2)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');"><div class="quote-card"><p class="quote-text">"Healing takes time, and asking for help is a courageous step."</p><p class="quote-author">— MindCare AI</p></div></div>
        <div class="slide" style="background-image:linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.2)),url('https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?q=80&w=2100&auto=format&fit=crop');"><div class="quote-card"><p class="quote-text">"Your mental health is a priority. Your happiness is essential."</p><p class="quote-author">— MindCare AI</p></div></div>
        <div class="slide" style="background-image:linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.2)),url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2100&auto=format&fit=crop');"><div class="quote-card"><p class="quote-text">"It's okay to not be okay. Just don't give up."</p><p class="quote-author">— MindCare AI</p></div></div>
        <div class="slide" style="background-image:linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.2)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');"><div class="quote-card"><p class="quote-text">"Healing takes time, and asking for help is a courageous step."</p><p class="quote-author">— MindCare AI</p></div></div>
    </div></div>
    <script>
        const track = document.getElementById('carouselTrack');
        let currentIndex = 0;
        const totalSlides = 3;
        const slideWidth = 25;
        function moveToNext() {
            currentIndex++;
            track.style.transform = `translateX(-${currentIndex * slideWidth}%)`;
            if (currentIndex === totalSlides) {
                setTimeout(() => {
                    track.style.transition = 'none';
                    track.style.transform = `translateX(0%)`;
                    currentIndex = 0;
                    track.getBoundingClientRect();
                    track.style.transition = 'transform 0.7s ease-in-out';
                }, 700);
            }
        }
        setInterval(moveToNext, 5000);
    </script>
    </body></html>
    """, height=350)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ================= MENTAL WELLNESS EXERCISES WITH VIDEOS =================
    st.markdown('<h2 class="section-title">🧘 Mental Wellness Exercises</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; color: #64748B; font-size: 1.1rem; margin-bottom: 40px;">
    Try these evidence-based exercises to support your mental well-being
    </p>
    """, unsafe_allow_html=True)
    
    # Read and encode first video (Breathing Exercise)
    # video_path_1 = r"C:\Users\shams\OneDrive\Documents\FYP_Mental_Health_Chatbot\assets\videos\fdc9691b2636acbc174610f97f618f6b.mp4"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    video_path_1 = os.path.join(BASE_DIR, "../../assets/videos/videobreathe.mp4")
    try:
        with open(video_path_1, "rb") as video_file:
            video_base64_1 = base64.b64encode(video_file.read()).decode()
        video_available_1 = True
    except FileNotFoundError:
        video_available_1 = False
        st.warning(f"Video file not found at: {video_path_1}")
        video_base64_1 = ""
    
    # Read and encode second video (Mindfulness - Nature video)
# <<<<<<< HEAD
#     video_path_2 = r"C:\Users\shams\OneDrive\Documents\FYP_Mental_Health_Chatbot\assets\videos\87513738abcee839311bbacc5319746b.mp4"
# =======
#     video_path_2 = r"C:\Users\HP\Desktop\Mental-Health-Chatbot\assets\videos\8712234-hd_1080_1920_25fps.mp4"
# >>>>>>> a74193bbe2cdcc5da92f7329082d7b36099cf0fc
    video_path_2 = os.path.join(BASE_DIR, "../../assets/videos/video1.mp4")

    
    try:
        with open(video_path_2, "rb") as video_file:
            video_base64_2 = base64.b64encode(video_file.read()).decode()
        video_available_2 = True
    except FileNotFoundError:
        video_available_2 = False
        st.warning(f"Video file not found at: {video_path_2}")
        video_base64_2 = ""
    
    # Exercise 1 - Breathing WITH VIDEO ON THE RIGHT SIDE
    if video_available_1:
        st.markdown(f"""
        <div class="exercise-card exercise-card-1">
            <div class="exercise-icon-large">🌬️</div>
            <div class="exercise-content">
                <div class="exercise-title">Breathing Exercise</div>
                <div class="exercise-quote">
                    "Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."
                    <div class="exercise-quote-author">— Thich Nhat Hanh</div>
                </div>
                <ul class="exercise-steps">
                    <li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li>
                    <li><span class="step-number">2</span> Hold your breath for 4 seconds</li>
                    <li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li>
                    <li><span class="step-number">4</span> Repeat 5-10 times <span class="exercise-image-small">🧘</span></li>
                </ul>
            </div>
            <div class="exercise-video">
                <video autoplay muted loop playsinline>
                    <source src="data:video/mp4;base64,{video_base64_1}" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exercise-card exercise-card-1">
            <div class="exercise-icon-large">🌬️</div>
            <div class="exercise-content">
                <div class="exercise-title">Breathing Exercise</div>
                <div class="exercise-quote">
                    "Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."
                    <div class="exercise-quote-author">— Thich Nhat Hanh</div>
                </div>
                <ul class="exercise-steps">
                    <li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li>
                    <li><span class="step-number">2</span> Hold your breath for 4 seconds</li>
                    <li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li>
                    <li><span class="step-number">4</span> Repeat 5-10 times <span class="exercise-image-small">🧘</span></li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Exercise 2 - Mindfulness WITH NATURE VIDEO ON THE RIGHT SIDE
    if video_available_2:
        st.markdown(f"""
        <div class="exercise-card exercise-card-2">
            <div class="exercise-icon-large">🧠</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindfulness</div>
                <div class="exercise-quote">
                    "The present moment is filled with joy and happiness. If you are attentive, you will see it."
                    <div class="exercise-quote-author">— Thich Nhat Hanh</div>
                </div>
                <ul class="exercise-steps">
                    <li><span class="step-number">1</span> Sit comfortably and close your eyes</li>
                    <li><span class="step-number">2</span> Focus on your breath without judgment</li>
                    <li><span class="step-number">3</span> Notice thoughts and let them pass</li>
                    <li><span class="step-number">4</span> Practice for 5-10 minutes daily <span class="exercise-image-small">🧠</span></li>
                </ul>
            </div>
            <div class="exercise-video">
                <video autoplay muted loop playsinline>
                    <source src="data:video/mp4;base64,{video_base64_2}" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exercise-card exercise-card-2">
            <div class="exercise-icon-large">🧠</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindfulness</div>
                <div class="exercise-quote">
                    "The present moment is filled with joy and happiness. If you are attentive, you will see it."
                    <div class="exercise-quote-author">— Thich Nhat Hanh</div>
                </div>
                <ul class="exercise-steps">
                    <li><span class="step-number">1</span> Sit comfortably and close your eyes</li>
                    <li><span class="step-number">2</span> Focus on your breath without judgment</li>
                    <li><span class="step-number">3</span> Notice thoughts and let them pass</li>
                    <li><span class="step-number">4</span> Practice for 5-10 minutes daily <span class="exercise-image-small">🧠</span></li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Exercise 3 - Grounding (No video for this one)
    st.markdown("""
    <div class="exercise-card exercise-card-3">
        <div class="exercise-icon-large">🌍</div>
        <div class="exercise-content">
            <div class="exercise-title">5-4-3-2-1 Grounding</div>
            <div class="exercise-quote">
                "Grounding is a powerful way to calm anxiety and return to the present moment."
                <div class="exercise-quote-author">— MindCare AI</div>
            </div>
            <ul class="exercise-steps">
                <li><span class="step-number">👁️</span> Acknowledge 5 things you see</li>
                <li><span class="step-number">🫂</span> Acknowledge 4 things you can touch</li>
                <li><span class="step-number">👂</span> Acknowledge 3 things you hear</li>
                <li><span class="step-number">👃</span> Acknowledge 2 things you can smell</li>
                <li><span class="step-number">👅</span> Acknowledge 1 thing you can taste <span class="exercise-image-small">🌿</span></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= FEATURES =================
    st.markdown('<h2 class="section-title">🎯 Core Capabilities</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">💬</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">Sentiment Analysis</div><div style="font-size:0.85rem;color:#64748B;">Detects real-time emotions to provide empathetic support</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">📊</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">Mood Tracking</div><div style="font-size:0.85rem;color:#64748B;">Visual analytics to monitor your emotional progress</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">🛡️</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">Crisis Guard</div><div style="font-size:0.85rem;color:#64748B;">Instant detection of high-risk keywords for safety</div></div>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">🎤</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">Voice Support</div><div style="font-size:0.85rem;color:#64748B;">Interact naturally using high-accuracy speech-to-text</div></div>', unsafe_allow_html=True)
    with col5: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">📚</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">RAG Knowledge</div><div style="font-size:0.85rem;color:#64748B;">Powered by WHO guidelines for verified medical safety</div></div>', unsafe_allow_html=True)
    with col6: st.markdown('<div class="feature-card-custom"><div style="font-size:38px;margin-bottom:12px;">🧘</div><div style="font-weight:700;font-size:1.1rem;margin:8px 0;color:#1E293B;">Coping Tools</div><div style="font-size:0.85rem;color:#64748B;">AI-suggested meditation and CBT grounding techniques</div></div>', unsafe_allow_html=True)

    # ================= TECH STACK =================
    st.markdown('<h2 class="section-title">🔧 Technology Stack</h2>', unsafe_allow_html=True)
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    with tech_col1: st.markdown('<div class="tech-card-custom"><div style="font-size:2.8rem;margin-bottom:12px;">⚡</div><div style="font-size:1.1rem;font-weight:700;margin-bottom:5px;color:#1E293B;">Frontend</div><div style="font-size:0.85rem;color:#64748B;">Streamlit</div></div>', unsafe_allow_html=True)
    with tech_col2: st.markdown('<div class="tech-card-custom"><div style="font-size:2.8rem;margin-bottom:12px;">🤖</div><div style="font-size:1.1rem;font-weight:700;margin-bottom:5px;color:#1E293B;">AI Engine</div><div style="font-size:0.85rem;color:#64748B;">LLM + RAG</div></div>', unsafe_allow_html=True)
    with tech_col3: st.markdown('<div class="tech-card-custom"><div style="font-size:2.8rem;margin-bottom:12px;">🗄️</div><div style="font-size:1.1rem;font-weight:700;margin-bottom:5px;color:#1E293B;">Backend</div><div style="font-size:0.85rem;color:#64748B;">FastAPI</div></div>', unsafe_allow_html=True)
    with tech_col4: st.markdown('<div class="tech-card-custom"><div style="font-size:2.8rem;margin-bottom:12px;">🎤</div><div style="font-size:1.1rem;font-weight:700;margin-bottom:5px;color:#1E293B;">Voice</div><div style="font-size:0.85rem;color:#64748B;">Whisper</div></div>', unsafe_allow_html=True)

    # ================= IMPACT =================
    st.markdown('<h2 class="section-title">📊 Impact</h2>', unsafe_allow_html=True)
    imp_col1, imp_col2, imp_col3, imp_col4 = st.columns(4)
    with imp_col1: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">24/7</div><div class="stat-label-custom">Availability</div></div>', unsafe_allow_html=True)
    with imp_col2: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">100%</div><div class="stat-label-custom">Anonymous</div></div>', unsafe_allow_html=True)
    with imp_col3: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">50+</div><div class="stat-label-custom">Sources</div></div>', unsafe_allow_html=True)
    with imp_col4: st.markdown('<div class="impact-card-custom"><div class="stat-number-custom">Real-time</div><div class="stat-label-custom">Detection</div></div>', unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div class="footer">
        <p>© 2026 Mind Care AI | National University of Modern Languages, Islamabad</p>
        <p>Final Year Project | Department of Computer Science</p>
        <p>Supervised by Faisal Hussain</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    show_landing_page()