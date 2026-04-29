import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods
from layout_utils import apply_professional_design_system
from datetime import datetime, timedelta, date
from db import get_all_user_messages

def show_mood_analytics(user_id):
    apply_professional_design_system()

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
        color: rgba(15,23,42,0.92);
        margin-bottom: 30px;
    }

    .center-text {
        text-align: center;
    }

    div[role="radiogroup"] {
        justify-content: center !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 1.5px solid rgba(15,23,42,0.14) !important;
        border-radius: 8px !important;
        background: #ffffff !important;
    }

    .insight-card {
        background: linear-gradient(135deg, rgba(59,130,246,0.10), rgba(124,58,237,0.10));
        border-left: 5px solid #8b5cf6;
        padding: 20px;
        border-radius: 18px;
        margin: 40px 0;
        color: rgba(15,23,42,0.82);
        border-top: 1px solid rgba(15,23,42,0.10);
        border-right: 1px solid rgba(15,23,42,0.10);
        border-bottom: 1px solid rgba(15,23,42,0.10);
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
        box-shadow: 0 18px 55px rgba(15,23,42,0.08);
        border: 1px solid rgba(15,23,42,0.10);
    }

    .stat-card:nth-child(1) { background: linear-gradient(145deg, rgba(16,185,129,0.22), rgba(59,130,246,0.14)); }
    .stat-card:nth-child(2) { background: linear-gradient(145deg, rgba(124,58,237,0.22), rgba(59,130,246,0.14)); }
    .stat-card:nth-child(3) { background: linear-gradient(145deg, rgba(236,72,153,0.18), rgba(124,58,237,0.14)); }

    .stat-value { font-size: 20px; font-weight: 800; color: rgba(15,23,42,0.92); }
    .stat-label { font-size: 12px; color: rgba(15,23,42,0.62); }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, rgba(59,130,246,0.92), rgba(124,58,237,0.92)) !important;
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
        background: rgba(255,255,255,0.92);
        padding: 20px;
        border-radius: 18px;
        margin-top: 40px;
        border: 1px solid rgba(15,23,42,0.10);
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

            # ================= CHAT-BASED TREND (History link) =================
            # Build a simple daily trendline from previous chats (volume + stress keywords)
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
                        # best-effort parsing for string timestamps
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

                fig2, ax2 = plt.subplots(figsize=(7, 3))
                ax2.plot(x2, counts, marker='o', linewidth=2, label="Messages/day")
                ax2.plot(x2, stress, marker='o', linewidth=2, label="Stress keyword score")
                ax2.set_title("Chat Activity Trend (from History)")
                ax2.set_xlabel("Date")
                ax2.set_ylabel("Count / Score")
                ax2.set_xticks(x2)
                ax2.set_xticklabels([d.strftime("%b %d") for d in days_sorted], rotation=45, ha="right")
                ax2.grid(alpha=0.15)
                ax2.legend()
                st.pyplot(fig2)
            else:
                st.info("No chat history found for the selected range yet.")

        else:
            st.info("Only one mood entry so far.")

    else:
        st.info("Start logging moods to see analytics.")