"""
Database operations for EchoPost
"""
import streamlit as st
from supabase import create_client

import os

# supabase = create_client(url, key)
# Removed cache_resource to ensure we can have unique authenticated clients per user/request
def init_supabase():
    url = st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        return None
        
    return create_client(url, key)

def get_supabase_client(use_service_role=False):
    """
    Get supabase client.
    Args:
        use_service_role: If True, attempts to use SUPABASE_SERVICE_KEY for admin access
    """
    # 1. Try st.secrets (Local/Streamlit Cloud)
    if "SUPABASE_URL" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        if use_service_role:
            key = st.secrets.get("SUPABASE_SERVICE_KEY", st.secrets["SUPABASE_KEY"])
        else:
            key = st.secrets["SUPABASE_KEY"]
    
    # 2. Linux/Render Env Vars
    else:
        url = os.getenv("SUPABASE_URL")
        if use_service_role:
            key = os.getenv("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_KEY"))
        else:
            key = os.getenv("SUPABASE_KEY")
            
    if not url or not key:
        print("❌ Supabase config not found in Secrets or Env")
        return None

    return create_client(url, key)

    # Standard client (Anon)
    key = st.secrets["SUPABASE_KEY"]
    
    # Create client
    client = create_client(url, key)
    
    # Set auth token on postgrest if available
    try:
        if 'access_token' in st.session_state and st.session_state.access_token:
            # Set authorization header for postgrest
            # Fix: Use .auth() method instead of accessing session.headers directly (which caused AttributeError)
            client.postgrest.auth(st.session_state.access_token)
    except Exception as e:
        # Log warning but continue, as we might be in a context where session isn't available
        # or we are using service role key above (though this block is after service role check? 
        # Actually logic is: if service role, return early. So here we are using Anon key.)
        print(f"WARN: Could not inject auth header: {e}")
        
    return client

def create_post(user_id, content, topic, tags=None, metrics=None, created_at=None):
    supabase = get_supabase_client()
    data = {
        "user_id": user_id,
        "content": content,
        "topic": topic,
        "tags": tags or [],
        "word_count": len(content.split())
    }
    
    # Add optional fields if provided
    if metrics:
        data.update({
            "likes_count": metrics.get("likes", 0),
            "comments_count": metrics.get("comments", 0),
            "shares_count": metrics.get("shares", 0),
            "views_count": metrics.get("views", 0)
        })
        
    if created_at:
        data["created_at"] = created_at
        
    try:
        response = supabase.table("posts").insert(data).execute()
        return response
    except Exception as e:
        # Handle missing column error gracefully
        if 'column' in str(e) and 'does not exist' in str(e):
             st.error("⚠️ Erro de Banco de Dados: Colunas de métricas ausentes. Por favor, execute o script 'add_metrics_schema.sql' no Supabase.")
        else:
             st.error(f"Error saving post: {e}")
        return None

def get_posts(user_id, limit=None):
    supabase = get_supabase_client()
    try:
        # Query specific user OR whatsapp bot posts
        # Fix: Use .in_() for safe parameterization instead of vulnerable .or() string interpolation
        bot_id = st.secrets.get("WHATSAPP_BOT_USER_ID", "whatsapp-bot")
        query = supabase.table("posts").select("*").in_("user_id", [user_id, bot_id]).order("created_at", desc=True)
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []

def delete_post(post_id, user_id):
    supabase = get_supabase_client()
    try:
        # Verify ownership
        post = supabase.table("posts").select("user_id").eq("id", post_id).single().execute()
        if not post.data:
            return None
        if post.data['user_id'] != user_id:
            st.error("Unauthorized: You do not own this post.")
            return None
            
        response = supabase.table("posts").delete().eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error deleting post: {e}")
        return None

