import streamlit as st

def show_sidebar():

    # Hide Streamlit default multipage navigation (App / About)
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## 🧠 MindCare AI")
        
        # Display username
        username = st.session_state.user[1]  # assuming user[1] is the name
        st.write(f"Welcome **{username}**")
        
        # Navigation
        menu = st.radio(
            "Navigation",
            ["Dashboard", "Chat", "History", "Mood Analytics", "Journal"],
            index=["Dashboard", "Chat", "History", "Mood Analytics", "Journal"].index(
                st.session_state.get("current_page", "Dashboard")
            )
        )

        st.session_state.current_page = menu
        
        st.markdown("---")
        
        # Logout
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.current_page = "Dashboard"
            st.rerun()