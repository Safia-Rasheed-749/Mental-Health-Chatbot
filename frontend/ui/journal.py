import streamlit as st
from db import add_journal, get_journals, log_user_activity
from datetime import datetime
from layout_utils import apply_clean_layout

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
    st.markdown("""
    <div class='info-card'>
        <h4>💭 The Power of Journaling</h4>
        <p>
        Journaling helps you slow down your thoughts and understand your emotions more clearly.
        This process—known as <b>catharsis</b>—helps release emotional tension, reduce stress,
        and bring clarity to your mind.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── JOURNAL INPUT CARD ──
    
    st.markdown("<div class='section-title'>🧠 What's on your mind today?</div>", unsafe_allow_html=True)
    
    entry = st.text_area("", placeholder="Start writing your thoughts here...", height=200, label_visibility="collapsed")

    st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
    save_clicked = st.button("💾 Save Entry", key="save_journal")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── SAVE LOGIC ──
    if 'last_journal' not in st.session_state:
        st.session_state['last_journal'] = None

    if save_clicked:
        if entry.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_entry = f"[{timestamp}] {entry.strip()}"
            add_journal(user_id, full_entry)
            try:
                log_user_activity(
                    user_id,
                    "Write Journal",
                    "Journal",
                    f"Entry length: {len(entry)} characters"
                )
            except Exception:
                pass
            st.success("✅ Journal entry saved successfully!")
            st.session_state['last_journal'] = full_entry
        else:
            st.warning("⚠️ Cannot save empty entry.")

    journals = get_journals(user_id)

    if st.session_state.get('last_journal'):
        if journals and st.session_state['last_journal'] not in journals:
            journals.append(st.session_state['last_journal'])
        elif not journals:
            journals = [st.session_state['last_journal']]

    # ── RECENT ENTRIES ──
    if journals:
        st.markdown("<div class='entries-section'>", unsafe_allow_html=True)
        st.markdown("<div class='entries-title'>📜 Recent Entries</div>", unsafe_allow_html=True)
        for j in reversed(journals[-5:]):
            st.markdown(f"<div class='journal-entry'>{j}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("📝 You have no journal entries yet. Start writing above!")
