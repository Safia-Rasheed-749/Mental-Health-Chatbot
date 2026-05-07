import streamlit as st

st.set_page_config(page_title="Navbar Test", layout="wide")

# Test if HTML renders properly
st.markdown("""
<style>
.test-box {
    background: #7c3aed;
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="test-box">
    <h1>✅ HTML IS RENDERING CORRECTLY!</h1>
    <p>If you can see this styled box, then unsafe_allow_html is working.</p>
</div>
""", unsafe_allow_html=True)

st.write("---")
st.write("Now testing navbar component:")

from components.navbar import render_navbar
render_navbar()

st.write("# Test Page Content")
st.write("If navbar shows as HTML text above, the issue is with the navbar component.")
st.write("If navbar renders properly, the issue is with your main app.py caching.")
