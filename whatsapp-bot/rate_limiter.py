"""
Simple in-memory rate limiter for WhatsApp bot
Limits users to 5 messages per minute
"""
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_messages=5, time_window=60):
        """
        Args:
            max_messages: Maximum messages allowed in time window
            time_window: Time window in seconds (default 60s = 1 minute)
        """
        self.max_messages = max_messages
        self.time_window = time_window
        self.user_messages = defaultdict(list)
    
    def is_allowed(self, user_id):
        """
        Check if user is allowed to send a message
        
        Args:
            user_id: User phone number
            
        Returns:
            tuple: (allowed: bool, remaining: int)
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.time_window)
        
        # Remove old messages
        self.user_messages[user_id] = [
            msg_time for msg_time in self.user_messages[user_id]
            if msg_time > cutoff_time
        ]
        
        # Check if under limit
        message_count = len(self.user_messages[user_id])
        
        if message_count < self.max_messages:
            self.user_messages[user_id].append(now)
            remaining = self.max_messages - message_count - 1
            return True, remaining
        else:
            return False, 0
    
    def get_wait_time(self, user_id):
        """
        Get seconds until user can send next message
        
        Args:
            user_id: User phone number
            
        Returns:
            int: Seconds to wait
        """
        if not self.user_messages[user_id]:
            return 0
        
        oldest_message = min(self.user_messages[user_id])
        wait_until = oldest_message + timedelta(seconds=self.time_window)
        wait_seconds = (wait_until - datetime.now()).total_seconds()
        
        return max(0, int(wait_seconds))
