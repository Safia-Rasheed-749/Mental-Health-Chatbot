# mood.py
import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods

def show_mood_analytics(user_id):
    st.title("📈 Mood Tracker")

    # ---------------- Mood Input ----------------
    st.markdown("### How are you feeling today?")
    mood = st.radio(
        "",
        ["Happy", "Neutral", "Sad", "Anxious", "Angry"],
        index=1,
        horizontal=True
    )

    # Log Mood Button
    if st.button("Log Mood", key="log_mood"):
        add_mood(user_id, mood)
        st.success(f"✅ Your mood '{mood}' has been logged successfully!")

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