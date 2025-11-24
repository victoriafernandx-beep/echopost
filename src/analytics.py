"""
Analytics module for EchoPost
Provides metrics and analytics data (currently mock data)
"""
import random
from datetime import datetime, timedelta

def get_metrics():
    """
    Returns mock metrics for dashboard
    In production, this would fetch real data from LinkedIn API
    """
    return {
        "followers": 15230,
        "followers_change": "+120",
        "impressions": 45000,
        "impressions_change": "+15%",
        "engagement": 4.8,
        "engagement_change": "+0.7%",
        "total_posts": 34,
        "posts_change": "+5"
    }

def get_popular_posts():
    """
    Returns mock data for popular posts table
    In production, this would fetch real engagement data
    """
    posts = [
        {
            "title": "A verdade sobre IA",
            "impressions": 15400,
            "comments": 145,
            "shares": 340,
            "engagement": "4.9%"
        },
        {
            "title": "5 dicas de Vendas",
            "impressions": 12300,
            "comments": 88,
            "shares": 120,
            "engagement": "3.2%"
        },
        {
            "title": "Minha História",
            "impressions": 8800,
            "comments": 230,
            "shares": 56,
            "engagement": "8.1%"
        },
        {
            "title": "Erro Comum no MKT",
            "impressions": 4500,
            "comments": 45,
            "shares": 89,
            "engagement": "2.1%"
        },
        {
            "title": "Futuro do Trabalho",
            "impressions": 2200,
            "comments": 32,
            "shares": 12,
            "engagement": "1.9%"
        }
    ]
    return posts

def get_engagement_chart_data():
    """
    Returns mock data for engagement chart
    In production, this would fetch historical data
    """
    dates = []
    engagement = []
    
    for i in range(30, 0, -1):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime("%d/%m"))
        engagement.append(round(random.uniform(3.5, 6.5), 1))
    
    return dates, engagement
