import streamlit as st
import pandas as pd
from db import get_all_users, get_messages_by_user, get_moods_by_user, get_journals_by_user,get_last_activity_with_details, get_user_activity_log
from layout_utils import apply_clean_layout
from datetime import datetime

def show_admin_panel():
    apply_clean_layout(hide_header_completely=False)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, .stApp, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #0B0F19 !important;
        }
        .main .block-container {
            background-color: #0B0F19 !important;
            padding-top: 0.5rem !important;
        }

        /* ── HEADER ── */
        .admin-header {
            margin-top: -3rem;
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
            border: 1px solid #4338ca;
            padding: 1.4rem 2rem;
            border-radius: 14px;
            color: #E5E7EB;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 24px rgba(99,102,241,0.25);
        }
        .admin-header h1 {
            margin: 0;
            font-size: 1.75rem;
            font-weight: 800;
            color: #F9FAFB;
            letter-spacing: -0.3px;
        }
        .admin-header p {
            margin: 0.3rem 0 0;
            color: #a5b4fc;
            font-size: 0.9rem;
            font-weight: 400;
        }

        /* ── STAT CARDS ── */
        .stat-card {
            background: #111827;
            border-radius: 12px;
            padding: 1.4rem 1.2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            border: 1px solid #1F2937;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            border-color: #6366F1;
        }
        .stat-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #6366F1;
            margin-bottom: 0.4rem;
            font-family: 'Inter', sans-serif;
        }
        .stat-label {
            font-size: 0.82rem;
            color: #9CA3AF;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        /* ── BUTTONS ── */
        button {
            background: #6366F1 !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 10px 28px !important;
            border-radius: 10px !important;
            font-size: 0.9rem !important;
            box-shadow: 0 2px 8px rgba(99,102,241,0.3) !important;
            transition: background 0.2s ease !important;
            font-family: 'Inter', sans-serif !important;
        }
        button:hover {
            background: #4F46E5 !important;
            transform: translateY(-1px) !important;
        }

        /* ── PROFESSIONAL TABLE ── */
        .professional-table {
            width: 100% !important;
            border-collapse: collapse !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.88rem !important;
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            margin: 1.5rem 0 !important;
        }
        .professional-table thead th {
            background: #1F2937 !important;
            color: #E5E7EB !important;
            font-weight: 700 !important;
            font-size: 0.8rem !important;
            padding: 14px 16px !important;
            border: none !important;
            text-align: left !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
        }
        .professional-table tbody tr {
            border-bottom: 1px solid #1F2937 !important;
            transition: background 0.15s ease !important;
        }
        .professional-table tbody tr:nth-child(odd) {
            background-color: rgba(255,255,255,0.02) !important;
        }
        .professional-table tbody tr:nth-child(even) {
            background-color: rgba(255,255,255,0.05) !important;
        }
        .professional-table tbody tr:hover {
            background-color: rgba(99,102,241,0.12) !important;
        }
        .professional-table td {
            padding: 13px 16px !important;
            color: #E5E7EB !important;
            font-weight: 400 !important;
            font-size: 0.88rem !important;
            line-height: 1.5 !important;
            border: none !important;
            vertical-align: middle !important;
        }
        /* Admin column */
        .professional-table td:nth-child(4) {
            font-weight: 600 !important;
            color: #22C55E !important;
        }
        /* Timestamp column */
        .professional-table td:last-child {
            color: #9CA3AF !important;
            font-size: 0.82rem !important;
            font-family: 'Inter', monospace !important;
        }

        /* ── TABS ── */
        div[role="tablist"] button[role="tab"] {
            border-radius: 8px !important;
            border: 1px solid #1F2937 !important;
            background: #111827 !important;
            color: #9CA3AF !important;
            padding: 8px 16px !important;
            margin: 0 6px 0 0 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        div[role="tablist"] button[role="tab"][aria-selected="true"] {
            background: #6366F1 !important;
            border-color: #6366F1 !important;
            color: #ffffff !important;
        }
        div[data-testid="stTab"] {
            padding: 0.5rem 0 !important;
        }

        /* ── SELECTBOX / LABELS ── */
        div[data-testid="stSelectbox"] label,
        label[data-testid="stMetricLabel"] {
            color: #E5E7EB !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
        }
        div[data-testid="stMetricValue"] {
            color: #6366F1 !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricValue"] p {
            color: #6366F1 !important;
            font-size: 1.6rem !important;
        }
        div[data-testid="stMetric"] {
            background: #111827 !important;
            border-radius: 10px !important;
            padding: 14px !important;
            border: 1px solid #1F2937 !important;
        }

        /* ── DIVIDER ── */
        hr {
            border-color: #1F2937 !important;
            margin: 1.5rem 0 !important;
        }

        @media (max-width: 768px) {
            .professional-table td,
            .professional-table th {
                padding: 10px 12px !important;
                font-size: 0.82rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="admin-header"><h1 style="margin: 0; font-size: 2rem; font-weight: 800;">🛡️ Admin Dashboard</h1><p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Manage users and view platform data</p></div>', unsafe_allow_html=True)

    users = get_all_users()
    if not users:
        st.warning("No users found.")
        return

    def get_last_activity(user_id):
        latest = None
        messages = get_messages_by_user(user_id)
        if messages:
            latest = max(latest, max(m[2] for m in messages)) if latest else max(m[2] for m in messages)
        moods = get_moods_by_user(user_id)
        if moods:
            latest = max(latest, max(m[1] for m in moods)) if latest else max(m[1] for m in moods)
        journals = get_journals_by_user(user_id)
        if journals:
            latest = max(latest, max(j[1] for j in journals)) if latest else max(j[1] for j in journals)
        return latest

    total_users = len(users)
    total_messages = sum(len(get_messages_by_user(u['id'])) for u in users)
    total_moods = sum(len(get_moods_by_user(u['id'])) for u in users)
    total_journals = sum(len(get_journals_by_user(u['id'])) for u in users)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_users}</div>
            <div class="stat-label">Total Users</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_messages}</div>
            <div class="stat-label">Messages</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_moods}</div>
            <div class="stat-label">Mood Logs</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_journals}</div>
            <div class="stat-label">Journal Entries</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 All Users", "💬 User Chats", "😊 User Moods", "📓 User Journals", "📊 Activity Logs"])

    def render_styled_table(df, timestamp_cols=None):
        if df.empty:
            st.info("No data to display.")
            return
        
        # Format timestamps
        if timestamp_cols:
            for col in timestamp_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime("%Y-%m-%d %H:%M")
        
        # Handle Admin column
        if 'Admin' in df.columns:
            df['Admin'] = df['Admin'].map({True: 'True', False: 'False'})
        
        # Replace NaN
        df = df.fillna("Never")
        
        html_table = df.to_html(
            classes='professional-table', 
            index=False, 
            escape=False,
            border=0
        )
        
        st.markdown(f'''
        <div style="
            background: #111827;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            border: 1px solid #1F2937;
            overflow-x: auto;
        ">
            {html_table}
        </div>
        ''', unsafe_allow_html=True)

    with tab1:
        users_data = []
        for u in users:
            last_active, last_action_details = get_last_activity_with_details(u['id'])
            users_data.append({
                'ID': u['id'],
                'Username': u['username'],
                'Email': u['email'],
                'Admin': u.get('is_admin', False),
                'Created': u.get('created_at'),
                'Last Active': last_active.strftime("%Y-%m-%d %H:%M") if last_active and last_active.year > 1970 else "Never",
                'Last Action': last_action_details  # NEW COLUMN
            })
        users_df = pd.DataFrame(users_data)
        render_styled_table(users_df, timestamp_cols=['Created', 'Last Active'])

    with tab2:
        selected_user = st.selectbox("Select user", users, format_func=lambda u: f"{u['username']} ({u['email']})")
        if selected_user:
            messages = get_messages_by_user(selected_user['id'])
            if messages:
                df = pd.DataFrame(messages, columns=["Role", "Content", "Timestamp"])
                render_styled_table(df, timestamp_cols=['Timestamp'])
            else:
                st.info("No messages for this user.")

    with tab3:
        selected_user2 = st.selectbox("Select user for moods", users, format_func=lambda u: f"{u['username']} ({u['email']})", key="mood")
        if selected_user2:
            moods = get_moods_by_user(selected_user2['id'])
            if moods:
                df = pd.DataFrame(moods, columns=["Mood", "Timestamp"])
                render_styled_table(df, timestamp_cols=['Timestamp'])
            else:
                st.info("No mood logs for this user.")

    with tab4:
        selected_user3 = st.selectbox("Select user for journals", users, format_func=lambda u: f"{u['username']} ({u['email']})", key="journal")
        if selected_user3:
            journals = get_journals_by_user(selected_user3['id'])
            if journals:
                df = pd.DataFrame(journals, columns=["Entry", "Timestamp"])
                render_styled_table(df, timestamp_cols=['Timestamp'])
            else:
                st.info("No journal entries for this user.")
    with tab5:
        st.markdown("<h3 style='color:#E5E7EB;font-family:Inter,sans-serif;font-weight:700;margin-bottom:0.25rem'>📊 Detailed User Activity Timeline</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9CA3AF;font-family:Inter,sans-serif;font-size:0.88rem;margin-top:0'>Shows every action users perform across the platform</p>", unsafe_allow_html=True)        
        selected_user_activity = st.selectbox(
            "Select user to view activity log", 
            users, 
            format_func=lambda u: f"{u['username']} ({u['email']})",
            key="activity_log"
        )
        
        if selected_user_activity:
            activities = get_user_activity_log(selected_user_activity['id'])
            
            if activities:
                activity_data = []
                for action_type, page_name, details, timestamp in activities:
                    # Format details nicely
                    details_display = details if details and details.strip() else "—"
                    activity_data.append({
                        'Action': action_type,
                        'Page': page_name,
                        'Details': details_display,
                        'Timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown"
                    })
                activity_df = pd.DataFrame(activity_data)
                render_styled_table(activity_df, timestamp_cols=['Timestamp'])
                
                # Add summary stats
                st.markdown("<h3 style='color:#E5E7EB;font-family:Inter,sans-serif;font-weight:700;margin-top:1.5rem'>📈 Activity Summary</h3>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    total_actions = len(activities)
                    st.metric("Total Actions", total_actions)
                with col2:
                    unique_pages = len(set(a[1] for a in activities))
                    st.metric("Pages Visited", unique_pages)
                with col3:
                    # Most common action
                    from collections import Counter
                    actions = [a[0] for a in activities]
                    most_common = Counter(actions).most_common(1)
                    if most_common:
                        st.metric("Most Frequent Action", most_common[0][0])
            else:
                st.markdown("<p style='color:#9CA3AF;font-family:Inter,sans-serif;font-size:0.88rem'>📭 No detailed activity logs yet. Activities will appear as users interact with the platform.</p>", unsafe_allow_html=True)
    # Back button with better spacing
    st.markdown("""
    <div style="margin-top: 3rem; text-align: center;">
        <div class="back-button-wrapper">
    """, unsafe_allow_html=True)
    if st.button("🔙 Back to Main App", key="admin_back"):
        st.session_state.page = "landing"
        st.session_state.user = None
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_admin_panel()