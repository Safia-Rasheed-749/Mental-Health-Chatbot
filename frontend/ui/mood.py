# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go
from db import add_mood, get_moods, log_user_activity
from datetime import datetime, timedelta, date
from db import get_all_user_messages

MOOD_COLORS = {
    "Happy": "#4FD1C5", "Neutral": "#63B3ED", "Sad": "#7F9CF5",
    "Anxious": "#F6AD55", "Angry": "#FC8181",
}


def _chart_layout(fig, height=330):
    fig.update_layout(
        height=height, margin=dict(l=12, r=12, t=24, b=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#475569", size=12),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font_size=12),
    )
    return fig

def show_mood_analytics(user_id):

    # ================= ENHANCED CSS (CHAT-STYLE) =================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ΓöÇΓöÇ HIDE CLUTTER ΓöÇΓöÇ */
    .stDeployButton { display: none !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu       { visibility: hidden !important; }
    footer          { visibility: hidden !important; }
    header {
        background: transparent !important;
        box-shadow: none !important;
        visibility: visible !important;
    }

    /* ΓöÇΓöÇ PAGE BACKGROUND (SAME AS CHAT) ΓöÇΓöÇ */
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 45%, #F5F3FF 100%) !important;
        height: 100%;
    }

    /* ΓöÇΓöÇ Sidebar styling is handled exclusively in sidebar.py ΓöÇΓöÇ */

    /* ΓöÇΓöÇ BLOCK CONTAINER ΓöÇΓöÇ */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }

    /* ΓöÇΓöÇ HEADER BANNER (SAME AS CHAT) ΓöÇΓöÇ */
    .page-header {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(91,141,239,0.28);
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
    /* Mood Analytics */
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
     /* Quick Mood Log , Mood Trend Timeline*/
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ΓöÇΓöÇ MOOD RADIO BUTTONS ΓöÇΓöÇ */
    .main div[role="radiogroup"] {
        justify-content: center !important;
        gap: 12px !important;
        margin: 16px 0 !important;
        flex-wrap: wrap !important;
    }

    div[data-testid="stRadio"] input[id*="mood_radio"] + div {
     background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95)) !important;
    padding: 12px 24px !important;
    # Not applying
    border-radius: 16px !important;
    border: 2px solid rgba(99,102,241,0.20) !important;
}
      /* Radio buttons label color Happy etc */
    .mood-radio-wrapper div[data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 500 !important;
        color: black !important;
        margin: 0 !important;
    }
      /* On hover, radio button styling , also change in sidebar */
     div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background: rgba(99,102,241,0.08) !important;
    border-color: #6366f1 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.20) !important;
    transform: translateY(-2px);
}

    .main div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border-color: #6366f1 !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
    }

.st-key-log_mood_btn button {
    background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%) !important;
    background-color: #5B8DEF !important;
   color: white !important;
    border: none !important;
    outline: none !important;
   border-radius: 12px !important;
    height: 48px !important;
    padding: 0 26px !important;
   box-shadow: 0 4px 16px rgba(91,141,239,0.30) !important;
   transition: all 0.2s ease !important;
   opacity: 1 !important;
}
/*log mood background color changes*/
/* FORCE INNER BUTTON LAYER */
.st-key-log_mood_btn button[kind="secondary"] {
    background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%) !important;
    background-color: #5B8DEF !important;
    margin-top: 24px !important;
    margin-bottom: 24px !important;
    padding-left:20px;
    justify-content: center;
}

/* TEXT */
.st-key-log_mood_btn button p {
    color: white !important;
    font-size: 17px !important;
    font-weight: 700 !important;
}

/* HOVER */
.st-key-log_mood_btn button:hover {
    background: linear-gradient(135deg, #4F83E3 0%, #6D8EF0 100%) !important;
    background-color: #4F83E3 !important;

    transform: translateY(-2px) !important;

    box-shadow: 0 6px 22px rgba(91,141,239,0.40) !important;
}
/* Select Time Range label */
div[data-testid="stSelectbox"] label p {
    font-size: 17px !important;
    color: black !important;
    font-weight: 500 !important;
}

/* SELECTBOX MAIN */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: white !important;
    border: 2px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    color: black !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
    border-color: #6366f1 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.15) !important;
}

