import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods
from datetime import datetime, timedelta, date
from db import get_all_user_messages

def show_mood_analytics(user_id):

    # ================= ENHANCED CSS (CHAT-STYLE) =================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── HIDE CLUTTER ── */
    .stDeployButton { display: none !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu       { visibility: hidden !important; }
    footer          { visibility: hidden !important; }
    header {
        background: transparent !important;
        box-shadow: none !important;
        visibility: visible !important;
    }

    /* ── PAGE BACKGROUND (SAME AS CHAT) ── */
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        background: linear-gradient(160deg, #eef2ff 0%, #f0fdf9 50%, #fdf4ff 100%) !important;
        height: 100%;
    }

    /* ── BLOCK CONTAINER ── */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }

    /* ── HEADER BANNER (SAME AS CHAT) ── */
    .page-header {
        background: linear-gradient(135deg, #4a7fd4 0%, #5fa8e0 55%, #7ecde8 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(99,102,241,0.28);
        border-radius: 20px;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    .page-header-avatar {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        border: 2px solid rgba(255,255,255,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.12);
        animation: headerPulse 3s ease-in-out infinite;
    }
    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(255,255,255,0.12); }
        50%       { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
    }
    .page-header-text h1 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    .page-header-text p {
        margin: 2px 0 0;
        font-size: 18px;
        color: rgba(255,255,255,0.78);
        font-weight: 400;
    }

    
    .mood-section-card:hover {
        box-shadow: 0 8px 28px rgba(99,102,241,0.15);
        transform: translateY(-2px);
    }

    /* Hide Streamlit default elements that create white bars */
    .element-container:has(> .stMarkdown:empty) {
        display: none !important;
    }
    
    /* Remove extra spacing from empty elements */
    .stMarkdown:empty {
        display: none !important;
    }
    
    /* Hide empty columns */
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    /* Remove white background from empty containers */
    .stVerticalBlock:empty {
        display: none !important;
    }

    /* Force hide any white bars from Streamlit columns */
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }

    div[data-testid="column"] {
        background: transparent !important;
    }

    /* Remove padding from empty columns */
    div[data-testid="column"]:has(> div:empty) {
        display: none !important;
    }

    /* Hide element containers with only whitespace */
    .element-container:has(> div:empty) {
        display: none !important;
    }

    /* Remove default Streamlit container backgrounds */
    .stVerticalBlock {
        background: transparent !important;
    }

    .block-container > div {
        background: transparent !important;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ── MOOD RADIO BUTTONS ── */
    .main div[role="radiogroup"] {
        justify-content: center !important;
        gap: 12px !important;
        margin: 16px 0 !important;
        flex-wrap: wrap !important;
    }

    .main div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95)) !important;
        padding: 12px 24px !important;
        border-radius: 16px !important;
        border: 2px solid rgba(99,102,241,0.20) !important;
        transition: all 0.3s ease !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    }

    .main div[role="radiogroup"] label:hover {
        transform: translateY(-2px);
        border-color: #6366f1 !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.20) !important;
    }

    .main div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border-color: #6366f1 !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
    }

    /* ── LOG BUTTON ── */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #4a7fd4 0%, #5fa8e0 55%, #7ecde8 100%);
        color: white !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        height: 48px !important;
        padding: 0 36px !important;
        border: none !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.30) !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(99,102,241,0.40) !important;
    }

    /* ── SELECTBOX ── */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 2px solid rgba(99,102,241,0.25) !important;
        border-radius: 12px !important;
        background: rgba(255,255,255,0.90) !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.15) !important;
    }

    /* ── INSIGHT CARD ── */
    .insight-card {
        background: linear-gradient(135deg, rgba(139,92,246,0.10), rgba(99,102,241,0.10));
        border-left: 4px solid #8b5cf6;
        padding: 20px 24px;
        border-radius: 16px;
        margin: 24px 0;
        border: 1px solid rgba(139,92,246,0.20);
        box-shadow: 0 4px 16px rgba(139,92,246,0.10);
    }

    .insight-card b {
        font-size: 16px;
        color: #1e293b;
        font-weight: 700;
    }

    /* ── STATS CARDS ── */
    .stats-wrapper {
        display: flex;
        gap: 16px;
        margin: 24px 0;
        flex-wrap: wrap;
    }

    .stat-card {
        flex: 1;
        min-width: 200px;
        padding: 20px 18px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(99,102,241,0.10);
        border: 1px solid rgba(99,102,241,0.15);
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.90);
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(99,102,241,0.18);
    }

    .stat-card:nth-child(1) { 
        border-bottom: 3px solid #10b981;
    }
    .stat-card:nth-child(2) { 
        border-bottom: 3px solid #6366f1;
    }
    .stat-card:nth-child(3) { 
        border-bottom: 3px solid #ec4899;
    }

    .stat-value { 
        font-size: 32px; 
        font-weight: 800; 
        color: #1e293b;
        margin-bottom: 8px;
    }

    .stat-label { 
        font-size: 13px; 
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    

    /* ── INFO/SUCCESS MESSAGES ── */
    .stInfo {
        background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(139,92,246,0.10)) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        border-left: 4px solid #6366f1 !important;
        color: #1e293b !important;
        font-weight: 500 !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(16,185,129,0.10), rgba(52,211,153,0.10)) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
        font-weight: 500 !important;
    }

    /* ── DIVIDER ── */
    hr {
        margin: 24px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.30), transparent) !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar       { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }
    </style>
    """, unsafe_allow_html=True)

    # ── HEADER BANNER ──
    st.markdown("""
    <div class="page-header">
        <div class="page-header-avatar">📊</div>
        <div class="page-header-text">
            <h1>Mood Analytics</h1>
            <p>Track and understand your emotional wellness journey</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= QUICK MOOD LOG =================
     
    st.markdown('<div class="section-title">😊 Quick Mood Log</div>', unsafe_allow_html=True)

    mood = st.radio(
        "",
        ["😄 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        horizontal=True,
        key="mood_radio"
    )

    # Centralized Log Button (no empty columns)
    st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
    if st.button("✨ Log My Mood", key="log_mood_btn"):
        mood_text = mood.split(" ", 1)[1]
        add_mood(user_id, mood_text)
        st.toast(f"🎉 Mood '{mood_text}' logged successfully!", icon="✅")
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close mood-section-card

    moods = get_moods(user_id)
    mood_list = ["Happy", "Neutral", "Sad", "Anxious", "Angry"]

    if moods:
        # ================= FILTER SECTION (ONLY SHOW IF MOODS EXIST) =================
        st.markdown('<div class="mood-section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📅 Mood Trend Timeline</div>', unsafe_allow_html=True)

        range_option = st.selectbox(
            "Select Time Range",
            ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"],
            key="time_range"
        )

        st.markdown('</div>', unsafe_allow_html=True)  # Close mood-section-card

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

    # ================= ANALYTICS SECTION (ONLY SHOW IF DATA EXISTS) =================
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

            # ================= MOOD DISTRIBUTION PIE CHART =================
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Spacing
            st.markdown("<div class='chart-wrapper'>", unsafe_allow_html=True)
            
            # Centered heading with larger size
            st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <h2 style='font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 12px;'>
                    🎨 Mood Distribution
                </h2>
                <p style='color: #475569; font-size: 15px; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
                    This chart visualizes the percentage breakdown of your emotional states during the selected period. 
                    Understanding your mood distribution helps identify patterns and emotional balance in your daily life.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Create pie chart with much smaller size
            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            colors = ['#10b981', '#3b82f6', '#ef4444', '#f59e0b', '#ec4899']
            mood_colors = {
                "Happy": '#10b981',
                "Neutral": '#3b82f6', 
                "Sad": '#ef4444',
                "Anxious": '#f59e0b',
                "Angry": '#ec4899'
            }
            
            pie_data = []
            pie_labels = []
            pie_colors = []
            for mood in mood_list:
                if mood in mood_counts and mood_counts[mood] > 0:
                    pie_data.append(mood_counts[mood])
                    pie_labels.append(mood)
                    pie_colors.append(mood_colors.get(mood, '#3b82f6'))
            
            if pie_data:
                wedges, texts, autotexts = ax2.pie(
                    pie_data, 
                    labels=pie_labels, 
                    colors=pie_colors,
                    autopct='%1.1f%%',
                    startangle=90,
                    textprops={'fontsize': 10, 'weight': 'bold'}
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(10)
                    autotext.set_weight('bold')
                
                ax2.set_title(f"Emotional Balance – {range_option}", fontsize=12, fontweight='bold', pad=12)
                fig2.patch.set_facecolor('white')
                
                st.pyplot(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

            # ================= CHAT-BASED TREND =================
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Spacing
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

                st.markdown("<div class='chart-wrapper' style='margin-top: 30px;'>", unsafe_allow_html=True)
                
                # Centered heading with larger size
                st.markdown("""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <h2 style='font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 12px;'>
                        💬 Chat Activity Insights
                    </h2>
                    <p style='color: #475569; font-size: 15px; line-height: 1.7; max-width: 750px; margin: 0 auto;'>
                        This analysis correlates your daily chat activity with stress-related keywords detected in your messages. 
                        The <span style='color: #10b981; font-weight: 600;'>green line</span> shows message volume, while the 
                        <span style='color: #ef4444; font-weight: 600;'>red line</span> indicates stress indicators, helping you identify 
                        patterns between communication frequency and emotional distress.
                    </p>
                </div>
                """, unsafe_allow_html=True)

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
                st.markdown("""
                <div style='text-align: center; padding: 40px 20px;'>
                    <p style='font-size: 16px; color: #64748b; font-weight: 500;'>
                        📭 No chat history found for the selected time range.
                    </p>
                    <p style='font-size: 14px; color: #94a3b8; margin-top: 10px;'>
                        Start chatting with the AI to see your activity insights here.
                    </p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("📊 Need more mood entries to show trend analysis. Keep logging your mood daily!")
    else:
        st.info("🌸 Start logging your moods to see beautiful analytics and insights about your emotional wellness journey!")