import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods
from layout_utils import apply_professional_design_system
from datetime import datetime, timedelta, date
from db import get_all_user_messages

def show_mood_analytics(user_id):
    # apply_professional_design_system()

    # ================= ENHANCED CSS =================
    st.markdown("""
    <style>
    /* ========== HIDE STREAMLIT DEFAULTS ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
    /* ========== MAIN CONTAINER ========== */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    /* ========== BACKGROUND ========== */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%) !important;
    }
    
    /* ========== TITLE STYLING ========== */
    .mood-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6, #60a5fa);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent !important;
        animation: fadeInDown 0.6s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ========== SECTION HEADERS ========== */
    .section-header {
        font-size: 24px;
        font-weight: 600;
        color: #1e293b;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #3b82f6;
        display: inline-block;
    }
    
    .center-text {
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 25px;
    }
    
    /* ========== MOOD RADIO BUTTONS ========== */
    .main div[role="radiogroup"] {
        justify-content: center !important;
        gap: 20px !important;
        margin: 20px 0 !important;
    }
    
    .main div[role="radiogroup"] label {
        background: white !important;
        padding: 12px 24px !important;
        border-radius: 50px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
    }
    
    .main div[role="radiogroup"] label:hover {
        transform: translateY(-2px);
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    
    .main div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        border-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* ========== LOG MOOD BUTTON - CENTERED ========== */
    .log-button-container {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 50px !important;
        height: 52px !important;
        padding: 0 40px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* ========== SELECTBOX STYLING ========== */
    div[data-testid="stSelectbox"] {
        margin: 20px 0;
    }
    
    div[data-testid="stSelectbox"] label {
        font-weight: 600 !important;
        color: #1e293b !important;
        font-size: 15px !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        background: white !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
        border-color: #3b82f6 !important;
    }
    
    /* ========== INSIGHT CARD ========== */
    .insight-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
        border-left: 5px solid #8b5cf6;
        padding: 24px;
        border-radius: 20px;
        margin: 30px 0;
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255,255,255,0.3);
        border-right: 1px solid rgba(255,255,255,0.3);
        border-bottom: 1px solid rgba(255,255,255,0.3);
        animation: fadeInUp 0.5s ease-out;
    }
    
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
    
    .insight-card b {
        font-size: 18px;
        color: #1e293b;
    }
    
    /* ========== STATS CARDS ========== */
    .stats-wrapper {
        display: flex;
        gap: 20px;
        margin: 30px 0 40px 0;
    }
    
    .stat-card {
        flex: 1;
        padding: 24px 18px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.15);
    }
    
    .stat-card:nth-child(1) { 
        background: linear-gradient(135deg, #ffffff, #f0fdf4);
        border-bottom: 3px solid #10b981;
    }
    .stat-card:nth-child(2) { 
        background: linear-gradient(135deg, #ffffff, #eff6ff);
        border-bottom: 3px solid #3b82f6;
    }
    .stat-card:nth-child(3) { 
        background: linear-gradient(135deg, #ffffff, #fdf2f8);
        border-bottom: 3px solid #ec4899;
    }
    
    .stat-value { 
        font-size: 32px; 
        font-weight: 800; 
        color: #1e293b;
        margin-bottom: 8px;
    }
    
    .stat-label { 
        font-size: 14px; 
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ========== TIMELINE WRAPPER ========== */
    .timeline-wrapper {
        background: white;
        padding: 0px;
        border-radius: 20px;
        margin-top: 40px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .timeline-wrapper:hover {
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.1);
    }
    
    /* ========== INFO MESSAGES ========== */
    .stInfo {
        background: linear-gradient(135deg, #e0f2fe, #bae6fd) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        border-left: 4px solid #0ea5e9 !important;
        color: #0c4a6e !important;
        font-weight: 500 !important;
    }
    
    /* ========== SUCCESS MESSAGES ========== */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
        font-weight: 500 !important;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ========== DIVIDER ========== */
    hr {
        margin: 30px 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, transparent) !important;
    }
    
    /* ========== RESPONSIVE DESIGN ========== */
    @media (max-width: 768px) {
        .stats-wrapper {
            flex-direction: column;
            gap: 15px;
        }
        
        .mood-title {
            font-size: 32px !important;
        }
        
        .section-header {
            font-size: 20px !important;
        }
        
        div[role="radiogroup"] {
            flex-direction: column !important;
            align-items: center !important;
        }
        
        div[role="radiogroup"] label {
            width: 80% !important;
            text-align: center !important;
        }
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e2e8f0;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2563eb;
    }
    
    /* ========== MATPLOTLIB FIGURE STYLING ========== */
    .timeline-wrapper .stPlotlyChart, 
    .timeline-wrapper .stImage {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown("<h1 class='mood-title'>📈 Mood Tracker</h1>", unsafe_allow_html=True)
    
    st.markdown("---")

    # ================= QUICK MOOD LOG - BETTER VERSION =================
# ================= QUICK MOOD LOG (USING st.toast) =================
    st.markdown('<div class="section-header">😊 Quick Mood Log</div>', unsafe_allow_html=True)

    mood = st.radio(
        "",
        ["😄 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        horizontal=True,
        key="mood_radio"
    )

    # Centralized Log Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Log My Mood", key="log_mood_btn", use_container_width=True):
            mood_text = mood.split(" ", 1)[1]
            add_mood(user_id, mood_text)
            # Professional built-in toast
            st.toast(f"🎉 Mood '{mood_text}' logged successfully!", icon="✅")
            st.balloons()  # Optional: fun effect

    st.markdown("---")

    # ================= FILTER SECTION =================
    st.markdown('<div class="section-header">📅 Mood Trend Timeline</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        range_option = st.selectbox(
            "Select Time Range",
            ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"],
            key="time_range"
        )

    moods = get_moods(user_id)
    mood_list = ["Happy", "Neutral", "Sad", "Anxious", "Angry"]

    if moods:
        if range_option == "Last 7 Days":
            filtered = moods[-7:]
        elif range_option == "Last 30 Days":
            filtered = moods[-30:]
        elif range_option == "Last 3 Months":
            filtered = moods[-90:]
        else:
            filtered = moods
    else:
        filtered = []

    # ================= ANALYTICS SECTION =================
    if filtered:

        mood_counts = {m: filtered.count(m) for m in mood_list if m in filtered}
        total = len(filtered)
        most_common = max(mood_counts, key=mood_counts.get)
        variety = len(set(filtered))

        # Insight Card
        st.markdown(f"""
        <div class='insight-card'>
            <b>🌿 Emotional Insight</b><br><br>
            Based on your {total} mood entries, your emotional pattern shows a tendency toward <b>{most_common}</b> moods. 
            You've experienced <b>{variety}</b> different emotional states during this period.
        </div>
        """, unsafe_allow_html=True)

        # Stats Cards
        st.markdown("""
        <div class='stats-wrapper'>
            <div class='stat-card'>
                <div class='stat-value'>""" + str(total) + """</div>
                <div class='stat-label'>Total Entries</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>""" + most_common + """</div>
                <div class='stat-label'>Most Frequent</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>""" + str(variety) + """</div>
                <div class='stat-label'>Mood Variety</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ================= MOOD TREND GRAPH =================
        if len(filtered) > 1:
            st.markdown("<div class='timeline-wrapper'>", unsafe_allow_html=True)
            st.markdown("### 📊 Mood Trend Analysis")

            y_map = {"Happy": 5, "Neutral": 3, "Sad": 2, "Anxious": 1, "Angry": 0}
            x = list(range(len(filtered)))
            y = [y_map[m] for m in filtered]

            # Create styled figure
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(x, y, marker='o', linewidth=2.5, markersize=8, 
                   color='#3b82f6', markerfacecolor='#2563eb', 
                   markeredgecolor='white', markeredgewidth=2)
            
            # Add gradient fill under the line
            ax.fill_between(x, y, alpha=0.2, color='#3b82f6')

            ax.set_yticks([0, 1, 2, 3, 5])
            ax.set_yticklabels(["Angry", "Anxious", "Sad", "Neutral", "Happy"])
            ax.set_xticks(x)
            ax.set_xticklabels([f"Day {i+1}" for i in x], rotation=45, ha='right')

            ax.set_title(f"Mood Trend – {range_option}", fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel("Timeline", fontsize=11)
            ax.set_ylabel("Mood Level", fontsize=11)
            ax.grid(alpha=0.15, linestyle='--')
            ax.set_facecolor('#f8fafc')
            fig.patch.set_facecolor('white')

            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

            # ================= CHAT-BASED TREND =================
            all_msgs = get_all_user_messages(user_id) or []
            cutoff_map = {
                "Last 7 Days": datetime.now() - timedelta(days=7),
                "Last 30 Days": datetime.now() - timedelta(days=30),
                "Last 3 Months": datetime.now() - timedelta(days=90),
                "All Time": None,
            }
            cutoff = cutoff_map.get(range_option)

            stress_keywords = [
                "stress", "stressed", "anxious", "anxiety", "panic", "overwhelmed", "depress",
                "depressed", "sad", "cry", "lonely", "tired", "can't", "cant", "hopeless",
                "worthless", "pressure", "worried", "worry", "fear"
            ]

            daily_count = {}
            daily_stress = {}

            for role, content, ts, conv_id in all_msgs:
                if not ts:
                    continue
                if isinstance(ts, datetime):
                    dt = ts
                else:
                    try:
                        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                    except Exception:
                        continue
                if cutoff and dt < cutoff:
                    continue

                d = dt.date()
                daily_count[d] = daily_count.get(d, 0) + 1

                text = (content or "").lower()
                score = sum(text.count(k) for k in stress_keywords)
                daily_stress[d] = daily_stress.get(d, 0) + score

            if daily_count:
                days_sorted = sorted(daily_count.keys())
                x2 = list(range(len(days_sorted)))
                counts = [daily_count[d] for d in days_sorted]
                stress = [daily_stress.get(d, 0) for d in days_sorted]

                st.markdown("<div class='timeline-wrapper' style='margin-top: 30px;'>", unsafe_allow_html=True)
                st.markdown("### 💬 Chat Activity Insights")

                fig2, ax2 = plt.subplots(figsize=(11, 4))
                ax2.plot(x2, counts, marker='o', linewidth=2.5, markersize=7, 
                        label="Messages per day", color='#10b981')
                ax2.plot(x2, stress, marker='s', linewidth=2.5, markersize=7, 
                        label="Stress indicators", color='#ef4444')
                
                ax2.fill_between(x2, counts, alpha=0.1, color='#10b981')
                ax2.fill_between(x2, stress, alpha=0.1, color='#ef4444')
                
                ax2.set_title("Chat Activity & Stress Level Correlation", fontsize=14, fontweight='bold', pad=20)
                ax2.set_xlabel("Date", fontsize=11)
                ax2.set_ylabel("Count / Score", fontsize=11)
                ax2.set_xticks(x2)
                ax2.set_xticklabels([d.strftime("%b %d") for d in days_sorted], rotation=45, ha="right")
                ax2.grid(alpha=0.15, linestyle='--')
                ax2.legend(loc='upper left', framealpha=0.9)
                ax2.set_facecolor('#f8fafc')
                fig2.patch.set_facecolor('white')

                st.pyplot(fig2)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("📭 No chat history found for the selected time range.")

        else:
            st.info("📊 Need more mood entries to show trend analysis. Keep logging your mood daily!")
    else:
        st.info("🌸 Start logging your moods to see beautiful analytics and insights about your emotional wellness journey!")