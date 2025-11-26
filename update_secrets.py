import os

secrets_content = """SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
"""

os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
    f.write(secrets_content)

print("secrets.toml updated successfully.")
