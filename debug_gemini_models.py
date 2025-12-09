
import google.generativeai as genai
import toml
import os

try:
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = toml.load(f)
        genai.configure(api_key=secrets["GEMINI_API_KEY"])
        
    print("Listing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
except Exception as e:
    print(f"Error: {e}")
