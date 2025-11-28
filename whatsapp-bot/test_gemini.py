#!/usr/bin/env python3
"""Script to test Gemini API with the new key"""
import os
import google.generativeai as genai

# Test with the new key
api_key = "AIzaSyDqZhTww2VdJJR0WbsZ0THL0w82uL7GwqA"

print(f"Testing Gemini API with key: {api_key[:20]}...")

try:
    genai.configure(api_key=api_key)
    print("✓ API configured")
    
    # List available models
    print("\nAvailable models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    
    # Test generation with gemini-1.5-flash
    print("\nTesting gemini-1.5-flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✓ Success! Response: {response.text}")
    
except Exception as e:
    print(f"✗ Error: {e}")
