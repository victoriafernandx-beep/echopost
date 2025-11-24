"""
Analytics module for EchoPost
Provides metrics and analytics data with period filtering
"""
import random
from datetime import datetime, timedelta

def get_metrics(period_days=30):
    """
    Returns metrics for specified period
    period_days: 7, 30, 90, or 365
    """
    # Base metrics (would come from real data)
    base_followers = 15230
    base_impressions = 45000
    base_engagement = 4.8
    base_posts = 34
    
    # Adjust based on period
    period_multiplier = period_days / 30
    
    # Calculate previous period for comparison
    prev_followers = base_followers - random.randint(50, 200)
    prev_impressions = int(base_impressions * 0.85)
    prev_engagement = base_engagement - random.uniform(0.3, 0.8)
    prev_posts = max(1, int(base_posts * 0.7))
    
    # Calculate changes
    followers_change = base_followers - prev_followers
    impressions_change = ((base_impressions - prev_impressions) / prev_impressions) * 100
    engagement_change = ((base_engagement - prev_engagement) / prev_engagement) * 100
    posts_change = base_posts - prev_posts
    
    return {
        "period_days": period_days,
        "followers": base_followers,
        "followers_change": f"+{followers_change}",
        "followers_percent": f"+{(followers_change/prev_followers*100):.1f}%",
        "impressions": int(base_impressions * period_multiplier),
        "impressions_change": f"+{impressions_change:.1f}%",
        "engagement": base_engagement,
        "engagement_change": f"+{engagement_change:.1f}%",
        "total_posts": base_posts,
        "posts_change": f"+{posts_change}",
        # Previous period data
        "prev_followers": prev_followers,
        "prev_impressions": prev_impressions,
        "prev_engagement": prev_engagement,
        "prev_posts": prev_posts
    }

def get_popular_posts():
    """Returns mock data for popular posts table"""
    posts = [
        {"title": "A verdade sobre IA", "impressions": 15400, "comments": 145, "shares": 340, "engagement": "4.9%"},
        {"title": "5 dicas de Vendas", "impressions": 12300, "comments": 88, "shares": 120, "engagement": "3.2%"},
        {"title": "Minha História", "impressions": 8800, "comments": 230, "shares": 56, "engagement": "8.1%"},
        {"title": "Erro Comum no MKT", "impressions": 4500, "comments": 45, "shares": 89, "engagement": "2.1%"},
        {"title": "Futuro do Trabalho", "impressions": 2200, "comments": 32, "shares": 12, "engagement": "1.9%"}
    ]
    return posts

def get_engagement_chart_data(period_days=30):
    """Returns engagement data for specified period"""
    dates = []
    engagement = []
    
    for i in range(period_days, 0, -1):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime("%d/%m"))
        engagement.append(round(random.uniform(3.5, 6.5), 1))
    
    return dates, engagement

def get_insights(metrics):
    """Generate automatic insights based on metrics"""
    insights = []
    
    # Follower growth insight
    if metrics['followers'] > metrics['prev_followers']:
        growth = metrics['followers'] - metrics['prev_followers']
        insights.append({
            "icon": "📈",
            "title": "Crescimento de Seguidores",
            "description": f"Você ganhou {growth} novos seguidores neste período!",
            "type": "positive"
        })
    
    # Engagement insight
    if metrics['engagement'] > metrics['prev_engagement']:
        insights.append({
            "icon": "🔥",
            "title": "Engajamento em Alta",
            "description": f"Sua taxa de engajamento aumentou {metrics['engagement_change']}!",
            "type": "positive"
        })
    else:
        insights.append({
            "icon": "💡",
            "title": "Oportunidade de Melhoria",
            "description": "Tente adicionar mais perguntas e CTAs nos posts.",
            "type": "tip"
        })
    
    # Post frequency insight
    if metrics['total_posts'] > metrics['prev_posts']:
        insights.append({
            "icon": "✅",
            "title": "Consistência",
            "description": f"Você publicou {metrics['posts_change']} posts a mais que o período anterior!",
            "type": "positive"
        })
    else:
        insights.append({
            "icon": "⏰",
            "title": "Frequência de Posts",
            "description": "Postar com mais frequência pode aumentar seu alcance.",
            "type": "tip"
        })
    
    # Best time insight (mock)
    insights.append({
        "icon": "🕐",
        "title": "Melhor Horário",
        "description": "Seus posts têm mais engajamento entre 9h-11h e 18h-20h.",
        "type": "info"
    })
    
    return insights

def get_post_performance_by_tag():
    """Get performance metrics by tag"""
    return {
        "Vendas": {"posts": 12, "avg_engagement": 5.2, "total_impressions": 45000},
        "Tech": {"posts": 8, "avg_engagement": 6.1, "total_impressions": 38000},
        "Marketing": {"posts": 7, "avg_engagement": 4.8, "total_impressions": 28000},
        "Carreira": {"posts": 5, "avg_engagement": 7.3, "total_impressions": 22000},
        "Liderança": {"posts": 2, "avg_engagement": 4.1, "total_impressions": 8000}
    }
