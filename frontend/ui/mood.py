import streamlit as st
import matplotlib.pyplot as plt
from db import add_mood, get_moods

def show_mood_analytics(user_id):
    # ---------------- Remove top white space (keeps header & sidebar) ----------------
    st.markdown("""
        <style>
        /* Remove default top padding/margin from main content */
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: -0.5rem !important;
        }
        .main .block-container > :first-child {
            margin-top: 0rem !important;
        }

        /* Hide only the hamburger menu (top-right) */
        #MainMenu {visibility: hidden;}
        
        /* Hide the footer */
        footer {visibility: hidden;}
        
        /* Make header transparent but keep functionality */
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
            # --- Minimized, professional graph size ---
            fig, ax = plt.subplots(figsize=(3.2, 2.0), dpi=100)

            colors = {
                "Happy": "#ffd700",
                "Neutral": "#90a4ae",
                "Sad": "#2196f3",
                "Anxious": "#ff9800",
                "Angry": "#f44336"
            }
            bar_colors = [colors[m] for m in mood_counts.keys()]

            bars = ax.bar(mood_counts.keys(), mood_counts.values(),
                          color=bar_colors, edgecolor='black', linewidth=0.5, width=0.6)
            ax.set_ylabel("Count", fontsize=7)
            ax.set_title("Mood Analytics", fontsize=8, fontweight='medium')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', labelsize=6)

            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{int(height)}',
                        ha='center', va='bottom', fontsize=6, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig, use_container_width=False)
    else:
        st.info("No moods logged yet. Log your mood above to see the analytics.")