import streamlit as st
from db import add_journal, get_journals
from datetime import datetime

def show_journal(user_id):
    # --- Remove top white space ---
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: -0.5rem !important;
        }
        .main .block-container > :first-child {
            margin-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📝 Personal Journal")
    st.markdown("### Write your thoughts here:")
    entry = st.text_area("", placeholder="Type your journal entry...", height=150)

    if 'last_journal' not in st.session_state:
        st.session_state['last_journal'] = None

    if st.button("Save Entry", key="save_journal"):
        if entry.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_entry = f"[{timestamp}] {entry.strip()}"
            add_journal(user_id, full_entry)
            st.success("✅ Journal entry saved successfully!")
            st.session_state['last_journal'] = full_entry
        else:
            st.warning("⚠️ Cannot save an empty journal entry.")

    journals = get_journals(user_id)
    if st.session_state.get('last_journal'):
        if journals and st.session_state['last_journal'] not in journals:
            journals.append(st.session_state['last_journal'])
        elif not journals:
            journals = [st.session_state['last_journal']]

    if journals:
        st.markdown("### Recent Entries")
        for j in reversed(journals[-5:]):
            st.markdown(
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px; margin-bottom:5px;'>{j}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("You have no journal entries yet. Start writing above!")