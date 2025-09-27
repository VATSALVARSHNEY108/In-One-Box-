import os
import streamlit as st
from utils.ai_client import ai_client


def test_ai_client():
    """Debug the AI client functionality"""
    print("=== AI Client Debug ===")

    # Check environment variables
    print(f"GEMINI_API_KEY in env: {bool(os.environ.get('GEMINI_API_KEY'))}")
    print(f"GOOGLE_API_KEY in env: {bool(os.environ.get('GOOGLE_API_KEY'))}")

    # Check AI client methods
    print(f"Has Gemini: {ai_client._has_gemini()}")
    print(f"Get Gemini Key: {bool(ai_client._get_gemini_key())}")

    # Test a simple text generation
    try:
        response = ai_client.generate_text("Say hello", model="gemini")
        print(f"Test response: {response[:100]}...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    test_ai_client()