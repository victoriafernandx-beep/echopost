import google.generativeai as genai
import toml
import sys
import os

def verify_gemini():
    print("Verifying Gemini API Configuration...")

    # 1. Load Secrets
    try:
        secrets_path = ".streamlit/secrets.toml"
        if not os.path.exists(secrets_path):
            print(f"Error: {secrets_path} not found.")
            return False
        
        secrets = toml.load(secrets_path)
        # Handle different structures of secrets.toml (nested 'secrets' key or flat)
        if "secrets" in secrets and "GEMINI_API_KEY" in secrets["secrets"]:
             api_key = secrets["secrets"]["GEMINI_API_KEY"]
        elif "GEMINI_API_KEY" in secrets:
            api_key = secrets["GEMINI_API_KEY"]
        else:
            print("Error: GEMINI_API_KEY not found in secrets.toml")
            return False
            
        print("API Key found in secrets.")
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return False

    # 2. Configure Gemini
    try:
        genai.configure(api_key=api_key)
        print("Gemini configured.")
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return False

    # 3. Test Generation
    try:
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")

        print("Attempting to generate content with gemini-flash-latest...")
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Say 'Hello, EchoPost!' if you can hear me.")
        
        if response and response.text:
            print(f"Success! Response received:\n---\n{response.text}\n---")
            return True
        else:
            print("Warning: No text returned in response.")
            return False
            
    except Exception as e:
        print(f"Error generating content: {e}")
        return False

if __name__ == "__main__":
    if verify_gemini():
        sys.exit(0)
    else:
        sys.exit(1)
