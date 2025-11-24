"""
AI Helper functions for content enhancement
"""
import re

def suggest_hashtags(content, topic):
    """
    Suggest relevant hashtags based on content and topic
    In production, this could use AI to analyze content
    """
    # Extract keywords from topic
    keywords = topic.lower().split()
    
    # Common professional hashtags
    professional_tags = [
        "#LinkedIn", "#Networking", "#ProfessionalGrowth",
        "#CareerDevelopment", "#Business", "#Leadership"
    ]
    
    # Topic-specific suggestions
    topic_tags = []
    if any(word in topic.lower() for word in ["ia", "inteligência artificial", "ai"]):
        topic_tags = ["#InteligenciaArtificial", "#AI", "#MachineLearning", "#Tech"]
    elif any(word in topic.lower() for word in ["vendas", "sales"]):
        topic_tags = ["#Vendas", "#Sales", "#B2B", "#Negociacao"]
    elif any(word in topic.lower() for word in ["marketing", "mkt"]):
        topic_tags = ["#Marketing", "#MarketingDigital", "#Branding", "#ContentMarketing"]
    elif any(word in topic.lower() for word in ["carreira", "trabalho", "emprego"]):
        topic_tags = ["#Carreira", "#DesenvolvimentoProfissional", "#Emprego", "#RH"]
    
    # Combine and return top suggestions
    all_tags = topic_tags + professional_tags[:3]
    return all_tags[:6]  # Return max 6 suggestions

def count_words(text):
    """Count words in text"""
    words = text.split()
    return len(words)

def count_sentences(text):
    """Count sentences in text"""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def analyze_readability(text):
    """
    Simple readability analysis
    Returns: Easy, Medium, or Hard
    """
    words = count_words(text)
    sentences = count_sentences(text)
    
    if sentences == 0:
        return "N/A"
    
    avg_words_per_sentence = words / sentences
    
    if avg_words_per_sentence < 15:
        return "Fácil"
    elif avg_words_per_sentence < 25:
        return "Médio"
    else:
        return "Complexo"

def extract_hashtags(text):
    """Extract existing hashtags from text"""
    return re.findall(r'#\w+', text)
