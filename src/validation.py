"""
Input validation for EchoPost
"""
import re

def validate_topic(topic: str) -> str:
    """
    Validate and sanitize topic input
    
    Args:
        topic: User provided topic
        
    Returns:
        Sanitized topic
        
    Raises:
        ValueError: If topic is invalid
    """
    if not topic:
        raise ValueError("Topic cannot be empty")
        
    # Check length
    if len(topic) > 500:
        raise ValueError("Topic is too long (max 500 characters)")
        
    # Check for prompt injection patterns
    # This is not exhaustive but catches common attempts
    suspicious_patterns = [
        r'ignore previous',
        r'system prompt',
        r'jailbreak',
        r'admin mode',
        r'bypass security'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, topic, re.IGNORECASE):
             raise ValueError("Topic contains invalid content")
             
    # Basic sanitization (strip whitespace, control chars)
    sanitized = topic.strip()
    return sanitized

def validate_content_length(content: str, max_length: int = 5000) -> bool:
    """Check text content length"""
    if len(content) > max_length:
        return False
    return True
