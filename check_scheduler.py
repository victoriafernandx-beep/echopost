import streamlit as st
from src import database
from datetime import datetime
import pytz

# Force load secrets (workaround for script execution outside streamlit run)
import toml
try:
    secrets = toml.load(".streamlit/secrets.toml")
    st.secrets = secrets
except:
    pass

print("--- DIAGNOSTIC SCRIPT ---")
print(f"UTC Now: {datetime.utcnow().isoformat()}")
print(f"Local (Sao Paulo): {datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()}")

print("\nQuerying Pending Posts via Service Key...")
try:
    # Use service role to simulate scheduler access
    supabase = database.get_supabase_client(use_service_role=True)
    
    # Get all pending
    response = supabase.table("scheduled_posts").select("*").eq("status", "pending").execute()
    posts = response.data
    
    print(f"Found {len(posts)} pending posts total.")
    
    for p in posts:
        s_time = p.get('scheduled_time')
        print(f"ID: {p['id']}")
        print(f"  Topic: {p['topic']}")
        print(f"  Scheduled (DB): {s_time}")
        print(f"  Timezone: {p['timezone']}")
        print(f"  Should publish? {s_time <= datetime.utcnow().isoformat()}")
        
except Exception as e:
    print(f"Error querying: {e}")
