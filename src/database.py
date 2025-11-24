"""
Database operations for EchoPost
"""
import streamlit as st
from supabase import create_client

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def create_post(user_id, content, topic, tags=None):
    supabase = init_supabase()
    data = {
        "user_id": user_id,
        "content": content,
        "topic": topic,
        "tags": tags or [],
        "word_count": len(content.split())
    }
    try:
        response = supabase.table("posts").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Error saving post: {e}")
        return None

def get_posts(user_id, limit=None):
    supabase = init_supabase()
    try:
        query = supabase.table("posts").select("*").eq("user_id", user_id).order("created_at", desc=True)
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []

def delete_post(post_id):
    supabase = init_supabase()
    try:
        response = supabase.table("posts").delete().eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error deleting post: {e}")
        return None

def update_post_tags(post_id, tags):
    """Update tags for a post"""
    supabase = init_supabase()
    try:
        response = supabase.table("posts").update({"tags": tags}).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error updating tags: {e}")
        return None

def toggle_favorite(post_id, is_favorite):
    """Toggle favorite status of a post"""
    supabase = init_supabase()
    try:
        response = supabase.table("posts").update({"is_favorite": is_favorite}).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error toggling favorite: {e}")
        return None

def search_posts(user_id, query=None, tags=None, favorites_only=False):
    """Search posts by content, tags, or favorites"""
    supabase = init_supabase()
    try:
        db_query = supabase.table("posts").select("*").eq("user_id", user_id)
        
        # Filter by favorites
        if favorites_only:
            db_query = db_query.eq("is_favorite", True)
        
        # Filter by tags
        if tags and len(tags) > 0:
            db_query = db_query.contains("tags", tags)
        
        # Execute query
        response = db_query.order("created_at", desc=True).execute()
        results = response.data
        
        # Filter by search query (client-side for now)
        if query and len(query) > 0:
            query_lower = query.lower()
            results = [
                post for post in results
                if query_lower in post.get('content', '').lower() or 
                   query_lower in post.get('topic', '').lower()
            ]
        
        return results
    except Exception as e:
        st.error(f"Error searching posts: {e}")
        return []

def get_all_tags(user_id):
    """Get all unique tags used by a user"""
    supabase = init_supabase()
    try:
        response = supabase.table("posts").select("tags").eq("user_id", user_id).execute()
        all_tags = set()
        for post in response.data:
            if post.get('tags'):
                all_tags.update(post['tags'])
        return sorted(list(all_tags))
    except Exception as e:
        st.error(f"Error fetching tags: {e}")
        return []
