import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def create_post(user_id, content, topic):
    supabase = init_supabase()
    # Assuming a 'posts' table exists
    data = {"user_id": user_id, "content": content, "topic": topic}
    try:
        response = supabase.table("posts").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Error saving post: {e}")
        return None

def get_posts(user_id):
    supabase = init_supabase()
    try:
        response = supabase.table("posts").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []
