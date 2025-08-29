#!/usr/bin/env python3
"""
Simple test to verify the minimal app works
"""
import subprocess
import sys
import time

def test_streamlit_import():
    """Test if streamlit can be imported"""
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
        return True
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False

def test_app_syntax():
    """Test if the app file has valid Python syntax"""
    try:
        with open('minimal-test.py', 'r') as f:
            code = f.read()
        compile(code, 'minimal-test.py', 'exec')
        print("✓ App syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ App syntax error: {e}")
        return False

if __name__ == "__main__":
    print("Testing minimal Streamlit app...")
    
    success = True
    success &= test_streamlit_import()
    success &= test_app_syntax()
    
    if success:
        print("\n✓ All tests passed! App should work in App Runner.")
    else:
        print("\n✗ Tests failed. Fix issues before deploying.")
        sys.exit(1)