# -*- coding: utf-8 -*-
import os
import streamlit as st
from datetime import datetime

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

EXERCISES = {
    "quick": [
        {
            "id": "reset",
            "icon": "✦",
            "title": "A one-minute reset",
            "duration": "1 minute",
            "summary": "A gentle reset for moments when everything feels like too much.",
            "why": "Slowing down your exhale can help your body shift toward a calmer state.",
            "source": "Based on slow-breathing research (Zaccaro et al., 2018).",
            "breathing_guide": True,
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
            "source": "Informed by orienting practices used in trauma-informed care.",
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
            "source": "Commonly used in stress-management and performance settings.",
            "breathing_guide": True,
            "breathing_pattern": "box",
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
            "source": "Popularised by Dr. Andrew Weil; rooted in pranayama traditions.",
            "breathing_guide": True,
            "breathing_pattern": "478",
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
            "source": "Adapted from Kabat-Zinn's mindfulness-based stress reduction (MBSR).",
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
            "source": "Adapted from MBSR body-scan practice (Kabat-Zinn).",
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
            "source": "Widely used in DBT distress-tolerance skills (Linehan).",
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
            "source": "Derived from grounding techniques in trauma-informed practice.",
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

MOOD_RECOMMENDATION = {
    1: "grounding",
    2: "breathing",
    3: "mindfulness",
    4: "quick",
    5: "quick",
}

CRISIS_RESOURCES = [
    ("Pakistan — Umang", "0311-7786264", "https://www.umang.com.pk/"),
    ("International — Befrienders", "Visit site", "https://www.befrienders.org/"),
    ("Emergency (Pakistan)", "1122", ""),
]

MEDIA_DIR = "assets/media"

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------

def _init_state():
    st.session_state.setdefault("completed_exercises", [])
    st.session_state.setdefault("completed_steps", {})
    st.session_state.setdefault("mood", None)
    st.session_state.setdefault("recommended_category", None)

_init_state()

# ---------------------------------------------------------------------------
# BREATHING CIRCLE
# ---------------------------------------------------------------------------

def _breathing_circle(pattern: str = "box"):
    if pattern == "478":
        keyframes = """
        @keyframes bcycle {
          0%   { transform: scale(0.9); }
          21%  { transform: scale(1.55); }
          58%  { transform: scale(1.55); }
          100% { transform: scale(0.9); }
        }
        """
        cycle = "19s"
        phase_html = """
        <div class="phase-row">
          <span class="phase inhale">Inhale 4</span>
          <span class="phase hold">Hold 7</span>
          <span class="phase exhale">Exhale 8</span>
        </div>
        """
    elif pattern == "calm":
        keyframes = """
        @keyframes bcycle {
          0%   { transform: scale(0.9); }
          40%  { transform: scale(1.55); }
          100% { transform: scale(0.9); }
        }
        """
        cycle = "10s"
        phase_html = """
        <div class="phase-row">
          <span class="phase inhale">Inhale 4</span>
          <span class="phase exhale">Exhale 6</span>
        </div>
        """
    else:  # box
        keyframes = """
        @keyframes bcycle {
          0%   { transform: scale(0.9); }
          25%  { transform: scale(1.55); }
          50%  { transform: scale(1.55); }
          75%  { transform: scale(0.9); }
          100% { transform: scale(0.9); }
        }
        """
        cycle = "16s"
        phase_html = """
        <div class="phase-row">
          <span class="phase inhale">Inhale 4</span>
          <span class="phase hold">Hold 4</span>
          <span class="phase exhale">Exhale 4</span>
          <span class="phase hold">Hold 4</span>
        </div>
        """

    st.markdown(
        f"""
        <style>
          {keyframes}
          .breath-stage {{
            position: relative;
            display: grid;
            place-items: center;
            height: 240px;
            margin: 12px 0 6px;
          }}
          .breath-halo {{
            position: absolute;
            width: 180px; height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,.35) 0%, rgba(99,102,241,0) 70%);
            animation: bcycle {cycle} ease-in-out infinite;
            filter: blur(2px);
          }}
          .breath-circle {{
            position: relative;
            width: 120px; height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #C7D2FE 0%, #6366F1 70%, #4F46E5 100%);
            box-shadow: 0 0 40px rgba(99,102,241,.45),
                        inset 0 0 20px rgba(255,255,255,.35);
            animation: bcycle {cycle} ease-in-out infinite;
            display: grid;
            place-items: center;
            color: #FFFFFF;
            font-weight: 700;
            letter-spacing: .06em;
            font-size: 11px;
            text-transform: uppercase;
          }}
          .breath-circle::after {{ content: "Breathe"; opacity: .85; }}
          .phase-row {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0 6px;
          }}
          .phase {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .06em;
            padding: 5px 11px;
            border-radius: 999px;
            border: 1px solid #E0E7FF;
            color: #4F46E5;
            background: #EEF2FF;
          }}
          .phase.hold  {{ background:#F5F3FF; color:#7C3AED; border-color:#DDD6FE; }}
          .phase.exhale{{ background:#F8FAFF; color:#6366F1; border-color:#E0E7FF; }}
          .breath-caption {{
            text-align: center;
            color: #6366F1;
            font-size: 12.5px;
            margin: 4px 0 14px;
            font-weight: 600;
          }}
        </style>

        <div class="breath-stage" aria-hidden="true">
          <div class="breath-halo"></div>
          <div class="breath-circle"></div>
        </div>
        {phase_html}
        <p class="breath-caption">Follow the circle — expand = inhale, contract = exhale.</p>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# MEDIA (local video / audio)
# ---------------------------------------------------------------------------

def _render_media(exercise: dict):
    video_path = os.path.join(MEDIA_DIR, f"{exercise['id']}.mp4")
    audio_path = os.path.join(MEDIA_DIR, f"{exercise['id']}.mp3")

    has_video = os.path.exists(video_path)
    has_audio = os.path.exists(audio_path)

    if has_video:
        with st.expander("▶  Watch guided demo", expanded=False):
            try:
                st.video(video_path)
            except Exception:
                st.caption("Video could not be loaded.")
    if has_audio:
        with st.expander("🎧  Listen to audio guide", expanded=False):
            try:
                st.audio(audio_path)
            except Exception:
                st.caption("Audio could not be loaded.")

# ---------------------------------------------------------------------------
# UI HELPERS
# ---------------------------------------------------------------------------

def _record_completion(exercise_id: str):
    st.session_state["completed_exercises"].append(
        {"id": exercise_id, "at": datetime.now().isoformat(timespec="seconds")}
    )


def _render_disclaimer():
    st.markdown(
        """
        <div class="disclaimer-banner" role="note">
          <span class="disclaimer-icon" aria-hidden="true">ℹ️</span>
          <div>
            <strong>This tool supports wellbeing — it is not a substitute for professional care.</strong>
            If you are in crisis or feel unsafe, please contact a helpline listed at the bottom of this page.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_mood_check():
    st.markdown('<div class="mood-check-label">Before you begin — how are you feeling right now?</div>',
                unsafe_allow_html=True)
    cols = st.columns(5)
    labels = [
        ("😣", "Very low", 1),
        ("😔", "Low", 2),
        ("😐", "Okay", 3),
        ("🙂", "Good", 4),
        ("😌", "Calm", 5),
    ]
    for col, (emoji, label, value) in zip(cols, labels):
        with col:
            if st.button(f"{emoji}\n\n{label}", key=f"mood_{value}", use_container_width=True):
                st.session_state["mood"] = value
                st.session_state["recommended_category"] = MOOD_RECOMMENDATION[value]

    if st.session_state["mood"] is not None:
        rec = st.session_state["recommended_category"]
        rec_label = dict(CATEGORIES)[rec]
        mood = st.session_state["mood"]
        st.markdown(
            f"""
            <div class="recommendation-strip">
              <strong>Suggested for you:</strong> {rec_label}
              <span class="rec-note">based on how you're feeling (mood {mood}/5)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


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

        if exercise.get("breathing_guide"):
            pattern = exercise.get("breathing_pattern", "calm")
            _breathing_circle(pattern)

        _render_media(exercise)

        interactive = exercise["id"] in {"mindful-moment", "body-scan", "54321", "steady-object"}

        if interactive:
            st.session_state["completed_steps"].setdefault(
                exercise["id"], [False] * len(exercise["steps"])
            )
            current = st.session_state["completed_steps"][exercise["id"]]

            selections = []
            for index, step in enumerate(exercise["steps"]):
                checked = st.checkbox(
                    step,
                    key=f"check_{exercise['id']}_{index}",
                    value=current[index],
                )
                selections.append(checked)

            st.session_state["completed_steps"][exercise["id"]] = selections
            completed = sum(selections)
            st.progress(completed / len(selections), text=f"{completed} of {len(selections)} steps")

            if completed == len(selections):
                st.success("Practice complete. Take a moment to notice how you feel.")
                already = any(e["id"] == exercise["id"] for e in st.session_state["completed_exercises"])
                if not already:
                    _record_completion(exercise["id"])
        else:
            for index, step in enumerate(exercise["steps"], 1):
                st.markdown(
                    f'<div class="step-pill"><span>{index}</span>{step}</div>',
                    unsafe_allow_html=True,
                )
            if st.button(f"Mark '{exercise['title']}' as done", key=f"done_{exercise['id']}"):
                _record_completion(exercise["id"])
                st.success("Logged. Well done for taking this moment.")

        with st.expander("Source / basis"):
            st.caption(exercise["source"])


def _render_crisis_footer():
    items = "".join(
        f'<li><strong>{name}</strong> — '
        + (f'<a href="{url}" target="_blank" rel="noopener">{number}</a>' if url else f'{number}')
        + "</li>"
        for name, number, url in CRISIS_RESOURCES
    )
    st.markdown(
        f"""
        <section class="crisis-footer" role="contentinfo">
          <h3>🆘 If you need urgent support</h3>
          <p>This tool is not a crisis service. If you are in danger or need immediate help, please reach out:</p>
          <ul>{items}</ul>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_session_summary():
    log = st.session_state["completed_exercises"]
    if not log:
        return
    unique = {e["id"] for e in log}
    st.markdown(
        f"""
        <div class="session-summary">
          <strong>Session so far:</strong> {len(log)} practice(s) logged · {len(unique)} unique exercise(s)
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# PAGE
# ---------------------------------------------------------------------------

def show_exercises_page():
    st.markdown(
        """
        <style>
          header,[data-testid="stHeader"],footer{display:none!important}
          .main .block-container{max-width:1120px;padding:1.5rem 2rem 3rem}

          .stApp{background:linear-gradient(180deg,#F8FAFC 0%,#F5F3FF 100%);color:#1E293B}

          /* ---------- HEADER ---------- */
          .exercise-header{text-align:center;margin:0 auto 2rem;max-width:780px}
          .exercise-header h1{color:#1E1B4B;font-size:clamp(2rem,4vw,2.7rem);
            letter-spacing:-.035em;margin:0 0 .65rem;font-weight:750}
          .exercise-header p{color:#64748B;font-size:1.05rem;line-height:1.65;margin:0}

          /* ---------- TABS ---------- */
          [data-testid="stTabs"] [data-testid="stTab"]{color:#64748B;font-weight:600}
          [data-testid="stTabs"] [aria-selected="true"]{color:#4F46E5}
          [data-testid="stTabs"] [data-baseweb="tab-highlight"]{background:#6366F1}
          /* give tabs a clean card-like bar */
          [data-testid="stTabs"] [data-baseweb="tab-list"]{
            gap: 6px;
            padding: 6px;
            background: #FFFFFF;
            border: 1px solid #EEF2FF;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(99,102,241,.06);
            margin-bottom: 1.25rem;
          }

          /* ---------- EXERCISE CARD ---------- */
          [class*="st-key-exercise_card_"]{
            background:#fff;border:1px solid #EEF2FF;border-radius:20px;
            padding:26px 26px 22px;
            box-shadow:0 4px 20px rgba(99,102,241,.06);
            margin:22px 0 22px;
            width:100%;
          }
          .card-heading{display:flex;align-items:center;gap:14px;margin-bottom:6px}
          .icon-badge{display:grid;place-items:center;flex:0 0 48px;height:48px;
            border-radius:16px;background:#EEF2FF;color:#6366F1;font-size:25px;font-weight:600}
          .eyebrow{font-size:10px;font-weight:750;letter-spacing:.12em;color:#818CF8;margin-bottom:4px}
          [class*="st-key-exercise_card_"] h3{font-size:1.2rem;line-height:1.3;
            color:#1E1B4B;margin:0;font-weight:700}
          .summary{color:#475569;line-height:1.6;margin:18px 0 12px;font-size:14px}
          .why{color:#64748B;background:#F8FAFF;border:1px solid #EEF2FF;
            padding:12px 14px;border-radius:12px;font-size:13px;line-height:1.6;margin:0 0 20px}
          .why strong{color:#4F46E5}
          .steps-label{font-size:10px;letter-spacing:.12em;font-weight:750;
            color:#94A3B8;margin:4px 0 12px}

          .step-pill{display:flex;align-items:flex-start;gap:12px;background:#F5F3FF;
            color:#4F46E5;padding:13px 16px;border-radius:12px;font-weight:600;
            margin:10px 0;border-left:4px solid #6366F1;line-height:1.55;font-size:13px}
          .step-pill span{display:grid;place-items:center;flex:0 0 22px;height:22px;
            border-radius:50%;background:#E0E7FF;color:#4F46E5;font-size:11px}

          /* ---------- BUTTONS ---------- */
          .stButton>button{border-radius:12px;min-height:44px;font-weight:650;
            transition:all .18s ease}
          .stButton>button:hover{transform:translateY(-1px);
            box-shadow:0 7px 18px rgba(99,102,241,.16)}

          /* ---------- PRO TIPS ---------- */
          .pro-tips-container{background:linear-gradient(135deg,#EEF2FF 0%,#F5F3FF 100%);
            border:1px solid #E0E7FF;border-radius:20px;padding:28px;margin-top:48px;color:#1E1B4B}
          .pro-tips-container h3{text-align:center;color:#312E81;margin:0 0 20px;font-size:1.2rem}
          .tips-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
          .tip-card{text-align:center;padding:16px;border-radius:14px;
            background:rgba(255,255,255,.65);color:#4338CA;font-size:13px;line-height:1.55}
          .tip-card strong{display:block;color:#312E81;margin-bottom:6px}

          /* ---------- DISCLAIMER ---------- */
          .disclaimer-banner{display:flex;gap:12px;align-items:flex-start;
            background:#F8FAFF;border:1px solid #E0E7FF;border-left:4px solid #6366F1;
            border-radius:14px;padding:15px 18px;margin:0 0 26px;
            color:#475569;font-size:13px;line-height:1.6}
          .disclaimer-banner strong{color:#312E81}
          .disclaimer-icon{font-size:16px;line-height:1.4}

          /* ---------- MOOD CHECK ---------- */
          .mood-check-label{text-align:center;color:#4F46E5;font-weight:650;
            font-size:14px;margin:6px 0 16px}

          /* ---------- RECOMMENDATION ---------- */
          .recommendation-strip{margin:20px 0 6px;padding:13px 18px;
            background:#EEF2FF;border:1px solid #E0E7FF;border-radius:12px;
            color:#312E81;font-size:13.5px;text-align:center}
          .rec-note{color:#6366F1;font-weight:600;margin-left:6px}

          /* ---------- SESSION SUMMARY ---------- */
          .session-summary{margin:22px 0 12px;padding:13px 18px;
            background:#F5F3FF;border:1px dashed #C7D2FE;border-radius:12px;
            color:#4338CA;font-size:13px;text-align:center}

          /* ---------- CRISIS FOOTER ---------- */
          .crisis-footer{margin-top:48px;background:#fff;border:1px solid #E0E7FF;
            border-radius:20px;padding:24px 28px;color:#1E1B4B}
          .crisis-footer h3{margin:0 0 10px;color:#312E81;font-size:1.05rem}
          .crisis-footer p{margin:0 0 12px;color:#64748B;font-size:13px}
          .crisis-footer ul{margin:0;padding-left:18px;color:#475569;
            font-size:13px;line-height:1.8}
          .crisis-footer a{color:#4F46E5;text-decoration:none;font-weight:600}
          .crisis-footer a:hover{text-decoration:underline}

          /* extra breathing space for Streamlit widgets inside cards */
          [class*="st-key-exercise_card_"] [data-testid="stExpander"]{
            margin-top:10px; border-radius:12px; border:1px solid #EEF2FF;
          }
          [class*="st-key-exercise_card_"] [data-testid="stExpander"] summary{
            font-size:13px; font-weight:650; color:#4F46E5;
          }

          [data-testid="stDialog"]>div{border:1px solid #E0E7FF;border-radius:22px}

          @media(max-width:700px){
            .main .block-container{padding:1rem 1rem 2rem}
            [class*="st-key-exercise_card_"]{padding:18px}
            .tips-grid{grid-template-columns:1fr}
            .exercise-header p{font-size:.95rem}
          }
        </style>

        <div class="exercise-header">
          <h1>Mental Wellness Exercises</h1>
          <p>Evidence-informed practices to regulate stress, restore focus, and reconnect with the present—at your own pace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Disclaimer
    _render_disclaimer()

    # 2. Mood check
    _render_mood_check()

    # 3. Small spacer before session summary
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    _render_session_summary()

    # 4. Big spacer before tabs
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # 5. Tabs
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

            if st.session_state["recommended_category"] == category_key:
                st.info("✨ Recommended based on your mood check-in.", icon="✨")

            for exercise in EXERCISES[category_key]:
                _render_exercise(exercise)

    # 6. Pro tips
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

    _render_crisis_footer()


if __name__ == "__main__":
    show_exercises_page()