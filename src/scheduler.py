"""
Scheduler service for EchoPost
Handles automatic publishing of scheduled posts
"""
import streamlit as st
from datetime import datetime, timedelta
import pytz
from typing import Optional, List, Dict
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostScheduler:
    """
    Background scheduler for publishing posts at scheduled times
    """
    
    def __init__(self):
        self.scheduler = None
        self.is_running = False
        
    def start(self):
        """Start the scheduler"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.interval import IntervalTrigger
            
            self.scheduler = BackgroundScheduler()
            
            # Check for posts to publish every minute
            self.scheduler.add_job(
                func=self.check_and_publish_posts,
                trigger=IntervalTrigger(seconds=60),
                id='post_publisher',
                name='Check and publish scheduled posts',
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info("Post scheduler started successfully")
            
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler and self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Post scheduler stopped")
    
    def check_and_publish_posts(self):
        """Check for posts ready to publish and publish them"""
        try:
            from src import database
            
            # Get posts that are ready to publish
            # Use service role to bypass RLS in background thread
            supabase = database.get_supabase_client(use_service_role=True)
            
            # We need to reimplement get_posts_to_publish here because the original function
            # in database.py calls get_supabase_client() without args (Anon key).
            # Or we can update database.py. Let's do it manually here for safety.
            
            # 1. Get raw count of pending posts
            pending_count = supabase.table("scheduled_posts")\
                .select("id", count="exact")\
                .eq("status", "pending")\
                .execute()
            
            logger.info(f"SCHEDULER Check: {len(pending_count.data)} pending posts found")


            # 2. Get posts ready to publish NOW
            now = datetime.utcnow().isoformat()
            
            response = supabase.table("scheduled_posts")\
                .select("*")\
                .eq("status", "pending")\
                .lte("scheduled_time", now)\
                .execute()
                
            posts_to_publish = response.data
            
            logger.info(f"SCHEDULER: Found {len(posts_to_publish)} posts ready to publish")
            
            for post in posts_to_publish:
                logger.info(f"SCHEDULER: Processing post {post['id']}")
                self.publish_scheduled_post(post['id'], post)
                
            # 3. List recent failures (Debug help)
            failures = supabase.table("scheduled_posts")\
                .select("id, error_message, updated_at")\
                .eq("status", "failed")\
                .order("updated_at", desc=True)\
                .limit(3)\
                .execute()
            
            if len(failures.data) > 0:
                print("SCHEDULER: --- RECENT FAILURES ---")
                for f in failures.data:
                    print(f"Failed at {f['updated_at']}: {f.get('error_message', 'No error message')}")
                    
        except Exception as e:
            print(f"SCHEDULER ERROR checking posts: {e}")
            logger.error(f"Error checking posts to publish: {e}")
    
    def publish_scheduled_post(self, post_id: str, post_data: dict):
        """
        Publish a single scheduled post
        
        Args:
            post_id: ID of the scheduled post
            post_data: Post data from database
        """
        try:
            from src import database, linkedin
            
            user_id = post_data['user_id']
            content = post_data['content']
            retry_count = post_data.get('retry_count', 0)
            
            logger.info(f"Publishing post {post_id} for user {user_id}")
            
            # Check if we've exceeded max retries
            max_retries = 3
            if retry_count >= max_retries:
                logger.warning(f"Post {post_id} exceeded max retries ({max_retries})")
                database.update_scheduled_post_status(
                    post_id, 
                    "failed", 
                    error_message=f"Exceeded maximum retry attempts ({max_retries})"
                )
                return
            
            # Attempt to publish to LinkedIn
            try:
                # Fetch user token from DB using Service Role (to bypass RLS)
                supabase_admin = database.get_supabase_client(use_service_role=True)
                
                token_resp = supabase_admin.table("user_connections")\
                    .select("*")\
                    .eq("user_id", user_id)\
                    .eq("provider", "linkedin")\
                    .execute()
                    
                token_data = token_resp.data[0] if token_resp.data else None
                
                if token_data and token_data.get('access_token'):
                    token = token_data['access_token']
                    
                    # We need to replicate post_to_linkedin logic here or make it more flexible
                    # Let's import requests and do it here to be safe and independent of session state
                    import requests
                    
                    # 1. Get user profile (needed for URN)
                    headers = {
                        'Authorization': f"Bearer {token}",
                        'X-Restli-Protocol-Version': '2.0.0'
                    }
                    
                    try:
                        print(f"SCHEDULER: Fetching LinkedIn profile for user {user_id}...")
                        profile_resp = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
                        profile_resp.raise_for_status()
                        profile_data = profile_resp.json()
                        linkedin_user_id = profile_data.get("sub")
                        
                        # 2. Publish post
                        post_body = {
                            "author": f"urn:li:person:{linkedin_user_id}",
                            "lifecycleState": "PUBLISHED",
                            "specificContent": {
                                "com.linkedin.ugc.ShareContent": {
                                    "shareCommentary": {
                                        "text": content
                                    },
                                    "shareMediaCategory": "NONE"
                                }
                            },
                            "visibility": {
                                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                            }
                        }
                        
                        headers['Content-Type'] = 'application/json'
                        
                        print(f"SCHEDULER: Sending post to LinkedIn...")
                        pub_resp = requests.post(
                            "https://api.linkedin.com/v2/ugcPosts",
                            headers=headers,
                            json=post_body
                        )
                        pub_resp.raise_for_status()
                        
                        # Success!
                        # Extract ID if possible
                        try:
                            linkedin_post_id = pub_resp.json().get('id')
                        except:
                            linkedin_post_id = "published"

                        print(f"SCHEDULER: SUCCESS! LinkedIn ID: {linkedin_post_id}")

                        # Update status using admin client
                        supabase_admin.table("scheduled_posts").update({
                            "status": "published",
                            "linkedin_post_id": linkedin_post_id,
                            "published_at": datetime.utcnow().isoformat(),
                            "updated_at": datetime.utcnow().isoformat()
                        }).eq("id", post_id).execute()
                        logger.info(f"Successfully published post {post_id}")
                        
                    except Exception as api_error:
                        # API Error
                         error_msg = str(api_error)
                         if hasattr(api_error, 'response') and api_error.response:
                             try:
                                 error_msg = api_error.response.json()
                             except:
                                 pass
                                 
                         print(f"SCHEDULER: LinkedIn API Error: {error_msg}")
                         logger.error(f"LinkedIn API Error: {error_msg}")
                         database.update_scheduled_post_status(
                            post_id, 
                            "failed", 
                            error_message=f"API Error: {error_msg}"
                        )
                    
                else:
                    # No token found
                    print(f"SCHEDULER: No LinkedIn token found for user {user_id}")
                    logger.warning(f"No LinkedIn token found for user {user_id}")
                    database.update_scheduled_post_status(
                        post_id, 
                        "failed", 
                        error_message="Token não encontrado. Por favor, reconecte o LinkedIn."
                    )
                    
            except Exception as e:
                # Error during publishing logic
                error_msg = str(e)
                print(f"SCHEDULER: Exception in publishing logic: {error_msg}")
                logger.error(f"Exception logic publishing post {post_id}: {error_msg}")
                database.update_scheduled_post_status(
                    post_id, 
                    "failed", 
                    error_message=error_msg
                )
                
        except Exception as e:
            print(f"SCHEDULER: Critical error in publish_scheduled_post: {e}")
            logger.error(f"Error in publish_scheduled_post: {e}")
    
    def _notify_user(self, user_id: str, notification_type: str, message: str):
        """
        Send notification to user (placeholder for future implementation)
        
        Args:
            user_id: User to notify
            notification_type: Type of notification (success, error, warning)
            message: Notification message
        """
        # TODO: Implement notification system
        # Could use email, push notifications, in-app notifications, etc.
        logger.info(f"Notification for {user_id} ({notification_type}): {message}")


# Utility functions for best time analysis

def get_best_posting_times(user_id: str, top_n: int = 5) -> List[Dict]:
    """
    Analyze user's posting history to suggest best times to post
    
    Args:
        user_id: User ID to analyze
        top_n: Number of suggestions to return
        
    Returns:
        List of dicts with recommended posting times and reasons
    """
    try:
        from src import database, analytics
        
        # Get user's post history
        posts = database.get_posts(user_id, limit=100)
        
        if not posts or len(posts) < 5:
            # Not enough data, return general best practices
            return get_default_best_times()
        
        # Analyze posting patterns
        day_performance = {}
        hour_performance = {}
        
        for post in posts:
            created_at = post.get('created_at')
            if not created_at:
                continue
            
            # Parse datetime
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            # Get day of week (0=Monday, 6=Sunday)
            day_of_week = dt.weekday()
            hour = dt.hour
            
            # For now, use word count as a proxy for engagement
            # TODO: Use actual engagement metrics when available
            engagement_score = post.get('word_count', 0)
            
            # Aggregate by day
            if day_of_week not in day_performance:
                day_performance[day_of_week] = {'count': 0, 'total_engagement': 0}
            day_performance[day_of_week]['count'] += 1
            day_performance[day_of_week]['total_engagement'] += engagement_score
            
            # Aggregate by hour
            if hour not in hour_performance:
                hour_performance[hour] = {'count': 0, 'total_engagement': 0}
            hour_performance[hour]['count'] += 1
            hour_performance[hour]['total_engagement'] += engagement_score
        
        # Calculate average engagement
        for day in day_performance:
            day_performance[day]['avg_engagement'] = (
                day_performance[day]['total_engagement'] / day_performance[day]['count']
            )
        
        for hour in hour_performance:
            hour_performance[hour]['avg_engagement'] = (
                hour_performance[hour]['total_engagement'] / hour_performance[hour]['count']
            )
        
        # Find best days and hours
        best_days = sorted(
            day_performance.items(), 
            key=lambda x: x[1]['avg_engagement'], 
            reverse=True
        )[:3]
        
        best_hours = sorted(
            hour_performance.items(), 
            key=lambda x: x[1]['avg_engagement'], 
            reverse=True
        )[:3]
        
        # Generate recommendations
        recommendations = []
        day_names = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for day, day_stats in best_days[:2]:
            for hour, hour_stats in best_hours[:3]:
                recommendations.append({
                    'day_of_week': day,
                    'day_name': day_names[day],
                    'hour': hour,
                    'time_display': f"{day_names[day]} às {hour:02d}:00",
                    'reason': f"Baseado em {day_stats['count']} posts com boa performance",
                    'confidence': min(day_stats['count'] / 10, 1.0)  # Confidence based on sample size
                })
        
        return recommendations[:top_n]
        
    except Exception as e:
        logger.error(f"Error analyzing best posting times: {e}")
        return get_default_best_times()


def get_default_best_times() -> List[Dict]:
    """
    Return default best posting times based on LinkedIn best practices
    """
    return [
        {
            'day_of_week': 1,  # Tuesday
            'day_name': 'Terça',
            'hour': 9,
            'time_display': 'Terça às 09:00',
            'reason': 'Horário de pico no LinkedIn (melhores práticas)',
            'confidence': 0.7
        },
        {
            'day_of_week': 2,  # Wednesday
            'day_name': 'Quarta',
            'hour': 10,
            'time_display': 'Quarta às 10:00',
            'reason': 'Alto engajamento no meio da semana',
            'confidence': 0.7
        },
        {
            'day_of_week': 3,  # Thursday
            'day_name': 'Quinta',
            'hour': 14,
            'time_display': 'Quinta às 14:00',
            'reason': 'Boa taxa de visualização após almoço',
            'confidence': 0.6
        },
        {
            'day_of_week': 1,  # Tuesday
            'day_name': 'Terça',
            'hour': 17,
            'time_display': 'Terça às 17:00',
            'reason': 'Profissionais checando LinkedIn após expediente',
            'confidence': 0.6
        },
        {
            'day_of_week': 4,  # Friday
            'day_name': 'Sexta',
            'hour': 11,
            'time_display': 'Sexta às 11:00',
            'reason': 'Engajamento antes do fim de semana',
            'confidence': 0.5
        }
    ]


def convert_to_utc(local_time: datetime, timezone_str: str) -> datetime:
    """
    Convert local time to UTC
    
    Args:
        local_time: Local datetime
        timezone_str: Timezone string (e.g., 'America/Sao_Paulo')
        
    Returns:
        UTC datetime
    """
    try:
        local_tz = pytz.timezone(timezone_str)
        local_dt = local_tz.localize(local_time)
        utc_dt = local_dt.astimezone(pytz.UTC)
        return utc_dt
    except Exception as e:
        logger.error(f"Error converting timezone: {e}")
        return local_time


def convert_from_utc(utc_time: datetime, timezone_str: str) -> datetime:
    """
    Convert UTC time to local timezone
    
    Args:
        utc_time: UTC datetime
        timezone_str: Target timezone string
        
    Returns:
        Local datetime
    """
    try:
        target_tz = pytz.timezone(timezone_str)
        if utc_time.tzinfo is None:
            utc_time = pytz.UTC.localize(utc_time)
        local_dt = utc_time.astimezone(target_tz)
        return local_dt
    except Exception as e:
        logger.error(f"Error converting from UTC: {e}")
        return utc_time


# Global scheduler instance
_scheduler_instance = None

def get_scheduler() -> PostScheduler:
    """Get or create the global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = PostScheduler()
    return _scheduler_instance


def start_scheduler():
    """Start the global scheduler"""
    scheduler = get_scheduler()
    if not scheduler.is_running:
        scheduler.start()
    return scheduler