def get_user_id_by_phone(phone_number):
    """
    Get user_id associated with a phone number from user_settings.
    """
    supabase = get_supabase_client()
    try:
        response = supabase.table("user_settings")\
            .select("user_id")\
            .eq("setting_key", "whatsapp_number")\
            .eq("setting_value", phone_number)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]['user_id']
        return None
    except Exception as e:
        print(f"Error finding user by phone: {e}")
        return None

def get_post_metrics(user_id=None):
    """
    Get metrics about posts (Total, by Source (WhatsApp/Web), etc).
    Also finds 'orphaned' WhatsApp posts that match the user's verified phone number.
    """
    supabase = get_supabase_client()
    try:
        # 1. Base Query
        query = supabase.table("posts").select("*", count="exact")
        
        # 2. Smart Filter: ID or Phone Tag
        if user_id:
            # Try to get phone number to recover broken links
            phone = get_user_setting(user_id, "whatsapp_number")
            
            if phone:
                # Syntax: user_id.eq.XYZ,tags.cs.{phone_123}
                # using .or_() method from postgrest
                tag_str = f"phone_{phone}"
                filter_str = f"user_id.eq.{user_id},tags.cs.{{{tag_str}}}"
                query = query.or_(filter_str)
            else:
                query = query.eq("user_id", user_id)
            
        # Execute
        response = query.execute()
        posts = response.data
        
        total_posts = len(posts)
        whatsapp_posts = sum(1 for p in posts if p.get('source') == 'whatsapp' or 'whatsapp' in p.get('tags', []))
        web_posts = total_posts - whatsapp_posts
        
        return {
            "total": total_posts,
            "whatsapp": whatsapp_posts,
            "web": web_posts,
            "posts_data": posts # Return recent posts for charts
        }
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return {"total": 0, "whatsapp": 0, "web": 0, "posts_data": []}

def update_post_tags(post_id, tags, user_id):
    """Update tags for a post"""
    supabase = get_supabase_client()
    try:
        # Verify ownership
        post = supabase.table("posts").select("user_id").eq("id", post_id).single().execute()
        if not post.data or post.data['user_id'] != user_id:
            st.error("Unauthorized")
            return None
            
        response = supabase.table("posts").update({"tags": tags}).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error updating tags: {e}")
        return None

def toggle_favorite(post_id, is_favorite, user_id):
    """Toggle favorite status of a post"""
    supabase = get_supabase_client()
    try:
        # Verify ownership
        post = supabase.table("posts").select("user_id").eq("id", post_id).single().execute()
        if not post.data or post.data['user_id'] != user_id:
            st.error("Unauthorized")
            return None

        response = supabase.table("posts").update({"is_favorite": is_favorite}).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error toggling favorite: {e}")
        return None

def search_posts(user_id, query=None, tags=None, favorites_only=False):
    """Search posts by content, tags, or favorites"""
    supabase = get_supabase_client()
    try:
        # Fix: Use .in_() for safe parameterization
        bot_id = st.secrets.get("WHATSAPP_BOT_USER_ID", "whatsapp-bot")
        db_query = supabase.table("posts").select("*").in_("user_id", [user_id, bot_id])
        
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
    supabase = get_supabase_client()
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

# ============================================
# SCHEDULED POSTS FUNCTIONS
# ============================================

def create_scheduled_post(user_id, content, topic, scheduled_time, timezone="UTC", tags=None):
    """Create a new scheduled post"""
    # DEBUG: Check auth status
    if 'access_token' not in st.session_state:
        st.error("DEBUG: No access_token in session!")
    else:
        # st.toast(f"DEBUG: Auth Token Present. User ID: {user_id}", icon="🛡️")
        pass

    supabase = get_supabase_client()
    data = {
        "user_id": user_id,
        "content": content,
        "topic": topic,
        "tags": tags or [],
        "scheduled_time": scheduled_time if isinstance(scheduled_time, str) else scheduled_time.isoformat(),
        "timezone": timezone,
        "status": "pending"
    }
    try:
        response = supabase.table("scheduled_posts").insert(data).execute()
        return response
    except Exception as e:
        # Improve error details
        st.error(f"Error creating scheduled post: {e}")
        return None

