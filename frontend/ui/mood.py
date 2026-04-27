import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods
from layout_utils import apply_clean_layout

def show_mood_analytics(user_id):
    # apply_clean_layout(hide_header_completely=False)
    # show_sidebar(user_id, "Mood Analytics")

    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {
        background: transparent !important;
        box-shadow: none !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Title */
    .mood-title {
        text-align: center;
        font-size: 34px;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 30px 0;
    }

    /* Black border ONLY around the selectbox (dropdown) */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
    }

    /* Spacing below the selectbox */
    .selectbox-spacing {
        margin-bottom: 40px;
    }

    /* Insight card */
    .insight-card {
        background: linear-gradient(135deg, #e0f7f4, #ede9fe);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        margin-bottom: 45px;
    }

    /* Stats wrapper */
    .stats-wrapper {
        display: flex;
        gap: 16px;
        margin: 10px 0 40px 0;
    }
    .stat-card {
        flex: 1;
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 22px rgba(0,0,0,0.07);
        transition: 0.2s ease;
    }
    .stat-card:hover { transform: translateY(-4px); }
    .stat-card:nth-child(1) { background: #c8eae6; }
    .stat-card:nth-child(2) { background: #d8c8f8; }
    .stat-card:nth-child(3) { background: #f0c8d4; }
    .stat-value { font-size: 20px; font-weight: 700; color: #0f172a; }
    .stat-label { font-size: 12px; color: #64748b; }

    /* Quick Mood Log container */
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 80%;
        margin: 20px auto 40px auto;
        background: #fafcff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    /* Center the heading inside the container */
    .center-container h3 {
        text-align: center !important;
        width: 100%;
    }
    /* Make radio buttons horizontal and centered */
    .center-container .stRadio label {
        font-size: 1.3rem !important;
        font-weight: 500;
    }
    .center-container .stRadio > div {
        display: flex !important;
        justify-content: center !important;
        gap: 32px !important;
        margin: 15px 0 25px 0 !important;
        flex-wrap: wrap;
    }
    /* Log Mood button - rectangular, centered, text on one line */
    div[data-testid="stButton"] button {
        background: #1e3a8a !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 8px !important;   /* less rounded, rectangular */
        height: 48px !important;
        width: auto !important;
        min-width: 150px !important;
        padding: 0 24px !important;
        margin: 15px auto 5px auto !important;
        display: inline-block !important;
        border: none !important;
        white-space: nowrap !important;   /* keep text on one line */
        transition: 0.2s !important;
    }
    div[data-testid="stButton"] button:hover {
        background: #2563eb !important;
        transform: scale(1.02);
    }

    /* Timeline graph wrapper */
    .timeline-wrapper {
        background: #f8fafc;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='mood-title'>📈 Mood Tracker</h1>", unsafe_allow_html=True)

    # Timeline header
    st.markdown("### 📅 Mood Trend Timeline")

    st.markdown('<div class="selectbox-spacing">', unsafe_allow_html=True)
    range_option = st.selectbox(
        "Select time range",
        ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"],
        index=0
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Data filtering
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

    mood_counts = {m: filtered.count(m) for m in mood_list if m in filtered}
    total = len(filtered)
    most_common = max(mood_counts, key=mood_counts.get) if mood_counts else "N/A"
    variety = len(set(filtered)) if filtered else 0

    if filtered:
        st.markdown(f"""
        <div class='insight-card'>
            <b>🌿 Mood Insight</b><br><br>
            Your emotional trend is being analyzed across time.
        </div>
        """, unsafe_allow_html=True)

    if filtered:
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

    # Quick Mood Log (centered heading, horizontal radio, rectangular button)
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown("### 😊 Quick Mood Log")   # this heading is now centered by CSS
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
    st.markdown('</div>', unsafe_allow_html=True)

    # Trend graph
    if filtered and len(filtered) > 1:
        st.markdown("<div class='timeline-wrapper'>", unsafe_allow_html=True)
        st.markdown("### 📈 Mood Trend Over Time")
        y_map = {"Happy": 5, "Neutral": 3, "Sad": 2, "Anxious": 1, "Angry": 0}
        x = list(range(len(filtered)))
        y = [y_map[m] for m in filtered]

        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.plot(x, y, marker='o', linewidth=2, color="#6366f1")
        ax.set_yticks([0,1,2,3,5])
        ax.set_yticklabels(["Angry","Anxious","Sad","Neutral","Happy"])
        if len(x) > 20:
            step = len(x) // 10
            xticks = x[::step]
            ax.set_xticks(xticks)
            ax.set_xticklabels([f"Day {i+1}" for i in xticks], rotation=45, ha='right', fontsize=8)
        else:
            ax.set_xticks(x)
            ax.set_xticklabels([f"Day {i+1}" for i in x], rotation=45, ha='right', fontsize=8)
        ax.grid(True, alpha=0.25)
        ax.set_title(f"Mood Trend – {range_option}", fontsize=10)
        ax.set_xlabel("Time")
        ax.set_ylabel("Mood")
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    elif filtered and len(filtered) == 1:
        st.info("Only one mood entry so far. Continue logging to see the trend.")
    else:
        st.info("Start logging moods to see analytics.")