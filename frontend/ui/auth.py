import streamlit as st
import re
from .email_utils import send_reset_email
from db import add_user, check_login, get_user_by_email, create_reset_token, reset_password_with_code

def show_auth_page():
    # ✅ If already logged in, go to dashboard immediately
    if st.session_state.get("user") is not None:
        st.session_state.page = "dashboard"
        st.session_state.current_page = "Dashboard"
        st.rerun()
        return

    # ================= BACK TO HOME BUTTON =================
    st.markdown("""
    <style>
    .back-home-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    .back-home-btn button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="back-home-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state.page = "landing"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= STYLES =================
    st.markdown("""
<style>
/* Background Animation */
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

/* Container Spacing */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Image Animations */
@keyframes slideFromLeft {
    0% { transform: translateX(-100px); opacity: 0; }
    100% { transform: translateX(0); opacity: 1; }
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

.doctor-img img {
    width: 95px;
    height: auto;
}

/* Typography */
h1 { color: #1e293b !important; font-size: 1.8rem !important; text-align: center; }
p { color: #475569 !important; font-size: 1rem !important; text-align: center; }

/* INPUT BOX UNIFORMITY */
/* This ensures both Text and Password inputs look identical */
div[data-testid="stTextInput"] > div[data-testid="stTextInputRootElement"] {
    border-radius: 12px !important;
    border: 1.5px solid #cbd5e1 !important;
    background-color: #f8fafc !important;
    padding: 2px !important;
    transition: all 0.3s ease;
}

/* Focus State - Black Border */
div[data-testid="stTextInput"] > div[data-testid="stTextInputRootElement"]:focus-within {
    border: 2px solid #000000 !important;
    background-color: #ffffff !important;
    box-shadow: none !important;
}

/* Internal Input Styling */
.stTextInput input {
    background-color: transparent !important;
    border: none !important;
    padding: 12px !important;
    font-size: 1rem !important;
    color: #1e293b !important;
}

/* Hide Streamlit's default red error borders to keep it clean */
.stTextInput input[aria-invalid="true"] {
    box-shadow: none !important;
    border: none !important;
}

/* PASSWORD ICON FIX */
/* Positioning the visibility toggle correctly without breaking the border */
div[data-testid="stTextInputRootElement"] button {
    background-color: transparent !important;
    border: none !important;
    color: #64748b !important;
    margin-right: 10px !important;
}

/* GLOBAL BUTTON STYLE */
div.stButton > button {
    background: linear-gradient(135deg, #B8D9FF, #6D9EEB) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-weight: 600;
    border: none;
    width: 100%;
    transition: all 0.3s ease;
    margin-top: 10px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px #4A90E2 !important;
}
</style>
""", unsafe_allow_html=True)

    # ================= CENTER LAYOUT =================
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown("""
            <div class="doctor-img">
                <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png">
            </div>
            <div style="margin-bottom:30px;">
                <h1>Welcome to Your AI Therapist</h1>
                <p>A safe space to talk, heal and grow</p>
            </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ================= LOGIN =================
        with tab_login:
            email = st.text_input("Email Address", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("Sign In", key="signin_btn"):
                user = check_login(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = "Dashboard"
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("🔐 Forgot Password?", expanded=False):
                st.markdown("#### Reset Your Password")
                reset_email_input = st.text_input("Enter your registered email", key="reset_email_widget")

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Send Reset Code", key="send_reset_btn"):
                        if reset_email_input:
                            user = get_user_by_email(reset_email_input)
                            if user:
                                token_data = create_reset_token(user['id'])
                                success, message = send_reset_email(
                                    reset_email_input,
                                    token_data['reset_code'],
                                    user['username']
                                )
                                if success:
                                    st.success("✅ Reset code sent!")
                                    st.session_state['reset_email_for_verification'] = reset_email_input
                                else:
                                    st.error(message)
                with c2:
                    if st.button("I have a code", key="have_code_btn"):
                        st.session_state['show_reset_form'] = True
            # ================= RESET PASSWORD FORM =================
            if st.session_state.get('show_reset_form', False):
                st.markdown("---")
                st.markdown("#### Enter Reset Code")
                
                reset_code = st.text_input("6-digit reset code", key="reset_code_input",
                                        placeholder="123456", max_chars=6)
                new_password = st.text_input("New password", type="password", 
                                            key="reset_new_password")
                confirm_password = st.text_input("Confirm new password", type="password",
                                                key="reset_confirm_password")
                
                if st.button("Reset Password", key="reset_password_btn", use_container_width=True):
                    if reset_code and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("❌ Passwords don't match")
                        elif len(new_password) < 8:
                            st.error("❌ Password must be at least 8 characters")
                        else:
                            # Reset password
                            reset_email = st.session_state.get('reset_email_for_verification', '')
                            success, message = reset_password_with_code(
                                reset_email, reset_code, new_password
                            )
                            if success:
                                st.success("✅ Password reset successfully! Please login.")
                                # Clear reset state
                                st.session_state['show_reset_form'] = False
                                st.session_state['reset_emaill_for_verification'] = ''
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ Please fill all fields")
                
                if st.button("Cancel", key="cancel_reset_btn"):
                    st.session_state['show_reset_form'] = False
                    st.rerun()   

        # ================= SIGNUP =================
        with tab_signup:
            name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
            reg_email = st.text_input("Email", key="reg_email", placeholder="example@mail.com")
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a strong password")

            def is_valid_email(email):
                return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

            if st.button("Create Account", key="signup_btn"):
                if name and reg_email and reg_password:
                    if not is_valid_email(reg_email):
                        st.warning("Invalid email format")
                    else:
                        success, message = add_user(name, reg_email, reg_password)
                        if success:
                            st.success("Account created successfully! You can now login.")
                        else:
                            st.error(message)

if __name__ == "__main__":
    show_auth_page()