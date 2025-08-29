import streamlit as st
import os
import sys

# Force static rendering mode
st.set_page_config(
    page_title="Test App", 
    page_icon="🧪",
    layout="wide"
)

# Static content that doesn't require WebSocket
st.title("🧪 Test App - Static Mode")
st.write("**App is running successfully!**")

st.success("✅ Deployment successful - Static rendering mode")

# Environment info (static)
st.subheader("Environment Information")
col1, col2 = st.columns(2)

with col1:
    st.write("**Python Version:**")
    st.code(sys.version)
    
with col2:
    st.write("**Working Directory:**")
    st.code(os.getcwd())

# Environment variables (static display)
st.subheader("Environment Variables")
aws_region = os.getenv('AWS_REGION', 'Not set')
kb_id = os.getenv('KB_ID', 'Not set')
port = os.getenv('PORT', 'Not set')

st.write(f"**AWS_REGION:** `{aws_region}`")
st.write(f"**KB_ID:** `{kb_id}`")
st.write(f"**PORT:** `{port}`")

# Static success message
st.write("---")
st.info("🎉 If you can see this page completely, the App Runner deployment is working!")

# Simple form that works without WebSocket
with st.form("test_form"):
    st.write("**Test Form (Submit-based, no WebSocket needed):**")
    test_input = st.text_input("Enter some text:")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"✅ Form submitted! You entered: {test_input}")

st.write("---")
st.write("**Note:** This is a static-rendering version that works without WebSocket connections.")