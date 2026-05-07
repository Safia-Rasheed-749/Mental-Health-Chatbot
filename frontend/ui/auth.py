import streamlit as st
import re
from db import add_user, check_login, get_user_by_email, create_reset_token, reset_password_with_code
from ui.email_utils import send_reset_email

def show_auth_page():
    # If already logged in, redirect based on user type
    if st.session_state.get("user") is not None:
        user = st.session_state.user
        is_admin = len(user) > 3 and user[3]
        if is_admin:
            st.session_state.page = "admin_panel"
            st.session_state.current_page = "Admin Panel"
        else:
            st.session_state.page = "dashboard"
            st.session_state.current_page = "Dashboard"
        st.rerun()
        return

    # Initialize state for page switching (Login, Signup, Forgot Password)
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'

    # ===== PROFESSIONAL AUTH PAGE STYLING =====
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Hide Streamlit default headers & footers */
    header, footer, .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden; }

    /* Clean White Background */
    .stApp { 
        background: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    .main .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important;
        max-width: 1000px;
        overflow-y: hidden !important;
    }
    .block-container{
        padding-top: 1rem !important; 

                }
    
    /* Disable auto-scroll */
    section[data-testid="stAppViewContainer"] {
        overflow-y: auto !important;
    }

    /* =========================================
       PROFESSIONAL AUTH CARD
       ========================================= */
    [data-testid="column"]:nth-child(2) {
        background: #ffffff !important;
        border-radius: 20px !important;
        padding: 2.5rem 3rem 3rem 3rem !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(0, 0, 0, 0.05) inset !important;
        border: 1px solid #e5e7eb !important;
        animation: slideUp 0.5s ease-out;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Header text alignment */
    .auth-header { 
        text-align: center; 
        margin-bottom: 1.5rem;
        margin-top: 2rem;
    }
    .auth-header h1 { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem !important; 
        font-weight: 800 !important; 
        margin-bottom: 0.5rem !important; 
        padding-bottom: 0;
        letter-spacing: -0.5px;
    }
    .auth-header p { 
        color: #64748B !important; 
        font-size: 0.95rem !important; 
        margin-top: 0 !important;
        font-weight: 400;
    }

    /* =========================================
       ENHANCED INPUT FIELDS (Single Border)
       ========================================= */
    .stTextInput label { 
        font-size: 0.875rem !important; 
        color: #1e293b !important; 
        font-weight: 600 !important; 
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Remove Streamlit's default input wrapper border */
    div[data-testid="stTextInput"] > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }
    
    div[data-testid="stTextInputRootElement"] {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 14px !important;
        background-color: #f8fafc !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stTextInputRootElement"]:focus-within {
        border-color: #667eea !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        transform: translateY(-1px);
    }
    
    input {
        color: #0F172A !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        border: none !important;
        background: transparent !important;
    }
    
    input::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }

    /* =========================================
       MODERN BUTTON STYLES
       ========================================= */
    
    /* Primary Button with Gradient */
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #FFFFFF !important;
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        margin-top: 1rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        letter-spacing: 0.3px;
    }
    
    button[kind="primary"]:hover { 
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    /* Tertiary Link Button */
    button[kind="tertiary"] {
        background-color: transparent !important;
        color: #667eea !important;
        width: 100% !important;
        border: none !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        margin-top: 0.75rem !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="tertiary"]:hover { 
        color: #764ba2 !important;
        background-color: rgba(102, 126, 234, 0.05) !important;
        border-radius: 8px !important;
    }

    /* Forgot Password Link Styling */
    .forgot-password-link {
        text-align: right;
        margin-top: -8px;
        margin-bottom: 8px;
    }
    
    .forgot-password-link button {
        font-size: 0.85rem !important;
        color: #667eea !important;
        padding: 0.25rem 0.5rem !important;
        width: auto !important;
        float: right;
    }

    /* Divider with text */
    .divider-container {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
    }
    
    .divider-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, transparent, #e2e8f0, transparent);
    }
    
    .divider-text {
        padding: 0 1rem;
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Success/Error Messages */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
        padding: 1rem !important;
        margin-top: 1rem !important;
    }
    
    /* Loading State */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        [data-testid="column"]:nth-child(2) {
            padding: 2rem 1.5rem !important;
        }
        
        .auth-header h1 {
            font-size: 1.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 3-Column Layout to center the Card perfectly
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        
        # ==================== VIEW 1: LOGIN ====================
        if st.session_state.auth_mode == 'login':
            st.markdown("""
                <div class="auth-header">
                    <h1>Welcome Back</h1>
                    <p>Enter your details to sign in to your account.</p>
                </div>
            """, unsafe_allow_html=True)

            email = st.text_input("Email", key="login_email", placeholder="name@example.com")
            password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")

            # Forgot Password small link just under password
            st.markdown("<div class='forgot-password-link'>", unsafe_allow_html=True)
            if st.button("Forgot password?", key="go_forgot", type="tertiary"):
                st.session_state.auth_mode = 'forgot_password'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            # Main Full-width Login Button
            if st.button("Sign In", key="signin_btn", type="primary", use_container_width=True):
                user = check_login(email, password)
                if user:
                    st.session_state.user = user
                    is_admin = len(user) > 3 and user[3]
                    if is_admin:
                        st.session_state.current_page = "Admin Panel"
                        st.session_state.page = "admin_panel"
                    else:
                        st.session_state.current_page = "Dashboard"
                        st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

            # Divider
            st.markdown("""
                <div class="divider-container">
                    <div class="divider-line"></div>
                    <div class="divider-text">or</div>
                    <div class="divider-line"></div>
                </div>
            """, unsafe_allow_html=True)

            # Switch to Sign Up text
            if st.button("Don't have an account? Sign up", key="go_signup", type="tertiary", use_container_width=True):
                st.session_state.auth_mode = 'signup'
                st.rerun()

        # ==================== VIEW 2: SIGN UP ====================
        elif st.session_state.auth_mode == 'signup':
            st.markdown("""
                <div class="auth-header">
                    <h1>Create an Account</h1>
                    <p>Join us and start your secure therapy journey.</p>
                </div>
            """, unsafe_allow_html=True)

            name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
            reg_email = st.text_input("Email", key="reg_email", placeholder="name@example.com")
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="••••••••")

            def is_valid_email(e):
                return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', e)

            # Full-width Signup Button
            if st.button("Create Account", key="signup_btn", type="primary", use_container_width=True):
                if name and reg_email and reg_password:
                    if not is_valid_email(reg_email):
                        st.warning("Please enter a valid email address.")
                    elif len(reg_password) < 8:
                        st.warning("Password must be at least 8 characters.")
                    else:
                        success, message = add_user(name, reg_email, reg_password)
                        if success:
                            st.success("Account created! Please log in.")
                            st.session_state.auth_mode = 'login'
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill all fields.")

            # Divider
            st.markdown("""
                <div class="divider-container">
                    <div class="divider-line"></div>
                    <div class="divider-text">or</div>
                    <div class="divider-line"></div>
                </div>
            """, unsafe_allow_html=True)

            # Switch to Login text
            if st.button("Already have an account? Log in", key="go_login", type="tertiary", use_container_width=True):
                st.session_state.auth_mode = 'login'
                st.rerun()

        # ==================== VIEW 3: FORGOT PASSWORD ====================
        elif st.session_state.auth_mode == 'forgot_password':
            st.markdown("""
                <div class="auth-header">
                    <h1>Reset Password</h1>
                    <p>We'll send you a 6-digit code to reset it.</p>
                </div>
            """, unsafe_allow_html=True)

            if not st.session_state.get('show_reset_form', False):
                reset_email_input = st.text_input("Registered Email", key="reset_email_widget", placeholder="name@example.com")
                
                # Full Width Send Code Button
                if st.button("Send Reset Code", key="send_reset_btn", type="primary", use_container_width=True):
                    if reset_email_input:
                        user = get_user_by_email(reset_email_input)
                        if user:
                            token_data = create_reset_token(user['id'])
                            success, message = send_reset_email(reset_email_input, token_data['reset_code'], user['username'])
                            if success:
                                st.success("✅ Code sent to your email.")
                                st.session_state['reset_email_for_verification'] = reset_email_input
                                st.session_state['show_reset_form'] = True
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("No account found with this email.")
                    else:
                        st.warning("Please enter your email.")
                
                if st.button("I already have a code", key="have_code_btn", type="tertiary", use_container_width=True):
                    st.session_state['show_reset_form'] = True
                    st.rerun()

            else:
                # User has the code, show reset fields
                reset_code = st.text_input("6-Digit Code", key="reset_code_input", placeholder="123456", max_chars=6)
                new_password = st.text_input("New Password", type="password", key="reset_new_password", placeholder="••••••••")
                confirm_password = st.text_input("Confirm Password", type="password", key="reset_confirm_password", placeholder="••••••••")
                
                if st.button("Confirm Reset", key="reset_password_btn", type="primary", use_container_width=True):
                    if reset_code and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match.")
                        elif len(new_password) < 8:
                            st.warning("Password must be at least 8 characters.")
                        else:
                            reset_email = st.session_state.get('reset_email_for_verification', '')
                            if reset_email:
                                success, message = reset_password_with_code(reset_email, reset_code, new_password)
                                if success:
                                    st.success("✅ Password reset successfully! Please log in.")
                                    st.session_state['show_reset_form'] = False
                                    st.session_state['reset_email_for_verification'] = ''
                                    st.session_state.auth_mode = 'login'
                                    st.rerun()
                                else:
                                    st.error(f"{message}")
                            else:
                                st.error("Please request a reset code first.")
                    else:
                        st.warning("Please fill all fields.")
                
                # Divider
                st.markdown("""
                    <div class="divider-container">
                        <div class="divider-line"></div>
                        <div class="divider-text">or</div>
                        <div class="divider-line"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Back to Login
                if st.button("Back to login", key="back_to_login", type="tertiary", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.session_state['show_reset_form'] = False
                    st.session_state['reset_email_for_verification'] = ''
                    st.rerun()
