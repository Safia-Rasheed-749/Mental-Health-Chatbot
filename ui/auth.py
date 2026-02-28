import streamlit as st
from db import add_user, check_login

def show_auth_page():

    # ================= LIGHTER BACKGROUND =================
    st.markdown("""
    <style>
    /* Lighter, softer gradient background */
    .stApp {
        background: linear-gradient(135deg, #a6b8ff 0%, #c4aaff 100%) !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding-top: 80px !important;
    }

    /* Center all content */
    .center-content {
        text-align: center;
        color: white;
    }

    /* Input Styling - Softer */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #38bdf8 !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 600;
    }

    /* Buttons - Slightly Softer Cyan */
    div.stButton > button {
        background: linear-gradient(90deg, #60a5fa 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 50px !important;
        width: 100% !important;
        margin-top: 15px;
    }

    div.stButton > button:hover {
        opacity: 0.9;
    }

    /* Social Buttons Styling */
    .social-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 25px;
    }
    .social-btn {
        flex: 1;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
        color: white;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    /* Sign up link at bottom */
    .signup-text {
        margin-top: 30px;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
    }
    .signup-text span {
        color: #00f2fe;
        cursor: pointer;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= CENTER LAYOUT =================
    col1, center_col, col3 = st.columns([1, 1.6, 1])

    with center_col:

        # Headings Centered
        st.markdown(
            """
            <div class="center-content">
                <h1 style="font-size:2.6rem; font-weight:800; margin-bottom:5px;">
                    Welcome Back
                </h1>
                <p style="font-size:1.1rem; opacity:0.85; margin-bottom:40px;">
                    Sign in to your account
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ================= LOGIN =================
        with tab_login:
            email = st.text_input("Email Address", key="login_email")
            pw = st.text_input("Password", type="password", key="login_pw")

            # Optional Remember Me & Forgot Password row
            st.markdown(""" 
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin: 10px 0 20px 0; color: white;">
                    <label><input type="checkbox"> Remember me</label>
                    <a href="#" style="color: #00f2fe; text-decoration: none;">Forgot password?</a>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Sign In", key="signin_btn"):
                user = check_login(email, pw)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid Login")

        # ================= SIGN UP =================
        with tab_signup:
            name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pw = st.text_input("Password", type="password", key="reg_pw")

            if st.button("Sign Up", key="signup_btn"):
                if name and reg_email and reg_pw:
                    add_user(name, reg_email, reg_pw)
                    st.success("Account created successfully!")
                else:
                    st.warning("Please fill all fields.")

        # ================= SOCIAL LOGIN =================
        st.markdown('<p style="margin: 25px 0 15px 0; color: rgba(255,255,255,0.7); font-size: 0.8rem; text-align:center;">or continue with</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="social-row">
                <div class="social-btn">
                    <img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png" width="18px"> Google
                </div>
                <div class="social-btn">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="18px" style="filter: invert(1);"> GitHub
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ================= SIGN UP LINK =================
        st.markdown('<p class="signup-text">Don\'t have an account? <span>Sign up</span></p>', unsafe_allow_html=True)


if __name__ == "__main__":
    show_auth_page()