import streamlit as st


EXERCISES = {
    "quick": [
        {
            "id": "reset",
            "icon": "✦",
            "title": "A one-minute reset",
            "duration": "1 minute",
            "summary": "A gentle reset for moments when everything feels like too much.",
            "why": "Slowing down your exhale can help your body shift toward a calmer state.",
            "steps": [
                "Let your shoulders drop and rest your feet on the floor.",
                "Breathe in comfortably through your nose.",
                "Exhale slowly, making the out-breath a little longer.",
                "Repeat at your own pace. Stop if anything feels uncomfortable.",
            ],
        },
        {
            "id": "orient",
            "icon": "◎",
            "title": "Pause and orient",
            "duration": "2 minutes",
            "summary": "A simple way to reconnect with the room around you during a stressful moment.",
            "why": "Noticing neutral details can offer your attention a steady place to land.",
            "steps": [
                "Place both feet on the ground and look around slowly.",
                "Name where you are and the date, if you know it.",
                "Notice one thing that tells you that you are here, right now.",
            ],
        },
    ],
    "breathing": [
        {
            "id": "box-breathing",
            "icon": "◌",
            "title": "Box breathing",
            "duration": "2 minutes",
            "summary": "A steady, even rhythm with an inhale, hold, exhale, and pause.",
            "why": "A predictable rhythm can provide a useful focus when your thoughts feel busy.",
            "steps": [
                "Inhale gently for 4 counts.",
                "Pause comfortably for 4 counts.",
                "Exhale gently for 4 counts.",
                "Pause for 4 counts, then repeat. Keep the breath comfortable.",
            ],
        },
        {
            "id": "478-breathing",
            "icon": "◍",
            "title": "4–7–8 breathing",
            "duration": "2 minutes",
            "summary": "A slow breathing pattern to explore when you have a quiet moment.",
            "why": "Counting can anchor attention to a gentle breathing pace.",
            "steps": [
                "Breathe in gently for 4 counts.",
                "Pause for up to 7 counts only if that feels comfortable.",
                "Breathe out slowly for 8 counts, without straining.",
                "Return to normal breathing if you feel light-headed or uncomfortable.",
            ],
        },
    ],
    "mindfulness": [
        {
            "id": "mindful-moment",
            "icon": "✧",
            "title": "Mindful moment",
            "duration": "2 minutes",
            "summary": "Practice noticing what is here without needing to change it.",
            "why": "Brief moments of mindful attention can help create space around busy thoughts.",
            "steps": [
                "Find a position that feels comfortable and supported.",
                "Notice the feeling of your breath, or the contact of your feet with the floor.",
                "When your attention wanders, gently bring it back.",
                "Close by noticing one thing you need in this moment.",
            ],
        },
        {
            "id": "body-scan",
            "icon": "◉",
            "title": "Gentle body scan",
            "duration": "2 minutes",
            "summary": "Move your attention through the body with curiosity, not judgment.",
            "why": "Noticing physical sensations can support awareness of tension and comfort.",
            "steps": [
                "Notice your feet, then your legs, without trying to change anything.",
                "Bring attention to your hands, shoulders, and jaw.",
                "If you find tension, see if a small release feels welcome.",
                "Finish by taking one comfortable breath.",
            ],
        },
    ],
    "grounding": [
        {
            "id": "54321",
            "icon": "⊙",
            "title": "5–4–3–2–1 grounding",
            "duration": "2 minutes",
            "summary": "Use your senses to notice the present environment, one detail at a time.",
            "why": "A sensory check-in can help redirect attention to what is around you.",
            "steps": [
                "Name 5 things you can see.",
                "Notice 4 things you can feel, such as your feet or clothing.",
                "Listen for 3 things you can hear.",
                "Notice 2 things you can smell and 1 thing you can taste.",
            ],
        },
        {
            "id": "steady-object",
            "icon": "◇",
            "title": "Steady object practice",
            "duration": "2 minutes",
            "summary": "Choose an everyday object and explore its details with your attention.",
            "why": "A nearby object can give your mind a calm, concrete point of focus.",
            "steps": [
                "Choose an object within reach that feels neutral or pleasant.",
                "Notice its color, shape, edges, and texture.",
                "Observe how the light falls on it and how it feels in your hand.",
            ],
        },
    ],
}

CATEGORIES = [
    ("quick", "⚡ Quick Relief"),
    ("breathing", "🌬️ Breathing & Pacing"),
    ("mindfulness", "🧘 Mindfulness & Meditation"),
    ("grounding", "🌿 Grounding Techniques"),
]


def _render_exercise(exercise: dict):
    with st.container(key=f"exercise_card_{exercise['id']}"):
        st.markdown(
            f"""
            <div class="card-heading">
              <span class="icon-badge" aria-hidden="true">{exercise['icon']}</span>
              <div><div class="eyebrow">GUIDED PRACTICE · {exercise['duration'].upper()}</div>
                <h3>{exercise['title']}</h3></div>
            </div>
            <p class="summary">{exercise['summary']}</p>
            <p class="why"><strong>Why it may help</strong> · {exercise['why']}</p>
            <div class="steps-label">YOUR PRACTICE</div>
            """,
            unsafe_allow_html=True,
        )
        if exercise["id"] in {"mindful-moment", "body-scan", "54321", "steady-object"}:
            selections = [
                st.checkbox(step, key=f"check_{exercise['id']}_{index}")
                for index, step in enumerate(exercise["steps"])
            ]
            completed = sum(selections)
            st.progress(completed / len(selections), text=f"{completed} of {len(selections)} steps")
            if completed == len(selections):
                st.success("Practice complete. Take a moment to notice how you feel.")
        else:
            for index, step in enumerate(exercise["steps"], 1):
                st.markdown(
                    f'<div class="step-pill"><span>{index}</span>{step}</div>',
                    unsafe_allow_html=True,
                )


