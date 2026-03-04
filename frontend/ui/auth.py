import streamlit as st
from db import add_user, check_login

def show_auth_page():

    # ================= LIGHTER BACKGROUND =================
    st.markdown("""
<style>

/* =============================
   Proper Animated Calm Background
   ============================= */

html, body, .stApp {
    height: 100%;
}

.stApp {
    background: linear-gradient(120deg, #ffffff, #f1f5f9, #e2e8f0, #f8fafc);
    background-size: 300% 300%;
    animation: calmMove 12s ease-in-out infinite;
}

@keyframes calmMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}


/* =============================
   Safe Card Styling (Does NOT break inputs)
   ============================= */

[data-testid="stVerticalBlock"] > div:has(.doctor-img) {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
}


/* =============================
   Typography
   ============================= */

h1, h2, h3 {
    color: #1e293b !important;
}

p {
    color: #475569 !important;
}


/* =============================
   Doctor Animation
   ============================= */

.doctor-img {
    text-align: center;
    animation: float 3s ease-in-out infinite;
    border: none;              /* Removes border */
    box-shadow: none;          /* Removes shadow if any */
    background: transparent;   /* Makes background invisible (if needed) */
}

.doctor-img img {
    width: 95px;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}


/* =============================
   Inputs
   ============================= */

.stTextInput input {
    border-radius: 12px !important;
    padding: 12px !important;
    border: 1px solid #cbd5e1 !important;
    background-color: #f8fafc !important;
}

.stTextInput input:focus {
    border: 1px solid #FF0000 !important;
    box-shadow: 0 0 0 2px rgba(255,0,0,0.08);
}


/* =============================
   Primary Button
   ============================= */

div.stButton > button {
    background-color: #FF0000 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-weight: 600;
    border: none;
}

div.stButton > button:hover {
    background-color: #CC0000 !important;
}


/* =============================
   Tabs
   ============================= */

button[data-baseweb="tab"] {
    font-weight: 600;
    color: #475569;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FF0000 !important;
}


/* =============================
   Social Buttons
   ============================= */

.social-row {
    display: flex;
    justify-content: center;
    gap: 14px;
    margin-top: 8px;
}

.social-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    border: 1px solid #e2e8f0;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    background: white;
    cursor: pointer;
    transition: 0.2s ease;
}

.social-btn img {
    width: 16px;
    height: 16px;
}

.social-btn:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

    # ================= CENTER LAYOUT =================
    col1, center_col, col3 = st.columns([1, 1.6, 1])

    with center_col:

    # OPEN CARD

        # Doctor Illustration
        st.markdown("""
            <div class="doctor-img">
                <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" width="110">
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align:center; margin-bottom:25px;">
                <h1 style="margin-bottom:5px;">Welcome to Your AI Therapist</h1>
                <p style="opacity:0.9;">A safe space to talk, heal and grow</p>
            </div>
        """, unsafe_allow_html=True)

        # TABS
        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ================= LOGIN =================
        with tab_login:
            email = st.text_input("Email Address", key="login_email")
            pw = st.text_input("Password", type="password", key="login_pw")

            st.markdown("""
            <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-top:5px;">
                <label><input type="checkbox"> Remember me</label>
                <span style="color:#FF0000;">Forgot password?</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Sign In", key="signin_btn"):
                user = check_login(email, pw)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid Login")

        # ================= SIGNUP =================
        with tab_signup:
            name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pw = st.text_input("Password", type="password", key="reg_pw")

            if st.button("Create Account", key="signup_btn"):
                if name and reg_email and reg_pw:
                    add_user(name, reg_email, reg_pw)
                    st.success("Account created successfully!")
                else:
                    st.warning("Please fill all fields.")

        # Social Section
        st.markdown(
            '<p style="text-align:center; margin-top:25px; color:rgba(255,255,255,0.8); font-size:0.85rem;">or continue with</p>',
            unsafe_allow_html=True
        )

        st.markdown("""
            <div class="social-row">
                <div class="social-btn">
                    <img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png">
                    Google
                </div>
                <div class="social-btn">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" style="filter:invert(1);">
                    GitHub
                </div>
            </div>
        """, unsafe_allow_html=True)

        # CLOSE CARD
        # st.markdown('</div>', unsafe_allow_html=True)

        

if __name__ == "__main__":
    show_auth_page()