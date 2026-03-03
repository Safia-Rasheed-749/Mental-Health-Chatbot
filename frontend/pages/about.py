
import streamlit as st

def show_about_page():
    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3rem; font-weight: 800; color: #1e293b;">About <span style="color: #4f46e5;">MindCareAI</span></h1>
            <p style="font-size: 1.2rem; color: #64748b; max-width: 800px; margin: 0 auto;">
                A specialized AI-powered conversational assistant designed at NUML Islamabad to provide empathetic mental health support.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Project Goals Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🎯 Mission\nTo provide 24/7 accessible mental health support without social stigma.")
    with col2:
        st.success("### 🔒 Privacy\nSecure PostgreSQL storage ensuring your conversations stay private.")
    with col3:
        st.warning("### 🤖 Technology\nPowered by Transformer models and Whisper for voice interaction.")

    st.markdown("---")
    
    # Team Section
    st.markdown("<h2 style='text-align: center;'>Our Team</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    
    team = [
        {"name": "Safia Rasheed", "id": "BSCS-MC-215"},
        {"name": "Maria Akram", "id": "BSCS-MC-207"},
        {"name": "Shamsa Akram", "id": "BSCS-MC-208"}
    ]
    
    for i, member in enumerate(team):
        with [t1, t2, t3][i]:
            st.markdown(f"""
                <div style="background: #f8fafc; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center;">
                    <h4 style="margin-bottom: 5px;">{member['name']}</h4>
                    <code style="color: #4f46e5;">{member['id']}</code>
                </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-top: 40px; padding: 20px; background: #EEF2FF; border-radius: 10px; text-align: center;">
            <p style="margin: 0; color: #4338ca; font-weight: 600;">Supervised By: Faisal Hussain</p>
        </div>
    """, unsafe_allow_html=True)