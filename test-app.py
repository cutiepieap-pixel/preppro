import streamlit as st
import os
import sys

print("Starting Streamlit app...")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print("Environment variables:")
for key, value in os.environ.items():
    if key.startswith(('AWS', 'KB', 'MODEL', 'PYTHON')):
        print(f"  {key}={value}")
print("App starting...")

try:
    st.set_page_config(
        page_title="Test App", 
        page_icon="🧪",
        layout="wide"
    )

    st.title("🧪 Test App")
    st.write("If you can see this, the basic Streamlit app is working!")

    st.success("✅ App is running successfully")

    # Test environment variables
    st.subheader("Environment Check")
    aws_region = os.getenv('AWS_REGION', 'Not set')
    kb_id = os.getenv('KB_ID', 'Not set')

    st.write(f"**AWS_REGION:** {aws_region}")
    st.write(f"**KB_ID:** {kb_id}")

    # Simple interaction test
    if st.button("Test Button"):
        st.balloons()
        st.write("✅ Button works!")

    st.write("---")
    st.write("If you can see this entire page, Streamlit is working correctly!")
    
    print("Streamlit app loaded successfully!")
    
except Exception as e:
    print(f"ERROR in Streamlit app: {e}")
    import traceback
    traceback.print_exc()
    st.error(f"App Error: {e}")
    st.code(traceback.format_exc())