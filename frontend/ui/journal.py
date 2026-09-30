# -*- coding: utf-8 -*-
import streamlit as st
from db import add_journal, get_journals, log_user_activity
from datetime import date, datetime, time
from layout_utils import apply_clean_layout
import html
import json


def _serialize_entry(title, mood, entry_date, entry_time, content):
    payload = {
        "title": title.strip() or "Untitled reflection",
        "mood": mood,
        "created_at": datetime.combine(entry_date, entry_time).isoformat(timespec="minutes"),
        "content": content.strip(),
    }
    return "JOURNAL_V1:" + json.dumps(payload, ensure_ascii=False)


def _parse_entry(value):
    if value.startswith("JOURNAL_V1:"):
        try:
            return json.loads(value[len("JOURNAL_V1:"):])
        except (json.JSONDecodeError, TypeError):
            pass
    title, created_at, content = "Journal reflection", "Date not available", value
    if value.startswith("[") and "]" in value:
        raw_date, content = value[1:].split("]", 1)
        try:
            created_at = datetime.fromisoformat(raw_date).strftime("%b %d, %Y · %I:%M %p")
        except ValueError:
            created_at = raw_date
        content = content.strip()
    return {"title": title, "mood": "Not tagged", "created_at": created_at, "content": content}

def show_journal(user_id):
    apply_clean_layout(hide_header_completely=False)

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── HIDE CLUTTER ── */
    .stDeployButton { display: none !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu       { visibility: hidden !important; }
    footer          { visibility: hidden !important; }
    header {
        background: transparent !important;
        box-shadow: none !important;
        visibility: visible !important;
    }

    /* ── PAGE BACKGROUND (SAME AS CHAT) ── */
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 45%, #F5F3FF 100%) !important;
        height: 100%;
    }

    /* ── BLOCK CONTAINER ── */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }

    /* ── HEADER BANNER (SAME AS CHAT) ── */
    .page-header {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        padding: 18px 28px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 24px rgba(91,141,239,0.28);
        border-radius: 20px;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    .page-header-avatar {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        border: 2px solid rgba(255,255,255,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.12);
        animation: headerPulse 3s ease-in-out infinite;
    }
    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(255,255,255,0.12); }
        50%       { box-shadow: 0 0 0 8px rgba(255,255,255,0.06); }
    }
    .page-header-text h1 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    .page-header-text p {
        margin: 2px 0 0;
        font-size: 18px;
        color: rgba(255,255,255,0.78);
        font-weight: 400;
    }
     /* card background color*/
    /* ── INFO CARD ── */
    .info-card {
        background: rgba(255,255,255,0.92);
        border-left: 4px solid #5B8DEF;
        padding: 20px 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(148,163,184,0.12);
        box-shadow: 0 4px 18px rgba(15,23,42,0.06);
    }

    .info-card h4 {
        font-weight: 700;
        margin-bottom: 10px;
        color: #1e293b;
        font-size: 16px;
    }

    .info-card p {
        color: #475569;
        font-size: 14px;
        line-height: 1.7;
        margin: 8px 0;
    }

   

    .journal-card:hover {
        box-shadow: 0 8px 28px rgba(99,102,241,0.15);
        transform: translateY(-2px);
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ── TEXT AREA ── */
    div[data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.95) !important;
        border: 2px solid rgba(99,102,241,0.25) !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        line-height: 1.7 !important;
        color: #1e293b !important;
        padding: 14px !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        outline: none !important;
    }

    textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* ── SAVE BUTTON ── */
    .stButton>button {
        background: linear-gradient(135deg, #5B8DEF 0%, #7C9DF5 100%);
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 16px rgba(91,141,239,0.30) !important;
        transition: all 0.2s !important;
    }

    .stButton>button:hover {
        filter: brightness(1.05) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(91,141,239,0.40) !important;
    }

    /* ── JOURNAL ENTRIES ── */
    .entries-section {
        margin-top: 32px;
    }

    .entries-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
     /*recent entries background color*/
    .journal-entry {
        background: rgba(255,255,255,0.92);
        border-left: 4px solid #5B8DEF;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 4px 18px rgba(15,23,42,0.06);
        font-size: 14px;
        color: #334155;
        line-height: 1.7;
        border: 1px solid rgba(148,163,184,0.12);
        transition: all 0.3s ease;
    }

    .journal-entry:hover {
        box-shadow: 0 4px 18px rgba(99,102,241,0.12);
        transform: translateX(4px);
    }

    /* ── INFO/SUCCESS MESSAGES ── */
    .stInfo {
        background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(139,92,246,0.10)) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        border-left: 4px solid #6366f1 !important;
        color: #1e293b !important;
        font-weight: 500 !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(16,185,129,0.10), rgba(52,211,153,0.10)) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
        font-weight: 500 !important;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(245,158,11,0.10), rgba(251,146,60,0.10)) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        border-left: 4px solid #f59e0b !important;
        color: #92400e !important;
        font-weight: 500 !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar       { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }

    /* Hide Streamlit default elements that create white bars */
    .element-container:has(> .stMarkdown:empty) {
        display: none !important;
    }
    
    /* Remove extra spacing from empty elements */
    .stMarkdown:empty {
        display: none !important;
    }
    
    /* Hide empty columns */
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    /* Remove white background from empty containers */
    .stVerticalBlock:empty {
        display: none !important;
    }

    /* Force hide any white bars from Streamlit columns */
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }

    div[data-testid="column"] {
        background: transparent !important;
    }

    /* Remove padding from empty columns */
    div[data-testid="column"]:has(> div:empty) {
        display: none !important;
    }

    /* Hide element containers with only whitespace */
    .element-container:has(> div:empty) {
        display: none !important;
    }

    /* Remove default Streamlit container backgrounds */
    .stVerticalBlock {
        background: transparent !important;
    }

    .block-container > div {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HEADER BANNER ──
    st.markdown("""
    <div class="page-header">
        <div class="page-header-avatar">📓</div>
        <div class="page-header-text">
            <h1>Personal Journal</h1>
            <p>Express your thoughts and reflect on your journey</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INFO CARD ──
    journals = get_journals(user_id) or []
    write_tab, history_tab = st.tabs(["✍️ Write Entry", "📖 Past Entries"])

    with write_tab:
        with st.expander("💡 Why Journaling Helps"):
            st.markdown("Journaling helps you slow down, understand your emotions, and release stress. A few honest lines can bring clarity to your day.")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>💭 What's on your mind today?</div>", unsafe_allow_html=True)
        title_col, mood_col = st.columns([2, 1], gap="medium")
        with title_col:
            title = st.text_input("Entry title", placeholder="Give this reflection a title", key="journal_title")
        with mood_col:
            mood = st.selectbox("Associated mood", ["No tag", "Happy", "Neutral", "Sad", "Anxious", "Angry"], key="journal_mood")
        date_col, time_col = st.columns([2, 1], gap="medium")
        with date_col:
            entry_date = st.date_input("Date", value=date.today(), key="journal_date")
        with time_col:
            entry_time = st.time_input("Time", value=datetime.now().replace(second=0, microsecond=0).time(), key="journal_time")

        entry = st.text_area("Your reflection", placeholder="Start writing your thoughts here...", height=220, key="journal_content")
        st.caption(f"{len(entry)} characters · {len(entry.split())} words")
        action_spacer, action_button = st.columns([3, 1])
        with action_button:
            save_clicked = st.button("💾 Save Entry", key="save_journal", use_container_width=True)

        if save_clicked:
            if entry.strip():
                full_entry = _serialize_entry(title, mood, entry_date, entry_time, entry)
                add_journal(user_id, full_entry)
                try:
                    log_user_activity(user_id, "Write Journal", "Journal", f"Entry length: {len(entry)} characters")
                except Exception:
                    pass
                st.success("Journal entry saved successfully.")
                st.session_state["journal_content"] = ""
                st.session_state["journal_title"] = ""
                st.rerun()
            else:
                st.warning("Write a few words before saving your entry.")

    with history_tab:
        if journals:
            st.markdown(f"<div class='entries-title'>📜 Your reflections <span style='font-size:13px;color:#64748b;font-weight:500'>· {len(journals)} entries</span></div>", unsafe_allow_html=True)
            for raw_entry in reversed(journals):
                item = _parse_entry(str(raw_entry))
                safe_title = html.escape(str(item.get("title", "Untitled reflection")))
                safe_date = html.escape(str(item.get("created_at", "Date not available")))
                safe_mood = html.escape(str(item.get("mood", "Not tagged")))
                content = html.escape(str(item.get("content", "")))
                preview = content if len(content) <= 600 else content[:600].rstrip() + "…"
                mood_icons = {"Happy": "😊", "Neutral": "😐", "Sad": "😔", "Anxious": "😰", "Angry": "😡", "No tag": "🌿", "Not tagged": "🌿"}
                icon = mood_icons.get(str(item.get("mood", "")), "🌿")
                st.markdown(f"""
                <article class="journal-entry">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
                        <div><div style="font-size:17px;font-weight:700;color:#1e293b">{safe_title}</div>
                        <div style="font-size:12px;color:#64748b;margin-top:5px">{safe_date}</div></div>
                        <span style="background:#eef4ff;border-radius:20px;padding:5px 11px;font-size:12px;color:#475569">{icon} {safe_mood}</span>
                    </div>
                    <div style="white-space:pre-wrap;margin-top:14px">{preview}</div>
                </article>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:42px 20px;background:rgba(255,255,255,.8);border:1px solid rgba(148,163,184,.2);border-radius:18px;margin-top:12px">
                <div style="font-size:42px">📖</div>
                <div style="font-size:17px;font-weight:700;color:#1e293b;margin-top:10px">A little space for your thoughts</div>
                <div style="font-size:14px;color:#64748b;margin-top:6px">No journal entries recorded yet. Select “Write Entry” to begin.</div>
            </div>
            """, unsafe_allow_html=True)