/* dropdown menu */
div[data-baseweb="popover"] {
    background: #fbcfe8 !important;
    border-radius: 12px !important;
    border: 1px solid #f9a8d4 !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}

ul[role="listbox"] {
    background: white !important;
    padding: 6px !important;
    border-radius: 12px !important;
}

li[role="option"] {
    background: white !important;
    color: #111827 !important;
    margin-bottom: 4px !important;
    border-radius: 8px !important;
}

li[role="option"]:hover {
    background: #6366f1 !important;
    color: white !important;
}

li[aria-selected="true"] {
    background: #6366f1 !important;
    color: white !important;
}

    # li {
    #     color: white !important;
    # }
    /* ΓöÇΓöÇ INSIGHT CARD ΓöÇΓöÇ */
    .insight-card {
        background: linear-gradient(135deg, rgba(139,92,246,0.10), rgba(99,102,241,0.10));
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

    /* ΓöÇΓöÇ STATS CARDS ΓöÇΓöÇ */
    .stats-wrapper {
        display: flex;
        gap: 16px;
        margin: 24px 0;
        flex-wrap: wrap;
    }
    /* Total Entries etc Cards Styling) */
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
        /* 1st stat card's bottom border */
    .stat-card:nth-child(1) {
        border-bottom: 3px solid #10b981;
    }
        /* 2nd card's bottom border */
    .stat-card:nth-child(2) {
        border-bottom: 3px solid #6366f1;
    }
         /* 3rd card's bottom border */
    .stat-card:nth-child(3) {
        border-bottom: 3px solid #ec4899;
    }
    /* Value of Total Entries etc */
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



    /* ΓöÇΓöÇ INFO/SUCCESS MESSAGES ΓöÇΓöÇ */
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

    /* ΓöÇΓöÇ DIVIDER ΓöÇΓöÇ */
    hr {
        margin: 24px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.30), transparent) !important;
    }

    /* ΓöÇΓöÇ SCROLLBAR ΓöÇΓöÇ */
    ::-webkit-scrollbar       { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }
    </style>
    """, unsafe_allow_html=True)

    # Header banner
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
    st.markdown('<div class="mood-radio-wrapper">', unsafe_allow_html=True)

    mood = st.radio(
        "Select Mood",
        ["😊 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        horizontal=True,
        key="mood_radio",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    # Centralized Log Button (no empty columns)


    if st.button(" Log My Mood", key="log_mood_btn"):

        mood_text = mood.split(" ", 1)[1]
        add_mood(user_id, mood_text)
        log_user_activity(
            user_id,
            "Log Mood",
            "Mood Tracker",
            f"Mood: {mood_text}"
        )
        st.toast(f"Mood '{mood_text}' logged successfully!", icon="✅")


    st.markdown('</div>', unsafe_allow_html=True)  # Close mood-section-card

    moods = get_moods(user_id)
    mood_list = ["Happy", "Neutral", "Sad", "Anxious", "Angry"]

    if moods:
        # ================= FILTER SECTION (ONLY SHOW IF MOODS EXIST) =================
        st.markdown('<div class="mood-section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Mood Trend Timeline</div>', unsafe_allow_html=True)

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
            <b>💡 Emotional Insight</b><br><br>
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

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        # ================= MOOD TREND + DISTRIBUTION =================
        trend_col, distribution_col = st.columns(2, gap="large")
        with trend_col:
            st.markdown("### 📈 Mood Trend Timeline")
            st.caption(f"Your logged moods across {range_option.lower()}.")
            if len(filtered) > 1:
                y_map = {"Angry": 1, "Anxious": 2, "Sad": 3, "Neutral": 4, "Happy": 5}
                day_labels = [f"Day {i}" for i in range(1, len(filtered) + 1)]
                fig = go.Figure(go.Scatter(x=day_labels, y=[y_map[m] for m in filtered], mode="lines+markers", line=dict(color="#7F9CF5", width=3, shape="spline", smoothing=0.8), marker=dict(size=8, color=[MOOD_COLORS[m] for m in filtered], line=dict(color="white", width=2)), fill="tozeroy", fillcolor="rgba(127,156,245,0.12)", text=filtered, hovertemplate="%{x}: %{text}<extra></extra>"))
                fig.update_xaxes(title=None, type="category", tickangle=0, showgrid=False, zeroline=False, showline=False)
                fig.update_yaxes(title=None, tickmode="array", tickvals=[1,2,3,4,5], ticktext=["Angry","Anxious","Sad","Neutral","Happy"], range=[0.5,5.5], showgrid=True, gridcolor="rgba(148,163,184,0.16)", zeroline=False)
                st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Log another mood to see your trend over time.")
        with distribution_col:
            st.markdown("### 🎨 Mood Distribution")
            st.caption(f"Emotional balance for {range_option.lower()}.")
            pie_labels = [m for m in mood_list if mood_counts.get(m, 0) > 0]
            fig = go.Figure(go.Pie(labels=pie_labels, values=[mood_counts[m] for m in pie_labels], hole=0.62, sort=False, marker_colors=[MOOD_COLORS[m] for m in pie_labels], textinfo="label+percent", textposition="outside", hovertemplate="%{label}: %{value} logs (%{percent})<extra></extra>"))
            fig.update_layout(annotations=[dict(text=f"{total}<br><span style='font-size:12px'>Logs</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=22, color="#1E293B"))], showlegend=False)
            st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})

        # ================= CHAT-BASED TREND =================
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)  # Spacing
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

            st.markdown("<div class='chart-wrapper' style='margin-top: 30px; margin -bottom: 25px;'>", unsafe_allow_html=True)

            # Centered heading with larger size
            st.markdown("""
            <div style='text-align: center; margin-bottom: 25px; margin-bottom: 25px;'>
                <h2 style='font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 12px;'>
                    💬 Chat Activity Insights
                </h2>
                <p style='color: #475569; font-size: 18px; line-height: 1.7; max-width: 700px; margin: 0 auto; margin-bottom: 25px;'>
                    This analysis correlates your daily chat activity with stress-related keywords detected in your messages.
                    The <span style='color: #10b981; font-weight: 600;'>green line</span> shows message volume, while the
                    <span style='color: #ef4444; font-weight: 600;'>red line</span> indicates stress indicators, helping you identify
                    patterns between communication frequency and emotional distress.
                </p>
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=days_sorted, y=counts, mode="lines+markers", name="Messages per day", line=dict(color=MOOD_COLORS["Happy"], width=3, shape="spline"), fill="tozeroy", fillcolor="rgba(79,209,197,0.12)"))
            fig.add_trace(go.Scatter(x=days_sorted, y=stress, mode="lines+markers", name="Stress indicators", line=dict(color=MOOD_COLORS["Angry"], width=2, shape="spline")))
            fig.update_xaxes(title=None, tickangle=0, showgrid=False, zeroline=False, showline=False)
            fig.update_yaxes(title="Messages / indicators", showgrid=True, gridcolor="rgba(148,163,184,0.16)", zeroline=False)
            fig.update_layout(title="Chat Activity & Stress Indicators", legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1), margin=dict(l=12, r=12, t=72, b=12))
            st.plotly_chart(_chart_layout(fig, height=360), use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 40px 20px;'>
                <p style='font-size: 16px; color: #64748b; font-weight: 500;'>
                    📭 No chat history found for the selected time range.
                </p>
                <p style='font-size: 17px; color: #94a3b8; margin-top: 17px; margiun-bottom; 25px;'>
                    Start chatting with the AI to see your activity insights here.
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("🌸 Start logging your moods to see beautiful analytics and insights about your emotional wellness journey!")