def get_scheduled_posts(user_id, status=None, limit=None):
    """Get scheduled posts for a user, optionally filtered by status"""
    supabase = get_supabase_client()
    try:
        query = supabase.table("scheduled_posts").select("*").eq("user_id", user_id)
        
        if status:
            query = query.eq("status", status)
        
        query = query.order("scheduled_time", desc=False)
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching scheduled posts: {e}")
        return []

def get_posts_to_publish():
    """Get all pending posts that are ready to be published (scheduled_time <= now)"""
    supabase = get_supabase_client()
    try:
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        
        response = supabase.table("scheduled_posts")\
            .select("*")\
            .eq("status", "pending")\
            .lte("scheduled_time", now)\
            .execute()
        
        return response.data
    except Exception as e:
        print(f"Error fetching posts to publish: {e}")
        return []

def update_scheduled_post_status(post_id, status, linkedin_post_id=None, error_message=None):
    """Update the status of a scheduled post after publishing attempt"""
    supabase = get_supabase_client()
    try:
        from datetime import datetime
        
        update_data = {"status": status}
        
        if status == "published":
            update_data["published_at"] = datetime.utcnow().isoformat()
            if linkedin_post_id:
                update_data["linkedin_post_id"] = linkedin_post_id
        
        if status == "failed" and error_message:
            update_data["error_message"] = error_message
            # Increment retry count
            post = supabase.table("scheduled_posts").select("retry_count").eq("id", post_id).execute()
            if post.data:
                current_retry = post.data[0].get("retry_count", 0)
                update_data["retry_count"] = current_retry + 1
        
        response = supabase.table("scheduled_posts").update(update_data).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error updating scheduled post status: {e}")
        return None

def delete_scheduled_post(post_id):
    """Delete/cancel a scheduled post"""
    supabase = get_supabase_client()
    try:
        # Option 1: Actually delete
        # response = supabase.table("scheduled_posts").delete().eq("id", post_id).execute()
        
        # Option 2: Mark as cancelled (better for audit trail)
        response = supabase.table("scheduled_posts").update({"status": "cancelled"}).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error deleting scheduled post: {e}")
        return None

def reschedule_post(post_id, new_scheduled_time, new_timezone=None):
    """Reschedule a post to a new time"""
    supabase = get_supabase_client()
    try:
        update_data = {
            "scheduled_time": new_scheduled_time,
            "status": "pending"  # Reset to pending if it was failed
        }
        
        if new_timezone:
            update_data["timezone"] = new_timezone
        
        response = supabase.table("scheduled_posts").update(update_data).eq("id", post_id).execute()
        return response
    except Exception as e:
        st.error(f"Error rescheduling post: {e}")
        return None

def get_scheduled_posts_count(user_id, status="pending"):
    """Get count of scheduled posts by status"""
    supabase = get_supabase_client()
    try:
        response = supabase.table("scheduled_posts")\
            .select("id", count="exact")\
            .eq("user_id", user_id)\
            .eq("status", status)\
            .execute()
        
        return response.count if hasattr(response, 'count') else len(response.data)
    except Exception as e:
        st.error(f"Error counting scheduled posts: {e}")
        return 0

def get_upcoming_scheduled_posts(user_id, days=7):
    """Get scheduled posts for the next N days"""
    supabase = get_supabase_client()
    try:
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        future = now + timedelta(days=days)
        
        response = supabase.table("scheduled_posts")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("status", "pending")\
            .gte("scheduled_time", now.isoformat())\
            .lte("scheduled_time", future.isoformat())\
            .order("scheduled_time", desc=False)\
            .execute()
        
        return response.data
    except Exception as e:
        st.error(f"Error fetching upcoming posts: {e}")
        return []

