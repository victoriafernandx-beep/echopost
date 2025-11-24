import google.generativeai as genai
import streamlit as st

def configure_genai():
    # genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    pass

def generate_post(topic, tone="Professional"):
    return f"Generated post about {topic} with {tone} tone."
