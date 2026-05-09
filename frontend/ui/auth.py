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
    
    /* =========================================
       COLOR CHANGE GUIDE - GLOBAL ELEMENTS
       =========================================
       To change MAIN BACKGROUND: Find 'background: #ffffff' below
       To change FONT FAMILY: Find 'font-family: 'Inter'' below
       To change CARD BACKGROUND: Find section '[data-testid="column"]:nth-child(2)' below
    ========================================= */
    
    /* Hide Streamlit default headers & footers */
    header, footer, .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden; }

    /* Clean White Background */
    .stApp { 
        background: #ffffff;  /* CHANGE THIS: Overall app background color */
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    .main .block-container { 
        padding-top: 85px !important; 
        padding-bottom: 2rem !important;
        max-width: 1000px;
        overflow-y: hidden !important;
    }
    
    /* Disable auto-scroll */
    section[data-testid="stAppViewContainer"] {
        overflow-y: auto !important;
    }

    
    [data-testid="column"]:nth-child(2) {
        background: #ffffff !important;  /* CHANGE THIS: Card background color */
        border-radius: 20px !important;
        padding: 2.5rem 3rem 3rem 3rem !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(0, 0, 0, 0.05) inset !important;
        border: 1px solid #e5e7eb !important;  /* CHANGE THIS: Card border color */
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
        margin-top: 1rem;
    }
    /*welcome back background color*/
    .auth-header h1 { 
        /* GRADIENT TEXT - To change title color, modify these two hex codes  main headinds bckground color*/
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* CHANGE THIS: Title gradient colors */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; /* TEXT MAIN HEADINGS changes.*/
        background-clip: text;
        font-size: 2rem !important; 
        font-weight: 800 !important; 
        margin-bottom: 0.5rem !important; 
        padding-bottom: 0;
        letter-spacing: -0.5px;
    }
    /* text below main headings welcome back craete an account and reset password color changes.*/
    .auth-header p { 
        color: #475569 !important;   /* DARKER color for better visibility */
        font-size: 1rem !important;  /* INCREASED from 0.95rem */
        margin-top: 0 !important;
        font-weight: 500 !important;  /* MEDIUM weight for better readability */
    }

    
    /* input fields name color change - INCREASED FONT SIZE - ULTRA AGGRESSIVE */
    .stTextInput label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] > label,
    label[data-testid="stWidgetLabel"],
    .stTextInput > label,
    [data-testid="column"] label {
        display: none !important;  /* HIDE ALL STREAMLIT LABELS - we use custom HTML labels */
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove Streamlit's default input wrapper border */
    div[data-testid="stTextInput"] > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }
    
    div[data-testid="stTextInputRootElement"] {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;  /* NOT CHANGE THIS: Input border color */
        padding: 10px 14px !important;
        background-color: #f8fafc !important;  /*  NOT CHANGE THIS: Input background color */
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stTextInputRootElement"]:focus-within {
        border-color: #667eea !important;  
        background-color: #FFFFFF !important; 
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        transform: translateY(-1px);
    }
    
    input {
        color: #FF0000 !important;  /* CHANGE THIS: Input text color */
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        border: none !important;
        background: transparent !important;
    }
    /* by default values in palceholder color change.*/
    input::placeholder {
        color: #94a3b8 !important;  /* CHANGE THIS: Placeholder text color */
        font-weight: 400 !important;
    }

    
    /* Primary Button with Gradient */
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; /* CHANGE THIS: Button gradient colors */
        color: #FFFFFF !important;  
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        margin-top: 1rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;  /* CHANGE THIS: Button shadow color (match gradient start) */
        letter-spacing: 0.3px;
    }
    
    button[kind="primary"]:hover { 
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;  /* CHANGE THIS: Hover shadow color */
    }
    
    button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    /* Tertiary Link Button - SEMI-BOLD & IMPROVED VISIBILITY */
    button[kind="tertiary"] {
        background-color: transparent !important;
        color: #5b21b6 !important;  /* Dark purple for visibility */
        width: 100% !important;
        border: none !important;
        box-shadow: none !important;
        font-weight: 600 !important;  /* SEMI-BOLD */
        font-size: 0.98rem !important;
        padding: 0.5rem !important;
        margin-top: 0.75rem !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="tertiary"]:hover { 
        color: #7c3aed !important;
        background-color: rgba(91, 33, 182, 0.08) !important;
        border-radius: 8px !important;
        text-decoration: underline !important;
    }

    /* Forgot Password Link Styling - SEMI-BOLD & IMPROVED VISIBILITY */
    .forgot-password-link {
        text-align: right;
        margin-top: -8px;
        margin-bottom: 8px;
    }
    
    .forgot-password-link button {
        font-size: 0.95rem !important;
        color: #5b21b6 !important;  /* Dark purple for visibility */
        font-weight: 600 !important;  /* SEMI-BOLD */
        padding: 0.25rem 0.5rem !important;
        width: auto !important;
        float: right;
    }
    
    .forgot-password-link button:hover {
        color: #7c3aed !important;
        text-decoration: underline !important;
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
        background: linear-gradient(to right, transparent, #e2e8f0, transparent); /* CHANGE THIS: Divider line color */
    }
    
    .divider-text {
        padding: 0 1rem;
        color: #94a3b8;  /* CHANGE THIS: Divider text color */
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Success/Error Messages */
    /* WARNING: Streamlit's alert classes might be renamed in future versions */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
        padding: 1rem !important;
        margin-top: 1rem !important;
    }
    
    /* Loading State */
    .stSpinner > div {
        border-top-color: #667eea !important;  /* CHANGE THIS: Spinner color */
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
    # NOTE: The card styling targets [data-testid="column"]:nth-child(2)
    # If you change this layout (e.g., different column ratios or more columns),
    # you'll need to update the CSS selector to match the correct column.
    _, center_col, _ = st.columns([1, 1.2, 1])  # This creates the 3 columns
    
    with center_col:
        
        # ==================== VIEW 1: LOGIN ====================
        if st.session_state.auth_mode == 'login':
            st.markdown("""
                <div class="auth-header">
                    <h1>Welcome Back</h1>
                    <p>Enter your details to sign in to your account.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Custom HTML labels with large font (semi-bold, not bold)
            st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 16px;">Email</p>', unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email", placeholder="name@example.com", label_visibility="collapsed")
            
            st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 20px;">Password</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••", label_visibility="collapsed")

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
            
            # Custom HTML labels with large font (semi-bold, not bold)
            st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 16px;">Full Name</p>', unsafe_allow_html=True)
            name = st.text_input("Full Name", key="reg_name", placeholder="John Doe", label_visibility="collapsed")
            
            st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 20px;">Email</p>', unsafe_allow_html=True)
            reg_email = st.text_input("Email", key="reg_email", placeholder="name@example.com", label_visibility="collapsed")
            
            st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 20px;">Password</p>', unsafe_allow_html=True)
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="••••••••", label_visibility="collapsed")

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
                st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 16px;">Registered Email</p>', unsafe_allow_html=True)
                reset_email_input = st.text_input("Registered Email", key="reset_email_widget", placeholder="name@example.com", label_visibility="collapsed")
                
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
                st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 16px;">6-Digit Code</p>', unsafe_allow_html=True)
                reset_code = st.text_input("6-Digit Code", key="reset_code_input", placeholder="123456", max_chars=6, label_visibility="collapsed")
                
                st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 20px;">New Password</p>', unsafe_allow_html=True)
                new_password = st.text_input("New Password", type="password", key="reset_new_password", placeholder="••••••••", label_visibility="collapsed")
                
                st.markdown('<p style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 16px; margin-top: 20px;">Confirm Password</p>', unsafe_allow_html=True)
                confirm_password = st.text_input("Confirm Password", type="password", key="reset_confirm_password", placeholder="••••••••", label_visibility="collapsed")
                
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