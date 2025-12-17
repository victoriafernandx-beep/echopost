"""
Multi-Source News Aggregator for EchoPost
Aggregates news from RSS feeds, Google News, and other free sources
"""
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
from urllib.parse import quote_plus

class NewsAggregator:
    """Aggregates news from multiple free sources"""
    
    # RSS Feed Sources
    RSS_SOURCES = {
        'brasil': [
            {'name': 'G1', 'url': 'https://g1.globo.com/rss/g1/'},
            {'name': 'UOL', 'url': 'https://rss.uol.com.br/feed/noticias.xml'},
            {'name': 'Folha', 'url': 'https://feeds.folha.uol.com.br/emcimadahora/rss091.xml'},
            {'name': 'Exame', 'url': 'https://exame.com/feed/'},
        ],
        'tech': [
            {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/'},
            {'name': 'Hacker News', 'url': 'https://news.ycombinator.com/rss'},
            {'name': 'The Verge', 'url': 'https://www.theverge.com/rss/index.xml'},
        ],
        'business': [
            {'name': 'Forbes', 'url': 'https://www.forbes.com/real-time/feed2/'},
            {'name': 'Business Insider', 'url': 'https://www.businessinsider.com/rss'},
        ]
    }
    
    @staticmethod
    def fetch_from_all_sources(topic: str, max_articles: int = 20, language: str = 'pt') -> List[Dict]:
        """
        Fetch news from all available sources
        
        Args:
            topic: Search topic
            max_articles: Maximum number of articles to return
            language: Language code ('pt' or 'en')
            
        Returns:
            List of article dictionaries
        """
        all_articles = []
        
        # 1. Fetch from Google News (most reliable for topic search)
        google_articles = NewsAggregator.fetch_google_news(topic, language)
        all_articles.extend(google_articles)
        
        # 2. Fetch from relevant RSS feeds based on topic
        category = NewsAggregator._categorize_topic(topic)
        if category and category in NewsAggregator.RSS_SOURCES:
            rss_articles = NewsAggregator.fetch_rss_feeds(NewsAggregator.RSS_SOURCES[category])
            all_articles.extend(rss_articles)
        
        # 3. Deduplicate
        unique_articles = NewsAggregator.deduplicate_articles(all_articles)
        
        # 4. Filter by topic relevance
        relevant_articles = NewsAggregator._filter_by_relevance(unique_articles, topic)
        
        # 5. Sort by date (newest first)
        sorted_articles = sorted(relevant_articles, key=lambda x: x.get('published_date', ''), reverse=True)
        
        return sorted_articles[:max_articles]
    
    @staticmethod
    def fetch_google_news(topic: str, language: str = 'pt') -> List[Dict]:
        """
        Fetch news from Google News RSS
        
        Args:
            topic: Search topic
            language: Language code
            
        Returns:
            List of articles
        """
        try:
            # Google News RSS URL
            encoded_topic = quote_plus(topic)
            
            if language == 'pt':
                url = f'https://news.google.com/rss/search?q={encoded_topic}&hl=pt-BR&gl=BR&ceid=BR:pt-419'
            else:
                url = f'https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en'
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:15]:  # Limit to 15 from Google News
                article = {
                    'title': entry.get('title', 'Sem título'),
                    'description': entry.get('summary', '')[:200] + '...' if entry.get('summary') else '',
                    'url': entry.get('link', ''),
                    'source': {'name': 'Google News'},
                    'published_date': entry.get('published', ''),
                    'content_hash': NewsAggregator._hash_content(entry.get('title', '') + entry.get('link', ''))
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error fetching Google News: {e}")
            return []
    
    @staticmethod
    def fetch_rss_feeds(sources: List[Dict]) -> List[Dict]:
        """
        Fetch articles from RSS feed sources
        
        Args:
            sources: List of source dictionaries with 'name' and 'url'
            
        Returns:
            List of articles
        """
        articles = []
        
        for source in sources:
            try:
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:5]:  # Limit to 5 per source
                    article = {
                        'title': entry.get('title', 'Sem título'),
                        'description': entry.get('summary', '')[:200] + '...' if entry.get('summary') else '',
                        'url': entry.get('link', ''),
                        'source': {'name': source['name']},
                        'published_date': entry.get('published', ''),
                        'content_hash': NewsAggregator._hash_content(entry.get('title', '') + entry.get('link', ''))
                    }
                    articles.append(article)
                    
            except Exception as e:
                print(f"Error fetching RSS from {source['name']}: {e}")
                continue
        
        return articles
    
    @staticmethod
    def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
        """
        Remove duplicate articles based on content hash
        
        Args:
            articles: List of articles
            
        Returns:
            Deduplicated list
        """
        seen_hashes = set()
        unique_articles = []
        
        for article in articles:
            content_hash = article.get('content_hash')
            if content_hash and content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_articles.append(article)
        
        return unique_articles
    
    @staticmethod
    def _hash_content(content: str) -> str:
        """Generate hash for content deduplication"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def _categorize_topic(topic: str) -> Optional[str]:
        """
        Categorize topic to select relevant RSS feeds
        
        Args:
            topic: Search topic
            
        Returns:
            Category name or None
        """
        topic_lower = topic.lower()
        
        # Tech keywords
        tech_keywords = ['tecnologia', 'tech', 'ia', 'inteligência artificial', 'software', 'startup', 'app']
        if any(keyword in topic_lower for keyword in tech_keywords):
            return 'tech'
        
        # Business keywords
        business_keywords = ['negócios', 'business', 'economia', 'mercado', 'empresa', 'investimento']
        if any(keyword in topic_lower for keyword in business_keywords):
            return 'business'
        
        # Default to Brazil news
        return 'brasil'
    
    @staticmethod
    def _filter_by_relevance(articles: List[Dict], topic: str) -> List[Dict]:
        """
        Filter articles by topic relevance (simple keyword matching)
        
        Args:
            articles: List of articles
            topic: Search topic
            
        Returns:
            Filtered list
        """
        topic_keywords = topic.lower().split()
        relevant_articles = []
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            # Check if any topic keyword appears in title or description
            if any(keyword in title or keyword in description for keyword in topic_keywords):
                relevant_articles.append(article)
        
        # If no relevant articles found, return all (better than nothing)
        return relevant_articles if relevant_articles else articles
    
    @staticmethod
    def format_for_display(article: Dict) -> str:
        """Format article for display in UI"""
        return f"""
**{article['title']}**
📰 Fonte: {article['source']['name']}
📅 {article.get('published_date', 'Data não disponível')}

{article['description']}

[Ler mais]({article['url']})
"""
