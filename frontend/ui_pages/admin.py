import streamlit as st
import pandas as pd
from db import get_all_users, get_messages_by_user, get_moods_by_user, get_journals_by_user
from layout_utils import apply_clean_layout
from datetime import datetime

def show_admin_panel():
    apply_clean_layout(hide_header_completely=False)

    # --- CLEAN PROFESSIONAL TABLES - NO HOVER, FIXED ROWS ---
    st.markdown("""
    <style>
        /* Dark + glassy "admin panel" theme (matches your 3rd reference) */
        :root{
            --bg0:#070a17;
            --bg1:#0b1227;
            --panel:#0c1630;
            --border:rgba(148,163,184,0.18);
            --text:#e5e7eb;
            --muted:rgba(226,232,240,0.72);
            --accent:#7c3aed;   /* purple */
            --accent2:#3b82f6;  /* blue */
        }
        html, body, .stApp {
            background-color: var(--bg0) !important;
        }
        .main .block-container {
            background-color: var(--bg0) !important;
        }

        .admin-header {
            margin-top: -5rem;
            background: linear-gradient(90deg, rgba(59,130,246,0.25), rgba(124,58,237,0.35));
            border: 1px solid rgba(124,58,237,0.25);
            padding: 1.5rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 2.5rem;
            font-family: 'Segoe UI', Roboto, sans-serif;
            box-shadow: 0 18px 60px rgba(124,58,237,0.18);
            backdrop-filter: blur(10px);
        }

        .stat-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.04) 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 12px 40px rgba(0,0,0,0.35);
            border: 1px solid rgba(148,163,184,0.18);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            backdrop-filter: blur(10px);
        }
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 55px rgba(0,0,0,0.45);
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 850;
            color: #c4b5fd;
            margin-bottom: 0.5rem;
            font-family: 'Segoe UI', Roboto, sans-serif;
            text-shadow: 0 0 18px rgba(124,58,237,0.35);
        }
        .stat-label {
            font-size: 0.95rem;
            color: rgba(226,232,240,0.78);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }

        button {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.85), rgba(124, 58, 237, 0.85)) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            font-weight: 800 !important;
            padding: 12px 32px !important;
            border-radius: 14px !important;
            font-size: 1rem !important;
            box-shadow: 0 18px 45px rgba(59,130,246,0.22) !important;
        }
        button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 25px 60px rgba(124,58,237,0.25) !important;
        }
         
        /* Professional tables - dark, clean, alternating rows */
        div[data-testid="stMarkdownContainer"] table.professional-table,
        div.element-container table.professional-table,
        .professional-table,
        table.professional-table {
            width: 100% !important;
            border-collapse: collapse !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            box-shadow: 0 18px 55px rgba(0,0,0,0.35) !important;
            font-family: 'Segoe UI', Roboto, -apple-system, sans-serif !important;
            font-size: 0.95rem !important;
            background: rgba(12,22,48,0.9) !important;
            border: 1px solid rgba(148,163,184,0.18) !important;
            margin: 2rem 0 !important;
        }

        .professional-table thead th,
        .professional-table th,
        table.professional-table th {
            background: linear-gradient(90deg, rgba(59,130,246,0.85) 0%, rgba(124,58,237,0.85) 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 0.92rem !important;
            padding: 16px 18px !important;
            border: none !important;
            text-align: left !important;
            letter-spacing: 0.25px !important;
            font-family: 'Segoe UI', Roboto, sans-serif !important;
        }

        .professional-table tbody tr,
        table.professional-table tbody tr {
            border-bottom: 1px solid rgba(148,163,184,0.14) !important;
        }

        .professional-table tbody tr:nth-child(odd),
        table.professional-table tbody tr:nth-child(odd) {
            background-color: rgba(11,18,39,0.85) !important;
        }

        .professional-table tbody tr:nth-child(even),
        table.professional-table tbody tr:nth-child(even) {
            background-color: rgba(15,23,42,0.72) !important;
        }

        .professional-table tbody tr:hover,
        table.professional-table tbody tr:hover {
            background-color: inherit !important;
        }

        .professional-table td,
        table.professional-table td {
            padding: 16px 18px !important;
            color: rgba(229,231,235,0.98) !important;
            font-weight: 550 !important;
            font-size: 0.94rem !important;
            line-height: 1.5 !important;
            border: none !important;
            vertical-align: middle !important;
            font-family: 'Segoe UI', Roboto, sans-serif !important;
        }

        /* Admin column highlighting */
        .professional-table td:nth-child(4),
        table.professional-table td:nth-child(4) {
            font-weight: 750 !important;
            color: rgba(209,250,229,0.95) !important;
        }

        .professional-table td:last-child,
        table.professional-table td:last-child {
            color: rgba(147,197,253,0.9) !important;
            font-size: 0.92rem !important;
            font-family: 'Monaco', monospace !important;
        }

        /* Tabs styling (Streamlit baseweb) */
        div[role="tablist"] button[role="tab"] {
            border-radius: 999px !important;
            border: 1px solid rgba(148,163,184,0.20) !important;
            background: rgba(15,23,42,0.4) !important;
            color: rgba(226,232,240,0.85) !important;
            padding: 10px 14px !important;
            margin: 0 8px 0 0 !important;
            font-weight: 800 !important;
        }
        div[role="tablist"] button[role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(59,130,246,0.85), rgba(124,58,237,0.85)) !important;
            border-color: rgba(124,58,237,0.55) !important;
            color: #ffffff !important;
        }

        /* Tabs content spacing */
        div[data-testid="stTab"] {
            padding: 1rem 0 !important;
        }
        div[data-testid="stTab"] > div > div {
            padding-top: 1rem !important;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .professional-table td,
            .professional-table th {
                padding: 12px 14px !important;
                font-size: 0.9rem !important;
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

    tab1, tab2, tab3, tab4 = st.tabs(["👥 All Users", "💬 User Chats", "😊 User Moods", "📓 User Journals"])

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
            background: linear-gradient(145deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.03) 100%);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 18px 55px rgba(0,0,0,0.35);
            border: 1px solid rgba(148,163,184,0.18);
            backdrop-filter: blur(10px);
        ">
            {html_table}
        </div>
        ''', unsafe_allow_html=True)

    with tab1:
        users_data = []
        for u in users:
            last_active = get_last_activity(u['id'])
            users_data.append({
                'ID': u['id'],
                'Username': u['username'],
                'Email': u['email'],
                'Admin': u.get('is_admin', False),
                'Created': u.get('created_at'),
                'Last Active': last_active.strftime("%Y-%m-%d %H:%M") if last_active else "Never"
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

    # Back button with better spacing
    st.markdown("""
    <div style="margin-top: 3rem; text-align: center;">
        <div class="back-button-wrapper">
    """, unsafe_allow_html=True)
    if st.button("🔙 Back to Main App", key="admin_back"):
        st.session_state.page = "dashboard"
        st.session_state.current_page = "Dashboard"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_admin_panel()