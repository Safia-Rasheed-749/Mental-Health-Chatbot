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
    margin: 0;
    padding: 0;
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
   Remove Streamlit's default padding and containers
   ============================= */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Remove any empty boxes */
.stVerticalBlock {
    gap: 0rem !important;
}

div[data-testid="stVerticalBlock"] > div {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* =============================
   Main Card Styling - Centered
   ============================= */


/* Doctor image container - NO BOX */
.doctor-img {
    text-align: center;
    animation: float 3s ease-in-out infinite;
    margin: 0;
    padding: 0;
    line-height: 0;  /* Remove any extra spacing */
}

.doctor-img img {
    width: 95px;
    height: auto;
    display: inline-block;
}

@keyframes slideFromLeft {
    0% {
        transform: translateX(-100px);
        opacity: 0;
    }
    100% {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

.doctor-img {
    text-align: center;
    animation: slideFromLeft 1s ease-out forwards, float 3s ease-in-out 0.8s infinite;
}
/* =============================
   Typography
   ============================= */
h1 {
    color: #1e293b !important;
    font-size: 1.8rem !important;
    margin-bottom: 5px !important;
    margin-top: 10px !important;
}

p {
    color: #475569 !important;
    font-size: 1rem !important;
    margin-bottom: 0 !important;
}

/* =============================
   Inputs
   ============================= */
.stTextInput {
    margin-bottom: 0 !important;
}

.stTextInput input {
    border-radius: 12px !important;
    padding: 12px !important;
    border: 1px solid #cbd5e1 !important;
    background-color: #f8fafc !important;
}

.stTextInput input:focus {
    border: 1px solid #4A90E2 !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

/* =============================
   Primary Button
   ============================= */
div.stButton > button {
    background: linear-gradient(135deg, #B8D9FF, #6D9EEB) !important;
    color: #fffafa !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-weight: 600;
    border: none;
    width: 100%;
    transition: all 0.3s ease;
    margin-top: 0 !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px #4A90E2 !important;
}

/* =============================
   Tabs
   ============================= */
.stTabs {
    margin-top: 20px;
}

button[data-baseweb="tab"] {
    font-weight: 600;
    color: #475569;
    font-size: 1rem;
    padding: 8px 16px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #4A90E2 !important;
}

/* =============================
   Social Buttons
   ============================= */
.social-row {
    display: flex;
    justify-content: center;
    gap: 14px;
    margin-top: 20px;
}

.social-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid #e2e8f0;
    padding: 10px 24px;
    border-radius: 12px;
    font-size: 0.9rem;
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #1E293B;
}

.social-btn img {
    width: 18px;
    height: 18px;
}

.social-btn:hover {
    background: #f8fafc;
    border-color: #4A90E2;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* =============================
   Custom Checkbox and Links
   ============================= */
.remember-forgot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    margin: 10px 0 20px 0;
}

.remember-forgot label {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #475569;
    cursor: pointer;
}

.remember-forgot input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.forgot-link {
    color: #4A90E2;
    cursor: pointer;
    font-weight: 500;
    text-decoration: none;
}

/* =============================
   Messages
   ============================= */
.error-message, .success-message, .warning-message {
    padding: 12px 16px;
    border-radius: 12px;
    margin: 1rem 0;
}

.error-message {
    background: #EF444415;
    border-left: 4px solid #EF4444;
    color: #EF4444;
}

.success-message {
    background: #10B98115;
    border-left: 4px solid #10B981;
    color: #10B981;
}

.warning-message {
    background: #F59E0B15;
    border-left: 4px solid #F59E0B;
    color: #F59E0B;
}

/* =============================
   Responsive Design
   ============================= */
@media (max-width: 768px) {
    .main-card {
        padding: 25px 15px;
    }
    
    .doctor-img img {
        width: 70px;
    }
    
    h1 {
        font-size: 1.5rem !important;
    }
    
    .social-row {
        flex-direction: column;
    }
    
    .social-btn {
        justify-content: center;
    }
    [data-testid="column"] {
        background: transparent !important;
        padding: 0 !important;
        box-shadow: none !important;
        border: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

    # ================= CENTER LAYOUT =================
    # Create three columns for centering
    col1, center_col, col2 = st.columns([1, 2, 1])

    with center_col:
        # MAIN CARD - This creates the centered box around ALL content
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        # Doctor Illustration - NO EXTRA BOX
        st.markdown("""
            <div class="doctor-img">
                <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png">
            </div>
        """, unsafe_allow_html=True)

        # Title and Subtitle - Now inside the card
        st.markdown("""
            <div style="text-align:center; margin-bottom:30px;">
                <h1>Welcome to Your AI Therapist</h1>
                <p>A safe space to talk, heal and grow</p>
            </div>
        """, unsafe_allow_html=True)

        # TABS
        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ================= LOGIN =================
        with tab_login:
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            # Remember me and Forgot password
            st.markdown("""
                <div class="remember-forgot">
                    <label>
                        <input type="checkbox"> Remember me
                    </label>
                    <span class="forgot-link">Forgot password?</span>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Sign In", key="signin_btn", ):
                user = check_login(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.markdown("""
                        <div class="error-message">
                            ❌ Invalid email or password
                        </div>
                    """, unsafe_allow_html=True)

        # ================= SIGNUP =================
        with tab_signup:
            name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if name and reg_email and reg_password:
                    add_user(name, reg_email, reg_password)
                    st.markdown("""
                        <div class="success-message">
                            ✓ Account created successfully!
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="warning-message">
                            ⚠ Please fill all fields.
                        </div>
                    """, unsafe_allow_html=True)

        # Social Login Section
        st.markdown("""
            <p style="text-align:center; margin-top:30px; color:#64748B; font-size:0.85rem;">
                or continue with
            </p>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="social-row">
                <div class="social-btn">
                    <img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png">
                    Google
                </div>
                <div class="social-btn">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" style="filter: invert(1);">
                    GitHub
                </div>
            </div>
        """, unsafe_allow_html=True)

        # CLOSE MAIN CARD
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_auth_page()