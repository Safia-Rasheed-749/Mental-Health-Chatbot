import streamlit as st
from datetime import datetime, date, timedelta
from db import get_all_user_messages, get_messages_by_conversation
from layout_utils import apply_clean_layout
import json

# ================= SESSION UTILITIES =================
def generate_session_title(messages):
    """
    Generate short session title from first user message.
    """

    mood_keywords = {
        "sad": "Sadness",
        "depress": "Depression",
        "stress": "Stress",
        "anxious": "Anxiety",
        "anxiety": "Anxiety",
        "panic": "Panic",
        "happy": "Happiness",
        "angry": "Anger",
        "fear": "Fear",
        "lonely": "Loneliness",
        "tired": "Fatigue",
        "overthink": "Overthinking",
        "motivation": "Motivation",
        "relationship": "Relationship",
        "study": "Studies",
        "exam": "Exams",
        "sleep": "Sleep Issues",
        "work": "Work Stress",
        "family": "Family Issues"
    }

    first_user = next(
        (msg[1] for msg in messages if msg[0] == "user"),
        "New Chat"
    )

    text = first_user.lower()

    for keyword, label in mood_keywords.items():
        if keyword in text:
            return label

    words = first_user.split()

    if len(words) >= 2:
        return " ".join(words[:2])

    return first_user[:18]

# ================= EXPORT FUNCTION =================
def export_conversation(messages):
    export_data = []

    for role, content in messages:
        export_data.append({
            "role": role,
            "message": content
        })

    return json.dumps(export_data, indent=4)

def show_history(user_id):
    apply_clean_layout(hide_header_completely=False)

    # ================= STYLES =================
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem;
    }
    .stApp{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%) !important;
        }

    .history-title {
        text-align: center;
        font-weight: 600;
        font-size: 34px;
        color: #1e293b;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    .session-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .session-title {
        font-size: 16px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
    }

    .search-box {
        margin-bottom: 18px;
    }
    /* ================= FIX ACTION BUTTON ALIGNMENT ================= */

/* Push search away from action buttons */
div[data-testid="stTextInput"] {
    margin-bottom: 20px !important;
}

/* Action buttons row spacing */
div[data-testid="column"] {
    gap: 10px !important;
}

/* Ensure rename input is more visible */
div[data-testid="stTextInput"] input {
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 10px 12px !important;
    border-radius: 10px !important;
}

/* Make action buttons consistent height */
div[data-testid="stButton"] button {
    height: 42px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* Export button spacing fix */
div[data-testid="stDownloadButton"] {
    margin-top: 0px !important;
}

/* Prevent overlap between columns */
div[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
    align-items: center !important;
}
    </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown(
        "<h1 class='history-title'>📜 Chat History</h1>",
        unsafe_allow_html=True
    )

    # ================= SEARCH =================
    search_query = st.text_input(
        "🔍 Search Session",
        placeholder="Search conversations...",
        key="history_search"
    )

    # ================= SELECTED CONVERSATION VIEW =================
    selected_convo = st.session_state.get("selected_history_conversation")

    if selected_convo is not None:

        messages = get_messages_by_conversation(selected_convo)

        if messages:

            # ===== TOP ACTIONS =====
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                new_name = st.text_input(
                    "Rename Session",
                    value=generate_session_title(messages),
                    key=f"rename_{selected_convo}"
                )

                if st.button("✏️ Save Name", key=f"save_name_{selected_convo}"):
                    if "custom_session_names" not in st.session_state:
                        st.session_state["custom_session_names"] = {}

                    st.session_state["custom_session_names"][selected_convo] = new_name
                    st.success("Session renamed successfully.")

            with col2:
                export_text = export_conversation(messages)

                st.download_button(
                    label="⬇️ Export Chat",
                    data=export_text,
                    file_name=f"conversation_{selected_convo}.json",
                    mime="application/json",
                    key=f"export_{selected_convo}"
                )

            with col3:
                if st.button("🗑️ Delete Session", key=f"delete_{selected_convo}"):

                    if "deleted_sessions" not in st.session_state:
                        st.session_state["deleted_sessions"] = []

                    st.session_state["deleted_sessions"].append(selected_convo)

                    st.session_state.pop("selected_history_conversation", None)

                    st.success("Session deleted.")
                    st.rerun()

            st.markdown("---")

            st.markdown("### Conversation")

            for role, content in messages:

                if role == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                        <div style="background-color: #dbeafe; padding: 10px 14px; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                            👤 {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 20px;">
                        <div style="background-color: #ffffff; padding: 14px 18px; border-radius: 18px; max-width: 85%; word-wrap: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                            🧠 {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("← Back to Today & Yesterday"):
                st.session_state.pop("selected_history_conversation", None)
                st.rerun()

        else:
            st.info("No messages in this conversation.")

        return

    # ================= DEFAULT VIEW =================
    all_msgs = get_all_user_messages(user_id)

    if not all_msgs:
        st.info("No messages yet. Start a conversation in Chat.")
        return

    today = date.today()
    yesterday = today - timedelta(days=1)

    today_msgs = []
    yesterday_msgs = []

    for role, content, ts, conv_id in all_msgs:

        if "deleted_sessions" in st.session_state:
            if str(conv_id) in st.session_state["deleted_sessions"]:
                continue

        if isinstance(ts, datetime):
            msg_date = ts.date()
        else:
            msg_date = today

        if msg_date == today:
            today_msgs.append((role, content, ts, conv_id))

        elif msg_date == yesterday:
            yesterday_msgs.append((role, content, ts, conv_id))

    # ================= SEARCH FILTER =================
    if search_query:

        today_msgs = [
            msg for msg in today_msgs
            if search_query.lower() in msg[1].lower()
        ]

        yesterday_msgs = [
            msg for msg in yesterday_msgs
            if search_query.lower() in msg[1].lower()
        ]

    if not today_msgs and not yesterday_msgs:
        st.info(
            "No messages from today or yesterday. "
            "Click a session on the left to see older chats."
        )
        return

    # ================= TODAY =================
    if today_msgs:

        st.markdown("### Today")

        for role, content, ts, conv_id in today_msgs:

            if role == "user":

                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                    <div style="background-color: #dbeafe; padding: 10px 14px; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                        👤 {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 20px;">
                    <div style="background-color: #ffffff; padding: 14px 18px; border-radius: 18px; max-width: 85%; word-wrap: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        🧠 {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ================= YESTERDAY =================
    if yesterday_msgs:

        st.markdown("### Yesterday")

        for role, content, ts, conv_id in yesterday_msgs:

            if role == "user":

                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                    <div style="background-color: #dbeafe; padding: 10px 14px; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                        👤 {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 20px;">
                    <div style="background-color: #ffffff; padding: 14px 18px; border-radius: 18px; max-width: 85%; word-wrap: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                            🧠 {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)