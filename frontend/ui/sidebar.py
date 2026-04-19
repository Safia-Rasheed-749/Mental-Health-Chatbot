# ui/sidebar.py (UPDATED FOR YOUR APP.PY)
import streamlit as st

def init_sidebar_state():
    """Initialize sidebar session state"""
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True

def show_sidebar():
    """Display custom sidebar with proper state management"""
    
    init_sidebar_state()
    
    # CRITICAL: Remove the hide class when user is logged in
    # This CSS will override the hiding from app.py
    st.markdown("""
        <style>
        /* Force sidebar to be visible for logged-in users */
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Hide only the default page navigation links (App/About) */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Ensure collapse button remains visible and clickable */
        button[kind="header"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        
        /* Optional: Customize collapse button styling */
        button[kind="header"] svg {
            stroke: #4a90e2 !important;
            stroke-width: 2px !important;
        }
        
        /* Fix sidebar width consistency */
        section[data-testid="stSidebar"] > div {
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Validate user is logged in
    if "user" not in st.session_state or st.session_state.user is None:
        st.error("Please login first")
        return False
    
    # Safely get username
    try:
        username = st.session_state.user[1] if len(st.session_state.user) > 1 else "User"
    except (TypeError, IndexError):
        username = "User"
    
    with st.sidebar:
        st.markdown("## 🧠 MindCare AI")
        st.write(f"Welcome **{username}**")
        
        st.markdown("---")
        
        # Navigation menu
        menu_options = ["Dashboard", "Chat", "History", "Mood Analytics", "Journal"]
        
        # Get current page with validation
        current_page = st.session_state.get("current_page", "Dashboard")
        if current_page not in menu_options:
            current_page = "Dashboard"
            st.session_state.current_page = current_page
        
        # Find index safely
        try:
            default_index = menu_options.index(current_page)
        except ValueError:
            default_index = 0
        
        menu = st.radio(
            "Navigation",
            menu_options,
            index=default_index,
            key="sidebar_navigation"
        )
        
        # Update session state
        if menu != st.session_state.current_page:
            st.session_state.current_page = menu
            st.rerun()  # Force rerun to load new page
        
        st.markdown("---")

        
        # Logout button
        if st.button("🚪 Logout", type="primary"):
            # Proper logout cleanup
            logout_and_cleanup()
            st.rerun()
            return False
    
    return True

def logout_and_cleanup():
    """Properly cleanup session state on logout"""
    # Clear user data
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.session_state.page = "landing"
    
    # Optional: Clear sensitive data but preserve settings if needed
    keys_to_clear = ['chat_history', 'demo_messages', 'demo_count']
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state[key] = [] if key == 'chat_history' else ([] if 'messages' in key else 0)
    
    # Reset sidebar visibility flag
    st.session_state.sidebar_visible = False