# ============================================
# TOKEN MANAGEMENT FUNCTIONS
# ============================================

def save_linkedin_token(user_id, access_token, refresh_token=None, expires_in=None):
    """Save LinkedIn token to database for offline access"""
    """Save LinkedIn token to database for offline access"""
    # Use Service Role to ensure we can write to the DB regardless of RLS
    # This is critical for avoiding 'silent failures' in Streamlit Cloud
    supabase = get_supabase_client(use_service_role=True)
    
    # Calculate expiration timestamp
    expires_at = None
    if expires_in:
        from datetime import datetime, timedelta
        expires_at = (datetime.utcnow() + timedelta(seconds=int(expires_in))).isoformat()
    
    data = {
        "user_id": user_id,
        "provider": "linkedin",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at
    }
    
    try:
        # Upsert: insert or update if exists
        response = supabase.table("user_connections").upsert(data).execute()
        # print(f"DEBUG: Token saved successfully. Response: {response.data}")
        
        # VERIFY WRITE
        verify = supabase.table("user_connections").select("*").eq("user_id", user_id).execute()
        if verify.data:
             # print(f"DEBUG: VERIFICATION SUCCESS! Found {len(verify.data)} row(s).")
             # Inject a visual confirmation for the user
             st.toast(f"Tudo certo! Token salvo e verificado. (ID: {user_id[-4:]})", icon="💾")
        else:
             # print(f"DEBUG: VERIFICATION FAILED! Row not found after insert.")
             st.error("ERRO CRÍTICO: O banco de dados confirmou a gravação mas os dados sumiram. Contate o suporte.")
             return None
             
        return response
    except Exception as e:
        print(f"Error saving token: {e}")
        st.error(f"Erro de Banco de Dados ao salvar token: {e}")
        return None

def get_linkedin_token(user_id):
    """Get stored LinkedIn token for a user"""
    supabase = get_supabase_client()
    try:
        response = supabase.table("user_connections")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("provider", "linkedin")\
            .single()\
            .execute()
            
        data = response.data
        if data and data.get('expires_at'):
            from datetime import datetime
            try:
                # Handle simplified ISO format
                expires_at_str = data['expires_at'].replace('Z', '+00:00')
                expires_at = datetime.fromisoformat(expires_at_str)
                
                # Compare with current UTC time (ensure timezone awareness match)
                from datetime import timezone
                now = datetime.now(timezone.utc)
                
                # If expires_at is naive, assume UTC
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                    
                if now > expires_at:
                    print(f"WARN: Token for user {user_id} expired at {expires_at}")
                    return None
            except Exception as e:
                print(f"WARN: Error parsing token expiration: {e}")
                # If parsing fails, return data but warn
                
        return data
    except Exception as e:
        # Only log if it's not simply "Row not found"
        if "JSON object requested, multiple (or no) rows returned" not in str(e):
             print(f"Error fetching token: {e}")
        return None

# ============================================
# USER SETTINGS FUNCTIONS
# ============================================

def save_user_setting(user_id, key, value):
    """Save a user preference setting"""
    supabase = get_supabase_client()
    try:
        data = {
            "user_id": user_id,
            "setting_key": key,
            "setting_value": value
        }
        # Upsert
        response = supabase.table("user_settings").upsert(data).execute()
        return response
    except Exception as e:
        # Avoid loud errors if table doesn't exist yet
        print(f"Error saving setting: {e}")
        return None

def get_user_setting(user_id, key):
    """Get a user preference setting"""
    supabase = get_supabase_client()
    try:
        response = supabase.table("user_settings")\
            .select("setting_value")\
            .eq("user_id", user_id)\
            .eq("setting_key", key)\
            .single()\
            .execute()
            
        if response.data:
            return response.data.get("setting_value")
        return None
    except Exception as e:
        # Silent fail is better here than crashing UI
        return None
