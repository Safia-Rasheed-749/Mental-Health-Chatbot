# components/navbar.py — brand + nav scoped so primary CTAs elsewhere stay blue
import streamlit as st

def render_navbar():
    st.markdown("""
    <style>
        :root {
            --mc-text: #0f172a;
            --mc-muted: #64748b;
            --mc-accent: #7c3aed;
            --mc-surface: rgba(255,255,255,0.92);
            --mc-border: rgba(15,23,42,0.10);
        }
        .nav-container {
            background: var(--mc-surface) !important;
            border: 1px solid var(--mc-border) !important;
            padding: 12px 22px !important;
            border-radius: 999px !important;
            box-shadow: 0 12px 40px rgba(15, 23, 42, 0.08) !important;
            margin: 4px 0 22px 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
            backdrop-filter: blur(14px);
        }
        /* Brand row — MindCare + AI (scoped inside .logo) */
        .logo {
            display: flex;
            align-items: center;
            gap: 14px;
            line-height: 1;
        }

        .logo-icon {
            width: 46px;
            height: 46px;
            border-radius: 50%;
            background: linear-gradient(145deg, #7c3aed 0%, #6366f1 55%, #8b5cf6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 2px solid rgba(255,255,255,0.45);
            box-shadow:
                0 0 0 4px rgba(124, 58, 237, 0.12),
                0 6px 18px rgba(124, 58, 237, 0.28);
            animation: mcLogoPulse 3s ease-in-out infinite;
        }
        @keyframes mcLogoPulse {
            0%, 100% {
                box-shadow:
                    0 0 0 4px rgba(124, 58, 237, 0.12),
                    0 6px 18px rgba(124, 58, 237, 0.28);
                transform: scale(1);
            }
            50% {
                box-shadow:
                    0 0 0 8px rgba(124, 58, 237, 0.08),
                    0 8px 26px rgba(124, 58, 237, 0.42);
                transform: scale(1.04);
            }
        }

        .logo-wordmark {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 2px;
        }
        .logo-wordmark-line {
            display: flex;
            align-items: baseline;
            gap: 4px;
        }
        .logo-wordmark-main {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 1.5rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            color: #0f172a;
        }
        .logo-wordmark-ai {
            font-size: 1.5rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .logo-wordmark-tag {
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: #64748b;
        }

        /* ONLY nav row that contains the brand logo (not hero / forms) */
        [data-testid="stHorizontalBlock"]:has(div.logo) div[data-testid="column"] button {
            padding: 6px 14px !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        [data-testid="stHorizontalBlock"]:has(div.logo) div.stButton > button {
            all: unset !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: rgba(255,255,255,0.96) !important;
            color: var(--mc-text) !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            border-radius: 999px !important;
            font-size: 14px !important;
            transition: background 0.2s ease, transform 0.2s ease !important;
            border: 1px solid var(--mc-border) !important;
            box-shadow: 0 2px 10px rgba(15,23,42,0.05) !important;
            width: auto !important;
            cursor: pointer !important;
            white-space: nowrap !important;
            margin: 0 6px !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) div.stButton > button:hover {
            background: rgba(124, 58, 237, 0.08) !important;
            transform: translateY(-1px) !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) button[key^="nav_getstarted"] {
            background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: none !important;
            box-shadow: 0 6px 18px rgba(124, 58, 237, 0.35) !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) button[key^="nav_getstarted"]:hover {
            filter: brightness(1.06) !important;
            transform: translateY(-2px) !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) button[key^="nav_games"] {
            background: rgba(16, 185, 129, 0.12) !important;
            color: #047857 !important;
            -webkit-text-fill-color: #047857 !important;
            border: 1px solid rgba(16, 185, 129, 0.28) !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) button[key^="nav_games"]:hover {
            background: rgba(16, 185, 129, 0.2) !important;
        }
        [data-testid="stHorizontalBlock"]:has(div.logo) .stColumn {
            display: flex;
            justify-content: center;
        }
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                text-align: center;
                border-radius: 20px !important;
            }
            .logo-wordmark { align-items: center; }
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("""
        <div class="logo">
            <div class="logo-icon">🧠</div>
            <div class="logo-wordmark">
                <div class="logo-wordmark-line">
                    <span class="logo-wordmark-main">MindCare</span><span class="logo-wordmark-ai">AI</span>
                </div>
                <span class="logo-wordmark-tag">mental wellness</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
        with nav_col1:
            if st.button("🏠 Home", key="nav_home_shared", type="secondary"):
                st.session_state.page = "landing"
                st.session_state["_games_nav_trigger"] = None
                st.rerun()
        with nav_col2:
            if st.button("📖 About", key="nav_about_shared", type="secondary"):
                st.session_state.page = "about"
                st.session_state["_games_nav_trigger"] = None
                st.rerun()
        with nav_col3:
            if st.button("Exercises", key="nav_demo_shared", type="secondary"):
                st.session_state.page = "exercises"
                st.session_state["_games_nav_trigger"] = None
                st.rerun()
        with nav_col4:
            if st.button("🎮 Games", key="nav_games_shared", type="secondary"):
                st.session_state.page = "games"
                st.session_state["_games_nav_trigger"] = None
                st.rerun()
        with nav_col5:
            if st.button("🚀 Get Started", key="nav_getstarted_shared", type="secondary"):
                st.session_state.page = "auth"
                st.session_state["_games_nav_trigger"] = None
                st.rerun()
