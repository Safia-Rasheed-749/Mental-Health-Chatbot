import streamlit as st
from db import add_user, check_login

def show_auth_page():

    # ================= MASTER CSS: NO SIDE BOXES, PURE CENTERING =================
    st.markdown("""
    <style>
    /* 1. Page Background */
    .stApp {
        background: linear-gradient(135deg, #a6b8ff 0%, #c4aaff 100%) !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 2. THE FIX: Center the main container and hide Streamlit's default column borders */
    [data-testid="stMainViewContainer"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 3. Target the Vertical Block to be the ONLY card on screen */
    [data-testid="stVerticalBlock"] > div:has(div.auth-card-wrapper) {
        background: rgba(255, 255, 255, 0.18) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        padding: 50px 40px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        width: 450px !important; /* Fixed width for professional look */
        margin: 40px auto !important;
    }

    /* Remove gaps between elements inside the card */
    [data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }

    /* 4. Inputs, Tabs, and Buttons */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
    }
    
    label { color: white !important; font-weight: 500 !important; }

    .stTabs [data-baseweb="tab-highlight"] { background-color: #00f2fe !important; }
    .stTabs [data-baseweb="tab"] { color: rgba(255, 255, 255, 0.7) !important; font-weight: 700; }
    .stTabs [aria-selected="true"] { color: white !important; }

    div.stButton > button {
        background: linear-gradient(90deg, #60a5fa 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 50px !important;
        width: 100% !important;
        margin-top: 20px;
    }

    /* Social Section */
    .social-row { display: flex; justify-content: space-between; gap: 10px; margin-top: 25px; }
    .social-btn {
        flex: 1; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px; padding: 10px; color: white; font-size: 0.85rem;
        display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= PAGE CONTENT =================

    # NO MORE COLUMNS - Just a direct container
    st.markdown('<div class="auth-card-wrapper"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: center; color: white; margin-bottom: 20px;">
            <h1 style="font-size:2.4rem; font-weight:900; margin-bottom:0; letter-spacing:-1px;">MindCare AI</h1>
            <p style="opacity:0.8; font-size:0.95rem;">Empowering Your Mental Wellness</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Email Address", key="login_email")
        pw = st.text_input("Password", type="password", key="login_pw")
        
        if st.button("Sign In", key="signin_btn"):
            user = check_login(email, pw)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid Login Credentials")

    with tab_signup:
        st.markdown("<br>", unsafe_allow_html=True)
        name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pw = st.text_input("Password", type="password", key="reg_pw")

        if st.button("Create Account", key="signup_btn"):
            if name and reg_email and reg_pw:
                add_user(name, reg_email, reg_pw)
                st.success("Registration Successful!")
            else:
                st.warning("Please fill all fields.")

    # Social Section
    st.markdown('<p style="margin: 20px 0 10px 0; color: rgba(255,255,255,0.5); font-size: 0.75rem; text-align:center;">OR CONTINUE WITH</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="social-row">
            <div class="social-btn">
                <img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png" width="16px"> Google
            </div>
            <div class="social-btn">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="16px" style="filter: invert(1);"> GitHub
            </div>
        </div>
        <p style="text-align:center; margin-top:25px; font-size:0.8rem; color:rgba(255,255,255,0.7);">
            Need help? <span style="color:#00f2fe; font-weight:bold;">Contact Support</span>
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_auth_page()