# ==================== exercises.py - PROFESSIONAL VERSION ====================
import streamlit as st
import os
import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def show_exercises_page():

    st.markdown("""
    <style>
        header {
            visibility: hidden;
            height: 0px;
            margin: 0px !important;
            padding: 0px !important;
        }

        [data-testid="stHeader"] {
            display: none !important;
            height: 0px !important;
        }

        .main {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .stApp {
            margin-top: 0px !important;
            padding-top: 0px !important;
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
        }
        
        /* ========== PAGE HEADER ========== */
        .page-header {
            text-align: center;
            margin: 20px 0 30px 0;
        }
        
        .page-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }
        
        .page-header p {
            color: #64748b;
            font-size: 1.3rem;
            max-width: 700px;
            margin: 5px auto;
        }
        
        /* ========== EXERCISE CARDS ========== */
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
            flex-wrap: wrap;
            animation: fadeInUp 0.8s ease-out;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        /* Card 1 - Purple/Lavender theme */
        .exercise-card-1 {
            background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-left: 4px solid #8b5cf6;
        }
        
        /* Card 2 - Blue theme */
        .exercise-card-2 {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-left: 4px solid #3b82f6;
        }
        
        /* Card 3 - Purple theme */
        .exercise-card-3 {
            background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-left: 4px solid #a855f7;
        }
        
        .exercise-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
        }
        
        .exercise-icon-large {
            font-size: 3.8rem;
            min-width: 85px;
            text-align: center;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
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
            border-left: 3px solid #8b5cf6;
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
            border-color: #8b5cf6;
            background: rgba(139, 92, 246, 0.05);
        }
        
        .step-number {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
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
        
        /* ========== TIPS SECTION - IMPROVED ========== */
        .tips-wrapper {
            margin: 10px 0 20px 0;
        }
        
        .tips-heading {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .tips-heading h2 {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .tips-heading p {
            color: #64748b;
            font-size: 1.3rem;
        }
        
        .tips-section {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border-radius: 28px;
            padding: 40px 30px;
            color: white;
            text-align: center;
        }
        
        .tips-grid {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        
        .tip-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px 25px;
            min-width: 180px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .tip-card:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-5px);
        }
        
        .tip-card span {
            font-size: 2.2rem;
            display: block;
            margin-bottom: 12px;
        }
        
        .tip-card p {
            font-size: 0.9rem;
            opacity: 0.9;
            margin: 0;
            line-height: 1.4;
        }
        
        /* Regular button style */
        div.stButton > button {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 40px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
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
            .page-header h1 {
                font-size: 1.8rem;
            }
            .tips-heading h2 {
                font-size: 1.5rem;
            }
            .tip-card {
                min-width: 150px;
                padding: 15px 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ================= PAGE HEADER =================
    st.markdown("""
    <div class="page-header">
        <h1>🧘 Mental Wellness Exercises</h1>
        <p><strong>✨ Evidence-based practices for emotional balance</strong></p>
        <p>These scientifically-backed exercises help reduce anxiety, improve focus, and build emotional resilience.</p>
    </div>
    """, unsafe_allow_html=True)    
    
    # ================= VIDEO PATHS =================
    video_path_1 = os.path.join(BASE_DIR, "../../assets/videos/video1.mp4")
    video_path_2 = os.path.join(BASE_DIR, "../../assets/videos/video2.mp4")
    video_path_3 = os.path.join(BASE_DIR, "../../assets/videos/Ins_-359471723.mp4")
    
    def get_video_base64(video_path):
        try:
            if os.path.exists(video_path):
                with open(video_path, "rb") as video_file:
                    video_base64 = base64.b64encode(video_file.read()).decode()
                    return video_base64, True
            else:
                return "", False
        except Exception:
            return "", False
    
    video_base64_1, video_available_1 = get_video_base64(video_path_1)
    video_base64_2, video_available_2 = get_video_base64(video_path_2)
    video_base64_3, video_available_3 = get_video_base64(video_path_3)

    # Exercise 1 - Mindful Breathing
    if video_available_1:
        st.markdown(f"""
        <div class="exercise-card exercise-card-1">
            <div class="exercise-icon-large">🌬️</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindful Breathing Exercise</div>
                <div class="exercise-quote">"Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🌿 Why it helps:</strong> Deep breathing activates your parasympathetic nervous system, reducing cortisol levels and calming anxiety.</div>
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
                <div class="exercise-description-text"><strong>🌿 Why it helps:</strong> Deep breathing activates your parasympathetic nervous system, reducing cortisol levels and calming anxiety.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Inhale deeply through your nose for 4 seconds</li><li><span class="step-number">2</span> Hold your breath for 4 seconds</li><li><span class="step-number">3</span> Exhale slowly through your mouth for 6 seconds</li><li><span class="step-number">4</span> Repeat 5-10 times</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exercise 2 - Mindfulness Meditation
    if video_available_2:
        st.markdown(f"""
        <div class="exercise-card exercise-card-2">
            <div class="exercise-icon-large">🧠</div>
            <div class="exercise-content">
                <div class="exercise-title">Mindfulness Meditation</div>
                <div class="exercise-quote">"The present moment is filled with joy and happiness. If you are attentive, you will see it."<div class="exercise-quote-author">— Thich Nhat Hanh</div></div>
                <div class="exercise-description-text"><strong>🎯 Why it helps:</strong> Mindfulness rewires your brain for greater emotional regulation and reduces stress.</div>
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
                <div class="exercise-description-text"><strong>🎯 Why it helps:</strong> Mindfulness rewires your brain for greater emotional regulation and reduces stress.</div>
                <ul class="exercise-steps"><li><span class="step-number">1</span> Sit comfortably and close your eyes</li><li><span class="step-number">2</span> Focus on your breath without judgment</li><li><span class="step-number">3</span> Notice thoughts and let them pass</li><li><span class="step-number">4</span> Practice for 5-10 minutes daily</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exercise 3 - Grounding Technique
    if video_available_3:
        st.markdown(f"""
        <div class="exercise-card exercise-card-3">
            <div class="exercise-icon-large">🌍</div>
            <div class="exercise-content">
                <div class="exercise-title">5-4-3-2-1 Grounding Technique</div>
                <div class="exercise-quote">"Grounding is a powerful way to calm anxiety and return to the present moment."<div class="exercise-quote-author">— AI Assistant</div></div>
                <div class="exercise-description-text"><strong>⚡ Why it helps:</strong> This evidence-based technique interrupts anxiety spirals by engaging all five senses.</div>
                <ul class="exercise-steps"><li><span class="step-number">👁️</span> Acknowledge 5 things you see around you</li><li><span class="step-number">🫂</span> Acknowledge 4 things you can physically touch</li><li><span class="step-number">👂</span> Acknowledge 3 distinct sounds you hear</li><li><span class="step-number">👃</span> Acknowledge 2 different smells in your environment</li><li><span class="step-number">👅</span> Acknowledge 1 thing you can taste or focus on your breath</li></ul>
            </div>
            <div class="exercise-video"><video autoplay muted loop playsinline><source src="data:video/mp4;base64,{video_base64_3}" type="video/mp4"></video></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exercise-card exercise-card-3">
            <div class="exercise-icon-large">🌍</div>
            <div class="exercise-content">
                <div class="exercise-title">5-4-3-2-1 Grounding Technique</div>
                <div class="exercise-quote">"Grounding is a powerful way to calm anxiety and return to the present moment."<div class="exercise-quote-author">— AI Assistant</div></div>
                <div class="exercise-description-text"><strong>⚡ Why it helps:</strong> This evidence-based technique interrupts anxiety spirals by engaging all five senses.</div>
                <ul class="exercise-steps"><li><span class="step-number">👁️</span> Acknowledge 5 things you see around you</li><li><span class="step-number">🫂</span> Acknowledge 4 things you can physically touch</li><li><span class="step-number">👂</span> Acknowledge 3 distinct sounds you hear</li><li><span class="step-number">👃</span> Acknowledge 2 different smells in your environment</li><li><span class="step-number">👅</span> Acknowledge 1 thing you can taste or focus on your breath</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ================= TIPS SECTION (WITH PROPER HEADING) =================
    st.markdown("""
    <div class="tips-wrapper">
        <div class="tips-heading">
            <h2>✨ Pro Tips for Best Results</h2>
            <p>Small consistent practices create lasting change</p>
        </div>
        <div class="tips-section">
            <div class="tips-grid">
                <div class="tip-card">
                    <span>📅</span>
                    <p>Practice daily for best results</p>
                </div>
                <div class="tip-card">
                    <span>🌅</span>
                    <p>Morning sessions set a calm tone for the day</p>
                </div>
                <div class="tip-card">
                    <span>😴</span>
                    <p>Evening practices improve sleep quality</p>
                </div>
                <div class="tip-card">
                    <span>📝</span>
                    <p>Journal your experience after each exercise</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_exercises_page()