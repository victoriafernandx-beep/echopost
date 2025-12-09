import os
import sys
import time
from datetime import datetime, timedelta
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit secrets for database connection if needed, 
# but usually it's loaded from .streamlit/secrets.toml by the streamlit lib.
# We might need to ensure we run this in a way that access secrets.
# If running via 'python', streamlit secrets might not be loaded automatically 
# unless we use the streamlit specific loading or mock it.

# Let's try to run it and if it fails on secrets, we'll guide the user.
try:
    from src import database, scheduler
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def verify_scheduling():
    print("🧪 Starting Scheduling Verification...")
    
    user_id = "test_user_verifier"
    
    # 1. Create a post scheduled for the past (so it's ready to publish immediately)
    print("1️⃣ Creating a test scheduled post (scheduled for 1 minute ago)...")
    now_utc = datetime.utcnow()
    past_time = now_utc - timedelta(minutes=1)
    
    try:
        result = database.create_scheduled_post(
            user_id=user_id,
            content="Test scheduled post verification content",
            topic="Verification",
            scheduled_time=past_time.isoformat(),
            timezone="UTC",
            tags=["test", "verification"]
        )
        
        if not result or not result.data:
            print("❌ Failed to create scheduled post.")
            return
            
        post_id = result.data[0]['id']
        print(f"✅ Post created! ID: {post_id}")
        
    except Exception as e:
        print(f"❌ Error creating post: {e}")
        return

    # 2. Run the scheduler check manually
    print("\n2️⃣ Triggering scheduler check manual run...")
    sch = scheduler.get_scheduler()
    
    try:
        # We call the method directly instead of waiting for the background job
        sch.check_and_publish_posts()
        print("✅ Scheduler check completed.")
    except Exception as e:
        print(f"❌ Error running scheduler check: {e}")
        return
        
    # 3. Verify status
    print("\n3️⃣ Verifying post status...")
    posts = database.get_scheduled_posts(user_id)
    target_post = next((p for p in posts if p['id'] == post_id), None)
    
    if target_post:
        status = target_post['status']
        print(f"📊 Final Post Status: {status}")
        
        if status == 'published':
            print("🎉 SUCCESS! Post was picked up and marked as published.")
        elif status == 'failed':
            print("⚠️ Post marked as FAILED. This is expected if specific auth is missing, but logic worked!")
            print(f"   Error message: {target_post.get('error_message')}")
        else:
            print(f"❌ FAILURE. Post status is still '{status}'. It should be published or failed.")
    else:
        print("❌ Could not find the post in database.")

if __name__ == "__main__":
    verify_scheduling()
