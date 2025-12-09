
import streamlit as st
import toml
import os
import sys

# Add current directory to path so we can import src
sys.path.append(os.getcwd())

# Mock st.secrets
try:
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = toml.load(f)
        st.secrets = secrets
        print("[OK] Secrets loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load secrets: {e}")
    sys.exit(1)

from src import news
from src import generator

def test_news():
    print("\n--- Testing News Search ---")
    try:
        # Try a broader topic
        topic = "Technology"
        print(f"Fetching news for '{topic}'...")
        articles = news.fetch_news(topic, language='pt')
        if articles:
            print(f"[OK] Success! Found {len(articles)} articles.")
            print(f"First article: {articles[0]['title']}")
        else:
            print("[FAIL] No articles found even with fallback.")
            
    except Exception as e:
        print(f"[ERROR] Error in test_news: {e}")

def test_generation():
    print("\n--- Testing Post Generation (OpenAI) ---")
    try:
        print("Generating post for 'Teste de OpenAI'...")
        # Mock st.spinner
        import contextlib
        @contextlib.contextmanager
        def mock_spinner(text):
            print(f"Spinner: {text}")
            yield
        st.spinner = mock_spinner
        
        result = generator.generate_post("Teste de OpenAI", tone="Profissional")
        
        if "Erro" in result:
            print(f"[FAIL] Generation failed: {result}")
        else:
            print("[OK] Generation successful!")
            print(f"Preview: {result[:100]}...")
            
    except Exception as e:
        print(f"[ERROR] Error in test_generation: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    test_news()
    test_generation()
