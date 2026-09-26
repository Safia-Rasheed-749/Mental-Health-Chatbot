# layout_utils.py
import streamlit as st

def apply_clean_layout(hide_header_completely=False):
    st.markdown("""
    <style>
        /* 1. Remove ALL top padding from the main content container */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 2rem !important;
        }
        /* 2. Remove any margin from the very first element inside */
        .block-container > :first-child,
        .element-container:first-child,
        .stMarkdown:first-child,
        [data-testid="stVerticalBlock"] > :first-child {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
        }
        /* 3. Optional: Remove extra gap from nested vertical blocks (Streamlit 1.31+) */
        [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
        }
        /* 4. Keep footer hidden (optional) */
        footer, .stApp footer, [data-testid="stFooter"] {
            visibility: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_professional_design_system():
    """
    Shared CSS variables + base styling so all *non-admin* pages look consistent.
    Light, calm, professional wellness palette (admin page keeps its own dark theme).
    """
    st.markdown(
        """
        <style>
            :root{
                --mc-bg0:#f6f7fb;
                --mc-bg1:#eef2ff;
                --mc-panel:#ffffff;
                --mc-surface:#ffffff;
                --mc-border: rgba(15,23,42,0.10);
                --mc-text:#0f172a;
                --mc-muted: rgba(15,23,42,0.72);
                --mc-accent:#7c3aed;   /* purple */
                --mc-accent2:#3b82f6;  /* blue */
                --mc-accent3:#10b981;  /* green */
                --mc-radius:16px;
                --mc-shadow: 0 18px 55px rgba(15,23,42,0.10);
                --mc-font: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
            }

            /* Base page background */
            html, body, .stApp {
                background-color: var(--mc-bg0) !important;
                color: var(--mc-text) !important;
                font-family: var(--mc-font) !important;
            }

            /* Main container background (Streamlit) */
            .main .block-container {
                background-color: var(--mc-bg0) !important;
            }

            /* Readability in main column (Streamlit markdown + widgets) */
            section.main .stMarkdown,
            section.main .stMarkdown p,
            section.main [data-testid="stCaptionContainer"] {
                color: #1e293b !important;
            }
            section.main .stMarkdown p {
                font-weight: 500;
                line-height: 1.65;
            }

            /* Nice soft page surface for wide layout */
            .main .block-container > div:first-child{
                border-radius: 24px;
            }

            /* Give Streamlit tabs/pills a nicer default */
            div[role="tablist"] button[role="tab"]{
                border-radius: 999px !important;
                border: 1px solid rgba(15,23,42,0.10) !important;
                background: rgba(255,255,255,0.85) !important;
                color: rgba(15,23,42,0.70) !important;
                font-weight: 800 !important;
                padding: 10px 14px !important;
                box-shadow: 0 10px 30px rgba(15,23,42,0.06);
            }

            div[role="tablist"] button[role="tab"][aria-selected="true"]{
                background: linear-gradient(135deg, rgba(59,130,246,0.85), rgba(124,58,237,0.85)) !important;
                border-color: rgba(124,58,237,0.55) !important;
                color: #ffffff !important;
            }
          /*learn more and chatting button start game signup background and text color */
            /* Main content CTAs — primary = blue (navbar uses secondary + :has(logo) overrides) */
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 14px !important;
                font-weight: 800 !important;
                font-family: var(--mc-font) !important;
                box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35) !important;
            }
            .stButton > button[kind="primary"]:hover {
                filter: brightness(1.05) !important;
                box-shadow: 0 12px 32px rgba(37, 99, 235, 0.45) !important;
            }
            .stButton > button[kind="secondary"] {
                border-radius: 14px !important;
                font-weight: 700 !important;
                font-family: var(--mc-font) !important;
            }
            

            /* Inputs fields of auth page */
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextInput"] > div input{
                border-radius: 14px !important;
                background-color: #ffffff !important;
                color: var(--mc-text) !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
                font-family: var(--mc-font) !important;
            }
            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stTextInput"] > div input:focus{
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            }

            /* Selectbox / textarea */
            div[data-baseweb="select"]{
                background: #ffffff !important;
                border-radius: 14px !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
            }
            div[data-baseweb="select"]:hover{
                border-color: #3b82f6 !important;
            }
            div[data-testid="stTextArea"] textarea{
                background: #ffffff !important;
                color: var(--mc-text) !important;
                border-radius: 14px !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
            }
            div[data-testid="stTextArea"] textarea:focus{
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            }

            /* =============================================================
               MindCare shared UI system
               Keep this layer intentionally widget-oriented. Streamlit's
               internal class names change between releases; data-testid and
               semantic roles are the most stable selectors available.
            ============================================================= */
            .main .block-container {
                width: min(100%, 1440px) !important;
                margin: 0 auto !important;
                padding-left: clamp(1rem, 3vw, 3.5rem) !important;
                padding-right: clamp(1rem, 3vw, 3.5rem) !important;
                padding-bottom: 4rem !important;
            }

            /* Consistent Streamlit widget rhythm */
            [data-testid="stVerticalBlock"] { gap: 0.65rem; }
            [data-testid="stHorizontalBlock"] { align-items: stretch; }
            [data-testid="stMetric"] {
                background: var(--mc-panel) !important;
                border: 1px solid var(--mc-border) !important;
                border-radius: var(--mc-radius) !important;
                padding: 1rem 1.1rem !important;
                box-shadow: 0 8px 24px rgba(15,23,42,0.05) !important;
            }
            [data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 700 !important; }
            [data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800 !important; }

            .stButton > button, .stDownloadButton > button {
                min-height: 42px !important;
                padding: 0.55rem 1rem !important;
                border-radius: 12px !important;
                font-weight: 750 !important;
                letter-spacing: 0.01em !important;
                transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease !important;
            }
            .stButton > button:hover, .stDownloadButton > button:hover {
                transform: translateY(-1px) !important;
                filter: brightness(1.03) !important;
            }
            .stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
            input:focus-visible, textarea:focus-visible {
                outline: 3px solid rgba(99,102,241,0.28) !important;
                outline-offset: 2px !important;
            }

            /* Labels remain visible and readable on non-authenticated forms. */
            [data-testid="stTextInput"] label,
            [data-testid="stTextArea"] label,
            [data-testid="stSelectbox"] label,
            [data-testid="stDateInput"] label,
            [data-testid="stFileUploader"] label {
                color: #334155 !important;
                font-weight: 700 !important;
                font-size: 0.88rem !important;
            }
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-baseweb="select"] > div {
                min-height: 44px !important;
                box-sizing: border-box !important;
            }

            /* Alerts, expanders and tables share the same surface language. */
            [data-testid="stAlert"] {
                border-radius: 14px !important;
                border: 1px solid rgba(99,102,241,0.16) !important;
            }
            [data-testid="stExpander"] {
                background: rgba(255,255,255,0.82) !important;
                border: 1px solid var(--mc-border) !important;
                border-radius: 14px !important;
                overflow: hidden !important;
            }
            [data-testid="stDataFrame"] {
                border: 1px solid var(--mc-border) !important;
                border-radius: 14px !important;
                overflow: hidden !important;
                box-shadow: 0 8px 24px rgba(15,23,42,0.05) !important;
            }
            [data-testid="stPlotlyChart"], [data-testid="stArrowVegaLiteChart"] {
                background: var(--mc-panel) !important;
                border: 1px solid var(--mc-border) !important;
                border-radius: var(--mc-radius) !important;
                padding: 0.5rem !important;
                box-shadow: 0 8px 24px rgba(15,23,42,0.04) !important;
            }

            /* Comfortable sidebar on desktop, full-width navigation on mobile. */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f8faff 0%, #f1f0ff 100%) !important;
                border-right: 1px solid rgba(99,102,241,0.14) !important;
            }
            section[data-testid="stSidebar"] [data-testid="stButton"] button {
                text-align: left !important;
                justify-content: flex-start !important;
            }

            @media (max-width: 900px) {
                .main .block-container { padding-top: 1.5rem !important; }
                [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
                [data-testid="stMetric"] { min-width: 160px !important; }
            }
            @media (max-width: 640px) {
                .main .block-container {
                    padding-left: 0.8rem !important;
                    padding-right: 0.8rem !important;
                }
                .stButton > button, .stDownloadButton > button { width: 100% !important; }
                [data-testid="stMetric"] { width: 100% !important; }
            }
            
        </style>
        """,
        unsafe_allow_html=True
    )
