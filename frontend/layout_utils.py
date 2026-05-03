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

            /* Main content CTAs — primary = blue (navbar uses secondary + :has(logo) overrides) */
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 14px !important;
                font-weight: 800 !important;
                font-family: var(--mc-font) !important;
                box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35) !important;
                transition: filter 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            .stButton > button[kind="primary"]:hover {
                filter: brightness(1.05) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 28px rgba(37, 99, 235, 0.4) !important;
            }
            .stButton > button[kind="secondary"] {
                border-radius: 14px !important;
                font-weight: 700 !important;
                font-family: var(--mc-font) !important;
            }

            /* Inputs */
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextInput"] > div input{
                border-radius: 14px !important;
                background-color: #ffffff !important;
                color: var(--mc-text) !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
                font-family: var(--mc-font) !important;
            }

            /* Selectbox / textarea */
            div[data-baseweb="select"]{
                background: #ffffff !important;
                border-radius: 14px !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
            }
            div[data-testid="stTextArea"] textarea{
                background: #ffffff !important;
                color: var(--mc-text) !important;
                border-radius: 14px !important;
                border: 1.5px solid rgba(15,23,42,0.14) !important;
            }

            /* Page transition on navigation / rerun */
            .main .block-container {
                animation: mcPageIn 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
            }
            @keyframes mcPageIn {
                from {
                    opacity: 0.94;
                    transform: translateY(5px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )