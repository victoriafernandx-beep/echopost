import os

secrets_content = """SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
LINKEDIN_CLIENT_ID = "SEU_CLIENT_ID"
LINKEDIN_CLIENT_SECRET = "SEU_CLIENT_SECRET"
LINKEDIN_REDIRECT_URI = "http://localhost:8503"
NEWS_API_KEY = "960005a1774143418a92cd997887ee6e"
"""

os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
    f.write(secrets_content)

print("secrets.toml updated successfully.")
