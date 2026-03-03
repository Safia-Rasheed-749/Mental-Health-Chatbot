# journal.py
import streamlit as st
from db import add_journal, get_journals
from datetime import datetime

def show_journal(user_id):
    st.title("📝 Personal Journal")

    # ---------------- Journal Entry Input ----------------
    st.markdown("### Write your thoughts here:")
    entry = st.text_area("", placeholder="Type your journal entry...", height=150)

    # Initialize session state for tracking last saved entry
    if 'last_journal' not in st.session_state:
        st.session_state['last_journal'] = None

    if st.button("Save Entry", key="save_journal"):
        if entry.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_entry = f"[{timestamp}] {entry.strip()}"
            add_journal(user_id, full_entry)
            st.success("✅ Journal entry saved successfully!")

            # Update session state to force re-render of entries
            st.session_state['last_journal'] = full_entry

        else:
            st.warning("⚠️ Cannot save an empty journal entry.")

    # ---------------- Display Recent Journal Entries ----------------
    journals = get_journals(user_id)

    # Include the latest just-saved entry from this session if not in DB yet
    if st.session_state.get('last_journal'):
        if journals and st.session_state['last_journal'] not in journals:
            journals.append(st.session_state['last_journal'])
        elif not journals:
            journals = [st.session_state['last_journal']]

    if journals:
        st.markdown("### Recent Entries")
        for j in reversed(journals[-5:]):  # show last 5 entries, most recent first
            st.markdown(
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px; margin-bottom:5px;'>{j}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("You have no journal entries yet. Start writing above!")