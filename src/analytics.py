"""
Analytics module for LinPost
Provides metrics based on internal platform usage
"""
import random
from datetime import datetime, timedelta
from src import database

def get_metrics(period_days=30):
    """
    Returns metrics based on internal database
    """
    user_id = "test_user" # In real app, get from session
    
    # Get all posts
    posts = database.get_posts(user_id)
    
    total_posts = len(posts)
    
    # Calculate posts in period
    now = datetime.now()
    period_start = now - timedelta(days=period_days)
    
    posts_in_period = 0
    posts_prev_period = 0
    prev_period_start = period_start - timedelta(days=period_days)
    
    for post in posts:
        try:
            created_at = datetime.fromisoformat(post['created_at'].replace('Z', '+00:00')).replace(tzinfo=None)
            if created_at >= period_start:
                posts_in_period += 1
            elif created_at >= prev_period_start:
                posts_prev_period += 1
        except:
            pass
            
    # Calculate streak (mock logic for now as we don't have daily data easily)
    streak = random.randint(1, 5) if posts_in_period > 0 else 0
    
    # Calculate average words
    total_words = sum([post.get('word_count', 0) for post in posts])
    avg_words = int(total_words / total_posts) if total_posts > 0 else 0
    
    return {
        "total_posts": total_posts,
        "posts_in_period": posts_in_period,
        "posts_change": posts_in_period - posts_prev_period,
        "streak": streak,
        "avg_words": avg_words,
        "period_days": period_days
    }

def get_posting_activity():
    """Returns data for activity chart"""
    # Mock activity data for the last 30 days
    dates = []
    counts = []
    
    for i in range(30, -1, -1):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime("%d/%m"))
        # Random count 0-3
        counts.append(random.choices([0, 1, 2, 3], weights=[0.6, 0.2, 0.1, 0.1])[0])
        
    return dates, counts

def get_insights(metrics):
    """Generate insights based on usage"""
    insights = []
    
    # Streak insight
    if metrics['streak'] >= 3:
        insights.append({
            "icon": "🔥",
            "title": "On Fire!",
            "description": f"Você está há {metrics['streak']} dias criando conteúdo consecutivamente!",
            "type": "positive"
        })
    else:
        insights.append({
            "icon": "📅",
            "title": "Consistência",
            "description": "Tente criar pelo menos um post por dia para manter o ritmo.",
            "type": "tip"
        })
        
    # Volume insight
    if metrics['posts_in_period'] > 5:
        insights.append({
            "icon": "🚀",
            "title": "Alta Produtividade",
            "description": "Você está criando bastante conteúdo! Continue assim.",
            "type": "positive"
        })
    
    # Word count insight
    if metrics['avg_words'] < 100:
        insights.append({
            "icon": "📝",
            "title": "Posts Curtos",
            "description": "Seus posts são curtos. Tente aprofundar mais nos tópicos.",
            "type": "info"
        })
    elif metrics['avg_words'] > 300:
        insights.append({
            "icon": "✂️",
            "title": "Posts Longos",
            "description": "Cuidado com textos muito longos. Tente ser mais conciso.",
            "type": "tip"
        })
        
    return insights

def get_top_topics(user_id="test_user"):
    """Get most used topics"""
    posts = database.get_posts(user_id)
    topics = {}
    
    for post in posts:
        topic = post.get('topic', 'Outros')
        topics[topic] = topics.get(topic, 0) + 1
        
    # Sort by count
    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    return sorted_topics[:5]

