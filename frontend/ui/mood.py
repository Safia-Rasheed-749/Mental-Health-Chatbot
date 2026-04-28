import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods

def show_mood_analytics(user_id):

    # ================= CSS =================
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
    }

    .mood-title {
        text-align: center;
        font-size: 34px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 30px;
    }

    .center-text {
        text-align: center;
    }

    div[role="radiogroup"] {
        justify-content: center !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 2px solid #000 !important;
        border-radius: 8px !important;
    }

    .insight-card {
        background: linear-gradient(135deg, #e0f7f4, #ede9fe);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 18px;
        margin: 40px 0;
    }

    .stats-wrapper {
        display: flex;
        gap: 16px;
        margin-bottom: 40px;
    }

    .stat-card {
        flex: 1;
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 22px rgba(0,0,0,0.07);
    }

    .stat-card:nth-child(1) { background: #c8eae6; }
    .stat-card:nth-child(2) { background: #d8c8f8; }
    .stat-card:nth-child(3) { background: #f0c8d4; }

    .stat-value { font-size: 20px; font-weight: 700; }
    .stat-label { font-size: 12px; color: #64748b; }

    div[data-testid="stButton"] button {
        background: #1e3a8a !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        height: 48px !important;
        padding: 0 24px !important;
        margin: 15px auto !important;
        display: block !important;
        padding-right: 200px;
    }

    .timeline-wrapper {
        background: #f8fafc;
        padding: 20px;
        border-radius: 18px;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown("<h1 class='mood-title'>📈 Mood Tracker</h1>", unsafe_allow_html=True)

    # ================= QUICK MOOD LOG (FIXED) =================
    st.markdown('<h3 class="center-text">😊 Quick Mood Log</h3>', unsafe_allow_html=True)

    mood = st.radio(
        "Select your mood",
        ["😄 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        horizontal=True,
        key="mood_radio"
    )

    if st.button("Log Mood"):
        mood_text = mood.split(" ", 1)[1]
        add_mood(user_id, mood_text)
        st.success(f"Mood '{mood_text}' logged!")
        st.rerun()

    # ================= FILTER =================
    st.markdown("### 📅 Mood Trend Timeline")

    range_option = st.selectbox(
        "Select time range",
        ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"]
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

    # ================= ANALYTICS =================
    if filtered:

        mood_counts = {m: filtered.count(m) for m in mood_list if m in filtered}
        total = len(filtered)
        most_common = max(mood_counts, key=mood_counts.get)
        variety = len(set(filtered))

        st.markdown(f"""
        <div class='insight-card'>
            <b>🌿 Mood Insight</b><br><br>
            Your emotional trend is being analyzed across time.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='stats-wrapper'>
            <div class='stat-card'>
                <div class='stat-value'>{total}</div>
                <div class='stat-label'>Entries</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>{most_common}</div>
                <div class='stat-label'>Most Frequent</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>{variety}</div>
                <div class='stat-label'>Variety</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ================= GRAPH =================
        if len(filtered) > 1:
            st.markdown("<div class='timeline-wrapper'>", unsafe_allow_html=True)

            y_map = {"Happy": 5, "Neutral": 3, "Sad": 2, "Anxious": 1, "Angry": 0}
            x = list(range(len(filtered)))
            y = [y_map[m] for m in filtered]

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(x, y, marker='o', linewidth=2)

            ax.set_yticks([0,1,2,3,5])
            ax.set_yticklabels(["Angry","Anxious","Sad","Neutral","Happy"])

            ax.set_xticks(x)
            ax.set_xticklabels([f"Day {i+1}" for i in x], rotation=45)

            ax.set_title(f"Mood Trend – {range_option}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Mood")

            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.info("Only one mood entry so far.")

    else:
        st.info("Start logging moods to see analytics.")