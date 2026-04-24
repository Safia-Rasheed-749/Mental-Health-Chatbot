import streamlit as st
import streamlit.components.v1 as components

def show_landing_page():
    # ================= STYLE ENGINE =================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Remove ALL default padding from top */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    section.main > div {
        padding-top: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(
    to bottom right,
    #ffffff,
    #eaf6fb,
    #d6ecf7
    );   
     header, #MainMenu, footer {visibility: hidden;}
    
    /* Remove top margin completely */
    .stApp {
        margin-top: -80px !important;
    }
    
    / /* ===== NAVIGATION BAR ===== */
    .nav-container {
        background: purple !important;
        padding: 12px 30px !important;
        border-radius: 60px !important;
        box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3) !important;
        margin: 10px 0 30px 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 36px;
        font-weight: 700;
        color: #6D9EEB !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .logo-icon {
        font-size: 36px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    /* ===== BUTTON STYLES - COMPACT HORIZONTAL SIZE, PROPER SPACING ===== */
    div.stButton > button {
        all: unset !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: linear-gradient(135deg, #9FC6F0, #4F84D9) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 6px 18px !important;  /* Reduced horizontal padding */
        border-radius: 40px !important;
        font-size: 15px !important;    /* Slightly smaller font */
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        min-width: auto !important;     /* Remove fixed min-width */
        cursor: pointer !important;
        line-height: normal !important;
        height: auto !important;
        white-space: nowrap !important;
        margin: 0 10px !important;      /* Increased horizontal margin */
    }
    
    div.stButton > button:hover {
        background: #6D9EEB !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3) !important;
    }
    
    /* Get Started button special - slightly larger */
    button[key="nav_getstarted_about"] {
        background: purple !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 6px 22px !important;
        min-width: auto !important;
    }
    
    button[key="nav_getstarted_about"]:hover {
        background: #ff4444 !important;
        box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3) !important;
    }
    
    /* Ensure columns have space between buttons */
    .stColumn {
        display: flex;
        justify-content: center;
        gap: 0;  /* No extra gap, handled by button margins */
    }}
    
    /* Section Titles - WITHOUT underline */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E293B;
        margin: 60px 0 20px 0;
        position: relative;
    }
    /* Removed the ::after pseudo-element that created the horizontal line */

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
    
    /* Updated colors: soft lavender, soft blue, soft teal */
    .exercise-card-1 { background: #F3E8FF; border-left: 8px solid #A855F7; }  /* lavender */
    .exercise-card-2 { background: #DBEAFE; border-left: 8px solid #3B82F6; }  /* soft blue */
    .exercise-card-3 { background: #CCFBF1; border-left: 8px solid #14B8A6; }  /* soft teal */
    
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
    
    .exercise-content {
        flex: 1;
    }
    
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
    
    .exercise-image-small {
        font-size: 1.2rem;
        margin-left: 5px;
    }

    /* ===== FEATURE BOX STYLE ===== */
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
    
    /* ===== TECH CARD STYLE ===== */
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
    
    /* ===== IMPACT CARD STYLE ===== */
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

    /* ===== FOOTER ===== */
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
    /* Carousel container */
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

    # ================= NAVIGATION =================
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div class="logo">
                <span class="logo-icon">🧠</span>
                <span>Mind Care AI</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1.2])
        
        with nav_col1:
            if st.button("🏠 Home", key="nav_home_about", use_container_width=False):
                st.session_state.page = "landing"
                st.rerun()
        
        with nav_col2:
            if st.button("📖 About", key="nav_about_about", use_container_width=False):
                st.session_state.page = "about"
                st.rerun()
        
        with nav_col3:
            if st.button("🚀 Demo", key="nav_demo_about", use_container_width=False):
                st.session_state.demo_messages = []
                st.session_state.demo_count = 0
                st.session_state.page = "demo"
                st.rerun()
        
        with nav_col4:
            if st.button("🚀 Get Started", key="nav_getstarted_about", use_container_width=False):
                st.session_state.page = "auth"
                st.rerun()

    # ================= HERO SECTION =================
    col_t, col_v = st.columns([1, 1.2], gap="large")
    with col_t:
        st.markdown('<div style="margin-top: 10px;"><h1 style="font-size:3.5rem; font-weight:800; color:#1E293B; line-height:1.1;"> AI Powered <span style="color:#1E40AF;">Emotional Care</span></h1><p style="color: #64748B; font-size: 1.1rem; margin-bottom:30px;">Your personal space for mental calm. Designed at NUML to provide intelligent, empathetic support whenever you need it.</p></div>', unsafe_allow_html=True)
        if st.button("✨ Try It Yourself", use_container_width=True, key="hero_try"):
            st.session_state.page = "demo"; st.rerun()

    with col_v:
        components.html("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 20px;
            border: 2px solid #E2E8F0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            height: 340px; 
            overflow: hidden;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            margin: 10px;
        ">
            <div id="chat-box" style="flex: 1; overflow-y: auto; padding-right: 10px;"></div>
        </div>

        <script>
        const box = document.getElementById('chat-box');
        const conversations = [
            [
                {u: "I'm really stressed about my project deadlines.", a: "That sounds overwhelming. Let's break it into smaller tasks."},
                {u: "I can't focus at all.", a: "Try a short 2-minute breathing pause. It helps reset your focus."},
                {u: "What if I miss the deadline?", a: "Worst case, you communicate early with your manager. Most deadlines can be negotiated."}
            ],
            [
                {u: "I feel anxious about my presentation tomorrow.", a: "Practice out loud 3 times tonight. It builds confidence."},
                {u: "What if I forget my lines?", a: "Keep bullet points on index cards as backup. You'll do great!"},
                {u: "Thanks, that helps.", a: "You're welcome! Get good rest tonight."}
            ],
            [
                {u: "My team isn't cooperating well.", a: "Have you tried a quick 5-min standup meeting?"},
                {u: "They ignore my suggestions.", a: "Try asking 'What if we tried...' instead of giving direct orders."},
                {u: "That might work.", a: "Lead with curiosity. It opens conversations."}
            ]
        ];
        
        let convIndex = 0;
        let msgIndex = 0;
        let isPlaying = true;
        
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
            if (isUser) {
                bubble.style.background = '#F1F5F9';
                bubble.innerText = "👤 " + text;
            } else {
                bubble.style.background = '#1E40AF';
                bubble.style.color = 'white';
                bubble.innerText = "🧠 " + text;
            }
            msg.appendChild(bubble);
            return msg;
        }
        
        function clearChat() {
            return new Promise((resolve) => {
                box.style.opacity = '0';
                setTimeout(() => {
                    while(box.firstChild) {
                        box.removeChild(box.firstChild);
                    }
                    box.style.opacity = '1';
                    resolve();
                }, 500);
            });
        }
        
        async function playConversation() {
            if (!isPlaying) return;
            
            const conv = conversations[convIndex];
            
            // Show all 3 messages one by one
            for (let i = 0; i < conv.length; i++) {
                // Show user message
                const userMsg = createMsg(conv[i].u, true);
                box.appendChild(userMsg);
                box.scrollTop = box.scrollHeight;
                
                // Wait 1.5 seconds before showing bot response
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Show bot response
                const botMsg = createMsg(conv[i].a, false);
                box.appendChild(botMsg);
                box.scrollTop = box.scrollHeight;
                
                // Wait 1.5 seconds before next message
                if (i < conv.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1500));
                }
            }
            
            // Wait 2 seconds then clear and move to next conversation
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Clear chat with fade effect
            await clearChat();
            
            // Move to next conversation
            convIndex = (convIndex + 1) % conversations.length;
            
            // Wait 0.5 seconds then play next conversation
            setTimeout(playConversation, 500);
        }
        
        // Start the conversation loop
        playConversation();
        </script>
        """, height=400)
    # ================= SLIDING QUOTE CAROUSEL =================
    st.markdown('<div class="carousel-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="carousel-outer">', unsafe_allow_html=True)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            background: transparent;
            font-family: 'Inter', sans-serif;
        }
        .carousel-container {
            width: 100%;
            overflow: hidden;
            position: relative;
            height: 350px;
            background: transparent;
        }
        .carousel-track {
            display: flex;
            width: 400%;
            height: 100%;
            transition: transform 0.7s ease-in-out;
        }
        .slide {
            width: 25%;
            height: 100%;
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            position: relative;
        }
        .slide::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.2);
        }
        .quote-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(8px);
            border-radius: 40px;
            padding: 30px 50px;
            max-width: 800px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
            z-index: 2;
            margin: 0 20px;
        }
        .quote-text {
            color: #0f172a;
            font-size: 28px;
            font-weight: 500;
            line-height: 1.5;
            font-style: italic;
            margin: 0;
        }
        .quote-author {
            margin-top: 20px;
            color: #334155;
            font-size: 16px;
            font-weight: 400;
        }
    </style>
    </head>
    <body>
    <div class="carousel-container">
        <div class="carousel-track" id="carouselTrack">
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Healing takes time, and asking for help is a courageous step.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Your mental health is a priority. Your happiness is essential.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“It’s okay to not be okay. Just don’t give up.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
            <div class="slide" style="background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2100&auto=format&fit=crop');">
                <div class="quote-card">
                    <p class="quote-text">“Healing takes time, and asking for help is a courageous step.”</p>
                    <p class="quote-author">— MindCare AI</p>
                </div>
            </div>
        </div>
    </div>

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
    </body>
    </html>
    """, height=350)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # ================= MENTAL WELLNESS EXERCISES (VERTICALLY) =================
    st.markdown('<h2 class="section-title">🧘 Mental Wellness Exercises</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; color: #64748B; font-size: 1.1rem; margin-bottom: 40px;">
    Try these evidence-based exercises to support your mental well-being
    </p>
    """, unsafe_allow_html=True)
    
    # Exercise 1 - Breathing (lavender)
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
    
    # Exercise 2 - Mindfulness (soft blue)
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
    
    # Exercise 3 - Grounding (soft teal)
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

    # ================= CORE FEATURES (2 Rows) =================
    st.markdown('<h2 class="section-title">🎯 Core Capabilities</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">💬</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">Sentiment Analysis</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">Detects real-time emotions to provide empathetic support</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">📊</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">Mood Tracking</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">Visual analytics to monitor your emotional progress</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">🛡️</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">Crisis Guard</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">Instant detection of high-risk keywords for safety</div>
            </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">🎤</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">Voice Support</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">Interact naturally using high-accuracy speech-to-text</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">📚</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">RAG Knowledge</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">Powered by WHO guidelines for verified medical safety</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
            <div class="feature-card-custom">
                <div style="font-size: 38px; margin-bottom: 12px;">🧘</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin: 8px 0; color: #1E293B;">Coping Tools</div>
                <div style="font-size: 0.85rem; color: #64748B; line-height: 1.5;">AI-suggested meditation and CBT grounding techniques</div>
            </div>
        """, unsafe_allow_html=True)

    # ================= TECHNOLOGY STACK =================
    st.markdown('<h2 class="section-title">🔧 Technology Stack</h2>', unsafe_allow_html=True)
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    with tech_col1:
        st.markdown("""
            <div class="tech-card-custom">
                <div style="font-size: 2.8rem; margin-bottom: 12px;">⚡</div>
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; color: #1E293B;">Frontend</div>
                <div style="font-size: 0.85rem; color: #64748B;">Streamlit</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
            <div class="tech-card-custom">
                <div style="font-size: 2.8rem; margin-bottom: 12px;">🤖</div>
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; color: #1E293B;">AI Engine</div>
                <div style="font-size: 0.85rem; color: #64748B;">LLM + RAG</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col3:
        st.markdown("""
            <div class="tech-card-custom">
                <div style="font-size: 2.8rem; margin-bottom: 12px;">🗄️</div>
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; color: #1E293B;">Backend</div>
                <div style="font-size: 0.85rem; color: #64748B;">FastAPI</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col4:
        st.markdown("""
            <div class="tech-card-custom">
                <div style="font-size: 2.8rem; margin-bottom: 12px;">🎤</div>
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; color: #1E293B;">Voice</div>
                <div style="font-size: 0.85rem; color: #64748B;">Whisper</div>
            </div>
        """, unsafe_allow_html=True)

    # ================= IMPACT STATISTICS =================
    st.markdown('<h2 class="section-title">📊 Impact</h2>', unsafe_allow_html=True)
    
    imp_col1, imp_col2, imp_col3, imp_col4 = st.columns(4)
    
    with imp_col1:
        st.markdown("""
            <div class="impact-card-custom">
                <div class="stat-number-custom">24/7</div>
                <div class="stat-label-custom">Availability</div>
            </div>
        """, unsafe_allow_html=True)
    
    with imp_col2:
        st.markdown("""
            <div class="impact-card-custom">
                <div class="stat-number-custom">100%</div>
                <div class="stat-label-custom">Anonymous</div>
            </div>
        """, unsafe_allow_html=True)
    
    with imp_col3:
        st.markdown("""
            <div class="impact-card-custom">
                <div class="stat-number-custom">50+</div>
                <div class="stat-label-custom">Sources</div>
            </div>
        """, unsafe_allow_html=True)
    
    with imp_col4:
        st.markdown("""
            <div class="impact-card-custom">
                <div class="stat-number-custom">Real-time</div>
                <div class="stat-label-custom">Detection</div>
            </div>
        """, unsafe_allow_html=True)

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