def show_exercises_page():
    st.markdown(
        """
        <style>
          header,[data-testid="stHeader"],footer{display:none!important}
          .main .block-container{max-width:1120px;padding:1.25rem 2rem 3rem}
          .stApp{background:linear-gradient(180deg,#F8FAFC 0%,#F5F3FF 100%);color:#1E293B}
          .exercise-header{text-align:center;margin:0 auto 1.5rem;max-width:780px}
          .exercise-header h1{color:#1E1B4B;font-size:clamp(2rem,4vw,2.7rem);letter-spacing:-.035em;margin:0 0 .65rem;font-weight:750}
          .exercise-header p{color:#64748B;font-size:1.05rem;line-height:1.65;margin:0}
          [data-testid="stTabs"] [data-testid="stTab"]{color:#64748B;font-weight:600}
          [data-testid="stTabs"] [aria-selected="true"]{color:#4F46E5}
          [data-testid="stTabs"] [data-baseweb="tab-highlight"]{background:#6366F1}
          [class*="st-key-exercise_card_"]{background:#fff;border:1px solid #EEF2FF;border-radius:20px;padding:24px;box-shadow:0 4px 20px rgba(99,102,241,.06);margin:12px 0 14px;width:100%;}
          .card-heading{display:flex;align-items:center;gap:14px}
          .icon-badge{display:grid;place-items:center;flex:0 0 48px;height:48px;border-radius:16px;background:#EEF2FF;color:#6366F1;font-size:25px;font-weight:600}
          .eyebrow{font-size:10px;font-weight:750;letter-spacing:.12em;color:#818CF8;margin-bottom:4px}
          [class*="st-key-exercise_card_"] h3{font-size:1.2rem;line-height:1.3;color:#1E1B4B;margin:0;font-weight:700}
          .summary{color:#475569;line-height:1.6;margin:16px 0 10px;font-size:14px}
          .why{color:#64748B;background:#F8FAFF;border:1px solid #EEF2FF;padding:11px 13px;border-radius:12px;font-size:13px;line-height:1.55;margin:0 0 16px}
          .why strong{color:#4F46E5}
          .steps-label{font-size:10px;letter-spacing:.12em;font-weight:750;color:#94A3B8;margin:0 0 8px}
          .exercise-steps{list-style:none;margin:0;padding:0;display:grid;gap:8px}
          .exercise-steps li{display:flex;align-items:flex-start;gap:10px;color:#334155;font-size:13px;line-height:1.5}
          .exercise-steps li span{display:grid;place-items:center;flex:0 0 22px;height:22px;border-radius:50%;background:#EEF2FF;color:#4F46E5;font-size:11px;font-weight:700}
          .step-pill{display:flex;align-items:flex-start;gap:12px;background:#F5F3FF;color:#4F46E5;padding:12px 16px;border-radius:12px;font-weight:600;margin:8px 0;border-left:4px solid #6366F1;line-height:1.5;font-size:13px}
          .step-pill span{display:grid;place-items:center;flex:0 0 22px;height:22px;border-radius:50%;background:#E0E7FF;color:#4F46E5;font-size:11px}
          .stButton>button{border-radius:12px;min-height:44px;font-weight:650;transition:all .18s ease}
          .stButton>button:hover{transform:translateY(-1px);box-shadow:0 7px 18px rgba(99,102,241,.16)}
          .pro-tips-container{background:linear-gradient(135deg,#EEF2FF 0%,#F5F3FF 100%);border:1px solid #E0E7FF;border-radius:20px;padding:26px;margin-top:36px;color:#1E1B4B}
          .pro-tips-container h3{text-align:center;color:#312E81;margin:0 0 18px;font-size:1.2rem}
          .tips-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
          .tip-card{text-align:center;padding:15px;border-radius:14px;background:rgba(255,255,255,.65);color:#4338CA;font-size:13px;line-height:1.5}
          .tip-card strong{display:block;color:#312E81;margin-bottom:4px}
          [data-testid="stDialog"]>div{border:1px solid #E0E7FF;border-radius:22px}
          @media(max-width:700px){.main .block-container{padding:1rem 1rem 2rem}[class*="st-key-exercise_card_"]{padding:18px}.tips-grid{grid-template-columns:1fr}.exercise-header p{font-size:.95rem}}
        </style>
        <div class="exercise-header">
          <h1>Mental Wellness Exercises</h1>
          <p>Evidence-informed practices to regulate stress, restore focus, and reconnect with the present—at your own pace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs([label for _, label in CATEGORIES])
    for tab, (category_key, _) in zip(tabs, CATEGORIES):
        with tab:
            if category_key == "quick":
                st.caption("Small, practical tools for a moment when you need a pause.")
            elif category_key == "breathing":
                st.caption("Explore a comfortable pace—never force or hold your breath if it feels uncomfortable.")
            elif category_key == "mindfulness":
                st.caption("Practice gently. There is no need to clear your mind or get it perfect.")
            else:
                st.caption("Use the senses that feel accessible to you; it is okay to skip any step.")

            for exercise in EXERCISES[category_key]:
                _render_exercise(exercise)

    st.markdown(
        """
        <section class="pro-tips-container">
          <h3>✨ Gentle reminders for your practice</h3>
          <div class="tips-grid">
            <div class="tip-card"><strong>Make it yours</strong>Choose a pace and posture that feel comfortable for you.</div>
            <div class="tip-card"><strong>Small is meaningful</strong>A short practice is still a practice. Consistency can grow over time.</div>
            <div class="tip-card"><strong>Check in kindly</strong>Notice how you feel afterward without judging the experience.</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_exercises_page()
