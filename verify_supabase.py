import streamlit as st
from supabase import create_client
import sys

# Load secrets directly since we are running as a script, not via streamlit run
# But streamlit secrets handling is tricky in standalone scripts without st.secrets being populated by the runner.
# We will parse the secrets.toml manually for this test script or just hardcode for the test since we know them.
# Actually, let's just read the file.

import toml

try:
    secrets = toml.load(".streamlit/secrets.toml")
    url = secrets["secrets"]["SUPABASE_URL"]
    key = secrets["secrets"]["SUPABASE_KEY"]
except Exception as e:
    print(f"Error loading secrets: {e}")
    sys.exit(1)

supabase = create_client(url, key)

print(f"Connecting to {url}...")

try:
    # Try to select from the posts table
    response = supabase.table("posts").select("*").limit(1).execute()
    print("Success! Table 'posts' exists and is accessible.")
    print(f"Data: {response.data}")
except Exception as e:
    print(f"Error: {e}")
    print("It seems the table 'posts' does not exist or permissions are wrong.")
    print("Please run the SQL script in the Supabase Dashboard.")
