import os
import sys

# Add parent directory to path to allow importing from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src import database
import io

# Force UTF-8 for stdout/stderr to handle emojis on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def setup_scheduled_posts_table():
    print("🚀 Initializing database setup...")
    
    # Read the schema file
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'scheduled_posts_schema.sql')
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Schema file not found at {schema_path}")
        return

    # Initialize Supabase client
    try:
        supabase = database.init_supabase()
        print("✅ Supabase client initialized")
    except Exception as e:
        print(f"❌ Error initializing Supabase: {e}")
        return

    # Execute SQL - Note: Supabase-py client usually doesn't support direct SQL execution 
    # for DDL (CREATE TABLE) depending on the key permissions. 
    # If this fails, we might need to use the SQL Editor in Supabase dashboard.
    # However, sometimes we can use the rpc call if a helper function exists, 
    # or just try to insert dependent on if the table exists.
    
    # Since we can't reliably execute raw SQL DDL via the standard client without a specific function,
    # we will try to use the `postgrest` client's ability if available, or warn the user.
    
    # ALTERNATIVE: loading the SQL via an RPC call if one existed. 
    # But since we are creating the table, we assume the user might need to run this manually 
    # if the client forbids it. Let's try to verify if the table exists first.
    
    try:
        # Check if table exists by trying to select from it
        supabase.table("scheduled_posts").select("id").limit(1).execute()
        print("✅ Table 'scheduled_posts' already exists and is accessible.")
        return
    except Exception as e:
        print(f"ℹ️ Table 'scheduled_posts' likely does not exist (or access denied). Error: {e}")
        print("⚠️ attempting to create via SQL Editor is recommended.")
        
    print("\n⚠️ IMPORTANT: To create the table, please copy the contents of 'scheduled_posts_schema.sql' and run it in your Supabase SQL Editor.")
    print(f"📂 Schema file: {schema_path}")

if __name__ == "__main__":
    setup_scheduled_posts_table()
