# admin.py (modified)
import streamlit as st
import pandas as pd
from db import get_all_users, get_messages_by_user, get_moods_by_user, get_journals_by_user
from layout_utils import apply_clean_layout   # add

def show_admin_panel():
    apply_clean_layout(hide_header_completely=False)   # <--- ADDED
    
    # Remove the old CSS block that sets .main .block-container padding/margin.
    # Keep only the custom styling for cards and back button.
    st.markdown("""
    <style>
        /* Optional: adjust header spacing */
        .admin-header {
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #1e3c72;
        }
        .back-button-wrapper div.stButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
        }
        .back-button-wrapper div.stButton > button:hover {
            background-color: #45a049 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ... rest unchanged

    st.markdown('<div class="admin-header"><h1>🛡️ Admin Dashboard</h1><p>Manage users and view platform data</p></div>', unsafe_allow_html=True)

    users = get_all_users()
    if not users:
        st.warning("No users found.")
        return

    total_users = len(users)
    total_messages = sum(len(get_messages_by_user(u['id'])) for u in users)
    total_moods = sum(len(get_moods_by_user(u['id'])) for u in users)
    total_journals = sum(len(get_journals_by_user(u['id'])) for u in users)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_users}</div><div class="stat-label">Total Users</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_messages}</div><div class="stat-label">Messages</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_moods}</div><div class="stat-label">Mood Logs</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_journals}</div><div class="stat-label">Journal Entries</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["👥 All Users", "💬 User Chats", "😊 User Moods", "📓 User Journals"])

    with tab1:
        users_df = pd.DataFrame(users)
        display_cols = ['id', 'username', 'email']
        if 'is_admin' in users_df.columns:
            display_cols.append('is_admin')
        if 'created_at' in users_df.columns:
            display_cols.append('created_at')
        st.dataframe(users_df[display_cols], use_container_width=True)

    with tab2:
        selected_user = st.selectbox("Select user", users, format_func=lambda u: f"{u['username']} ({u['email']})")
        if selected_user:
            messages = get_messages_by_user(selected_user['id'])
            if messages:
                chat_df = pd.DataFrame(messages, columns=["Role", "Content", "Timestamp"])
                st.dataframe(chat_df, use_container_width=True)
            else:
                st.info("No messages.")

    with tab3:
        selected_user2 = st.selectbox("Select user for moods", users, format_func=lambda u: f"{u['username']} ({u['email']})", key="mood")
        if selected_user2:
            moods = get_moods_by_user(selected_user2['id'])
            if moods:
                moods_df = pd.DataFrame(moods, columns=["Mood", "Timestamp"])
                st.dataframe(moods_df, use_container_width=True)
            else:
                st.info("No mood logs.")

    with tab4:
        selected_user3 = st.selectbox("Select user for journals", users, format_func=lambda u: f"{u['username']} ({u['email']})", key="journal")
        if selected_user3:
            journals = get_journals_by_user(selected_user3['id'])
            if journals:
                journals_df = pd.DataFrame(journals, columns=["Entry", "Timestamp"])
                st.dataframe(journals_df, use_container_width=True)
            else:
                st.info("No journal entries.")

    # FIXED BACK BUTTON with custom wrapper to change its color
    st.markdown('<div class="back-button-wrapper">', unsafe_allow_html=True)
    if st.button("🔙 Back to Main App", key="admin_back"):
        st.session_state.page = "dashboard"
        st.session_state.current_page = "Dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_admin_panel()