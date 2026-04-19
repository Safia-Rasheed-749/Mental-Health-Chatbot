import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods

def show_mood_analytics(user_id):
    # ---------------- HIDE DEFAULT UI (BUT NOT HEADER!) ----------------
    st.markdown("""
        <style>
        /* Hide only the hamburger menu (top-right) */
        #MainMenu {visibility: hidden;}
        
        /* Hide the footer */
        footer {visibility: hidden;}
        
        /* DO NOT hide header - it contains the sidebar collapse button! */
        /* header {visibility: hidden;}  ← REMOVED THIS LINE */
        
        /* Optional: Make header transparent but keep functionality */
        header {
            background: transparent !important;
            backdrop-filter: blur(0px) !important;
            box-shadow: none !important;
        }

        /* Gradient Log Mood button */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #4facfe, #00f2fe) !important;
            color: white !important;
            font-weight: 700;
            border-radius: 12px;
            height: 50px;
            width: 100%;
        }

        div.stButton > button:hover {
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📈 Mood Tracker")

    # ---------------- Mood Input ----------------
    st.markdown("### How are you feeling today?")
    mood = st.radio(
        "",
        ["😄 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"],
        index=1,
        horizontal=True
    )

    # Log Mood Button
    if st.button("Log Mood", key="log_mood"):
        # Strip emoji when saving to DB
        mood_text = mood.split(" ", 1)[1]
        add_mood(user_id, mood_text)
        st.success(f"✅ Your mood '{mood_text}' has been logged successfully!")

    # ---------------- Mood Overview ----------------
    moods = get_moods(user_id)

    if moods:
        # Count each mood
        mood_counts = {m: moods.count(m) for m in ["Happy", "Neutral", "Sad", "Anxious", "Angry"] if moods.count(m) > 0}

        if mood_counts:
            st.markdown("### Mood Overview")
            fig, ax = plt.subplots(figsize=(6, 4))

            # Modern colored bar chart
            colors = {
                "Happy": "#ffd700",      # gold
                "Neutral": "#90a4ae",    # greyish
                "Sad": "#2196f3",        # blue
                "Anxious": "#ff9800",    # orange
                "Angry": "#f44336"       # red
            }
            bar_colors = [colors[m] for m in mood_counts.keys()]

            ax.bar(mood_counts.keys(), mood_counts.values(), color=bar_colors, edgecolor='black')
            ax.set_ylabel("Count")
            ax.set_title("Mood Analytics")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Add counts on top of bars
            for i, v in enumerate(mood_counts.values()):
                ax.text(i, v + 0.1, str(v), ha='center', fontweight='bold')

            st.pyplot(fig)
    else:
        st.info("No moods logged yet. Log your mood above to see the analytics.")