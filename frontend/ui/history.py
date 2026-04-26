import streamlit as st
from db import get_messages
from layout_utils import apply_clean_layout


def detect_emotion(text):
    text = text.lower()

    if any(w in text for w in ["stress", "worried", "anxious", "tired", "sad", "bad"]):
        return "😟 Anxious"
    elif any(w in text for w in ["happy", "good", "great", "love", "nice", "better"]):
        return "😊 Positive"
    elif any(w in text for w in ["angry", "hate", "annoyed"]):
        return "😡 Angry"
    else:
        return "⚖ Neutral"


def show_history(user_id):
    apply_clean_layout(hide_header_completely=False)

    # ---------------- TITLE ----------------
    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:34px;
            font-weight:600;
            color:#1e293b;
            margin-bottom:6px;
        ">
        📜 Chat History
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

    # ---------------- DATA ----------------
    messages = get_messages(user_id)

    if not messages:
        st.info("No chat history found.")
        return

    # ---------------- SEARCH ----------------
    search = st.text_input("🔍 Search chat history")

    if search:
        messages = [(r, c) for r, c in messages if search.lower() in c.lower()]

    # ---------------- AI SUMMARY ----------------
    sentiments = [detect_emotion(c) for _, c in messages]

    stress = sentiments.count("😟 Anxious")
    positive = sentiments.count("😊 Positive")

    if messages:
        if stress > positive:
            summary = "⚠ Your conversations show stress patterns."
        elif positive > stress:
            summary = "😊 Positive interaction detected."
        else:
            summary = "⚖ Balanced conversation tone."

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,#e0f7f4,#ede9fe);
            padding:16px;
            border-radius:16px;
            margin-bottom:20px;
            box-shadow:0 6px 18px rgba(0,0,0,0.05);
        ">
            <b>🧠 AI Chat Insight</b><br><br>
            {summary}
        </div>
        """, unsafe_allow_html=True)

    # ---------------- STYLING ----------------
    st.markdown("""
    <style>

    /* USER (LEFT SIDE) */
    .user-bubble {
        background: #f1f5f9;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 4px;
        margin: 6px 0;
        max-width: 75%;
        margin-right: auto;
        font-size: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    /* ASSISTANT (RIGHT BLUE BOX - FIXED AS REQUESTED) */
    .assistant-bubble {
        background: linear-gradient(135deg, #4facfe, #00c6ff);
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px;
        margin: 6px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .emotion-tag {
        font-size: 11px;
        margin-top: 4px;
        opacity: 0.8;
    }

    .date-group {
        margin-top: 18px;
        margin-bottom: 8px;
        font-weight: 600;
        color: #334155;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- GROUPING (SAME LOGIC) ----------------
    grouped = {
        "Today": [],
        "Yesterday": [],
        "Earlier": []
    }

    for i, (role, content) in enumerate(messages):
        if i < 5:
            grouped["Today"].append((role, content))
        elif i < 10:
            grouped["Yesterday"].append((role, content))
        else:
            grouped["Earlier"].append((role, content))

    # ---------------- DISPLAY ----------------
    for group, msgs in grouped.items():

        if not msgs:
            continue

        st.markdown(f"<div class='date-group'>📅 {group}</div>", unsafe_allow_html=True)

        for role, content in msgs:

            emotion = detect_emotion(content)

            # 👤 USER (with icon restored)
            if role == "user":
                st.markdown(f"""
                <div class='user-bubble'>
                    👤 {content}
                    <div class='emotion-tag'>{emotion}</div>
                </div>
                """, unsafe_allow_html=True)

            # 🤖 ASSISTANT (blue box + icon restored)
            else:
                st.markdown(f"""
                <div class='assistant-bubble'>
                    🤖 {content}
                    <div class='emotion-tag'>{emotion}</div>
                </div>
                """, unsafe_allow_html=True)