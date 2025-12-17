from newsapi import NewsApiClient
import streamlit as st
import datetime

def get_news_api_key():
    """Get NewsAPI key from env or secrets"""
    import os
    # 1. Try env first
    api_key = os.getenv("NEWS_API_KEY")
    if api_key:
        return api_key
    
    # 2. Try secrets with protection
    try:
        if "NEWS_API_KEY" in st.secrets:
            return st.secrets["NEWS_API_KEY"]
    except FileNotFoundError:
        pass
    
    return ""

def fetch_news(topic, language='pt', sort_by='relevancy'):
    """
    Fetch news from NewsAPI
    
    Args:
        topic (str): Topic to search for
        language (str): Language code (default: 'pt')
        sort_by (str): Sort order (relevancy, publishedAt, popularity)
        
    Returns:
        list: List of news articles
    """
    api_key = get_news_api_key()
    
    if not api_key:
        return []
        
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Calculate date range (last 7 days)
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        
        response = newsapi.get_everything(
            q=topic,
            language=language,
            sort_by=sort_by,
            from_param=last_week,
            to=today,
            page_size=12  # Limit to 12 articles
        )
        
        if response['status'] == 'ok':
            articles = response['articles']
            print(f"[DEBUG] Found {len(articles)} articles raw.")
            
            # Filter out articles with removed content
            valid_articles = [
                a for a in articles 
                if a['title'] != '[Removed]' and a['description'] is not None
            ]
            print(f"[DEBUG] Found {len(valid_articles)} valid articles.")
            
            # Fallback: If no articles found and language was specific, try English
            if not valid_articles and language != 'en':
                print("[DEBUG] No articles found. Retrying with English...")
                return fetch_news(topic, language='en', sort_by=sort_by)
                
            return valid_articles
        else:
            print(f"[DEBUG] NewsAPI status: {response.get('status')}, message: {response.get('message')}")
            return []
            
    except Exception as e:
        print(f"Error fetching news: {e}")
        import traceback
        traceback.print_exc()
        return []

def format_news_for_prompt(article):
    """Format news article for AI prompt"""
    return f"""
    TÍTULO: {article['title']}
    FONTE: {article['source']['name']}
    RESUMO: {article['description']}
    URL: {article['url']}
    """
