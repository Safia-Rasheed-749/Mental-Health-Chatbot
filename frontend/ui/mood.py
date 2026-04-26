import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods
from layout_utils import apply_clean_layout


def show_mood_analytics(user_id):
    apply_clean_layout(hide_header_completely=False)

    # ---------------- CSS ----------------
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
        padding-bottom: 1rem !important;
    }

    /* 🌟 TITLE */
    .mood-title {
        text-align: center;
        font-size: 34px;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }

    /* 📏 SPACING */
    .space-sm { height: 10px; }
    .space-md { height: 18px; }
    .space-lg { height: 28px; }

    /* 🌿 INSIGHT CARD */
    .insight-card {
        background: linear-gradient(135deg, #e0f7f4, #ede9fe);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        margin-bottom: 8px;   /* 🔥 FIX: reduced gap below */
    }

    /* 💎 FLOATING CARDS */
    .stats-wrapper {
        display: flex;
        gap: 16px;
        margin-top: 10px;
    }

    .stat-card {
        flex: 1;
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 22px rgba(0,0,0,0.07);
        transition: 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
    }

    .stat-card:nth-child(1) { background: #e0f7f4; }
    .stat-card:nth-child(2) { background: #ede9fe; }
    .stat-card:nth-child(3) { background: #ffe4ec; }

    .stat-value {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
    }

    .stat-label {
        font-size: 12px;
        color: #64748b;
    }

    /* 📊 TIMELINE */
    .timeline-wrapper {
        background: #f8fafc;
        padding: 16px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        margin-top: 18px;
    }

    /* 🔘 BUTTON */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4facfe, #00f2fe) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        height: 50px;
        width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.markdown("<h1 class='mood-title'>📈 Mood Tracker</h1>", unsafe_allow_html=True)

    st.markdown("<div class='space-lg'></div>", unsafe_allow_html=True)

    # ---------------- DATA ----------------
    moods = get_moods(user_id)
    mood_list = ["Happy", "Neutral", "Sad", "Anxious", "Angry"]

    # ---------------- FILTER ----------------
    st.markdown("### 📅 Mood Trend Timeline")

    range_option = st.selectbox(
        "Select time range",
        ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"],
        index=0
    )

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
    last7 = filtered[-7:] if filtered else []

    # ---------------- INSIGHT ----------------
    if filtered:
        st.markdown(f"""
        <div class='insight-card'>
            <b>🌿 Mood Insight</b><br><br>
            Your emotional trend is being analyzed across time.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='space-sm'></div>", unsafe_allow_html=True)

    # ---------------- STATS (FLOATING CARDS) ----------------
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

    # ---------------- MOOD LOG SECTION (NEW + ABOVE GRAPH) ----------------
    st.markdown("<div class='space-lg'></div>", unsafe_allow_html=True)

    st.markdown("### 😊 Quick Mood Log")

    mood = st.radio(
        "Select your mood",
        ["😄 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        horizontal=True
    )

    if st.button("Log Mood"):
        mood_text = mood.split(" ", 1)[1]
        add_mood(user_id, mood_text)
        st.success(f"Mood '{mood_text}' logged!")

    # ---------------- TIMELINE ----------------
    st.markdown("<div class='space-lg'></div>", unsafe_allow_html=True)

    if filtered:
        st.markdown("<div class='timeline-wrapper'>", unsafe_allow_html=True)

        st.markdown("### 📈 Mood Trend")

        fig, ax = plt.subplots(figsize=(4.5, 2.0), dpi=100)

        y_map = {
            "Happy": 5,
            "Neutral": 3,
            "Sad": 2,
            "Anxious": 1,
            "Angry": 0
        }

        x = list(range(len(last7)))
        y = [y_map[m] for m in last7]

        ax.plot(x, y, marker='o', linewidth=2, color="#6366f1")

        ax.set_yticks([0,1,2,3,5])
        ax.set_yticklabels(["Angry","Anxious","Sad","Neutral","Happy"])

        ax.set_xticks(x)
        ax.set_xticklabels(["D"+str(i+1) for i in x], fontsize=8)

        ax.grid(True, alpha=0.25)
        ax.set_title("Mood Trend Over Time", fontsize=10)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Start logging moods to see analytics.")