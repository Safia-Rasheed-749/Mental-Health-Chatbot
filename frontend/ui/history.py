import streamlit as st
from datetime import datetime, date, timedelta
from db import get_all_user_messages, get_messages_by_conversation
from layout_utils import apply_clean_layout

def show_history(user_id):
    apply_clean_layout(hide_header_completely=False)

    st.title("📜 Chat History")

    # If a specific conversation is selected (from sidebar), show that full conversation
    selected_convo = st.session_state.get("selected_history_conversation")
    if selected_convo is not None:
        messages = get_messages_by_conversation(selected_convo)
        if messages:
            st.markdown("### Conversation")
            for role, content in messages:
                if role == "user":
                    # User bubble (light blue, right-aligned, 👤 inside)
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                        <div style="background-color: #dbeafe; padding: 10px 14px; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                            👤 {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Assistant bubble (white with shadow, left-aligned, 🧠 inside)
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 20px;">
                        <div style="background-color: #ffffff; padding: 14px 18px; border-radius: 18px; max-width: 85%; word-wrap: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                            🧠 {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            # Back button to return to default view
            if st.button("← Back to Today & Yesterday"):
                st.session_state.pop("selected_history_conversation", None)
                st.rerun()
        else:
            st.info("No messages in this conversation.")
        return

    # DEFAULT VIEW: only Today and Yesterday messages (from all conversations)
    all_msgs = get_all_user_messages(user_id)
    if not all_msgs:
        st.info("No messages yet. Start a conversation in Chat.")
        return

    today = date.today()
    yesterday = today - timedelta(days=1)

    today_msgs = []
    yesterday_msgs = []

    for role, content, ts, conv_id in all_msgs:
        if isinstance(ts, datetime):
            msg_date = ts.date()
        else:
            msg_date = today

        if msg_date == today:
            today_msgs.append((role, content, ts))
        elif msg_date == yesterday:
            yesterday_msgs.append((role, content, ts))

    if not today_msgs and not yesterday_msgs:
        st.info("No messages from today or yesterday. Click a session on the left to see older chats.")
        return

    # Display Today messages
    if today_msgs:
        st.markdown("### Today")
        for role, content, ts in today_msgs:
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

    # Display Yesterday messages
    if yesterday_msgs:
        st.markdown("### Yesterday")
        for role, content, ts in yesterday_msgs:
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