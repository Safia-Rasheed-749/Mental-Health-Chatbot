import streamlit as st
from db import add_journal, get_journals
from datetime import datetime
from layout_utils import apply_clean_layout

def show_journal(user_id):
    apply_clean_layout(hide_header_completely=False)

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* FIX STREAMLIT TOP SPACE (IMPORTANT) */
    .block-container {
        padding-top: 1rem !important;   /* 🔥 MOVES EVERYTHING UP */
        padding-bottom: 2rem;
    }

    .main {
        background: linear-gradient(135deg, #e3f2fd, #fce4ec);
    }

    /* TITLE (LESS GAP ABOVE + BELOW) */
    .journal-title {
        text-align: center;
        font-weight: 600;
        font-size: 34px;
        color: #1e293b;
        margin-top: 0px;
        margin-bottom: 20px;   /* reduced */
    }

    /* INFO CARD (soft but visible) */
    .info-section {
        background: #eaf4ff;
        padding: 24px;
        border-radius: 18px;
        margin-bottom: 25px;
        border: 1px solid #cfe3ff;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    }

    .info-section h4 {
        font-weight: 600;
        margin-bottom: 10px;
        color: #1e293b;
    }

    .info-section p {
        color: #475569;
        font-size: 15px;
        line-height: 1.7;
    }

    /* CLEAN NOTEBOOK (FIXED DISTORTION) */
    .notebook-container {
        background: #fffef7;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    /* REMOVE HEAVY EFFECT THAT CAUSED VISUAL BUG */
    .notebook-lines {
        background: transparent;
        padding: 0;
    }

    /* TEXT AREA CLEAN */
    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        line-height: 28px !important;
        color: #1e293b !important;
        padding: 12px !important;
    }

    textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* BUTTON SPACING FIX */
    .button-container {
        margin-top: 15px;
        margin-bottom: 35px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #4facfe, #00c6ff);
        color: white;
        border-radius: 12px;
        padding: 11px 30px;
        border: none;
        font-weight: 500;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.12);
    }

    /* ENTRIES */
    .entries-title {
        margin-top: 10px;
        margin-bottom: 18px;
        font-weight: 600;
        color: #1e293b;
    }

    .journal-entry {
        background: #ffffff;
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        font-size: 14.5px;
        color: #334155;
        line-height: 1.6;
    }

    </style>
    """, unsafe_allow_html=True)

    # 📝 TITLE
    st.markdown("<h1 class='journal-title'>📓 My Personal Journal</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # 🧠 INFO SECTION
    st.markdown("""
    <div class='info-section'>
        <h4>💭 The power of journaling</h4>
        <p>
        Journaling helps you slow down your thoughts and understand your emotions more clearly.
        </p>
        <p>
        This process—known as <b>catharsis</b>—helps release emotional tension, reduce stress,
        and bring clarity to your mind.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 📓 NOTEBOOK INPUT
    st.markdown("<div class='notebook-container'>", unsafe_allow_html=True)

    st.markdown("### 🧠 What's on your mind today?")
    entry = st.text_area("", placeholder="Start writing your thoughts here...", height=200)

    st.markdown("</div>", unsafe_allow_html=True)

    # 🔘 BUTTON
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    save_clicked = st.button("💾 Save Entry", key="save_journal")
    st.markdown("</div>", unsafe_allow_html=True)

    # 💾 LOGIC
    if 'last_journal' not in st.session_state:
        st.session_state['last_journal'] = None

    if save_clicked:
        if entry.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_entry = f"[{timestamp}] {entry.strip()}"
            add_journal(user_id, full_entry)
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

    # 📜 ENTRIES
    if journals:
        st.markdown("<h3 class='entries-title'>📜 Recent Entries</h3>", unsafe_allow_html=True)
        for j in reversed(journals[-5:]):
            st.markdown(f"<div class='journal-entry'>{j}</div>", unsafe_allow_html=True)
    else:
        st.info("You have no journal entries yet. Start writing above!")