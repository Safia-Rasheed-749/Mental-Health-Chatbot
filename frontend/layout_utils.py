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