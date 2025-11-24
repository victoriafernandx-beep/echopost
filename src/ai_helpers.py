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

def score_content(text):
    """
    Score content based on LinkedIn best practices
    Returns score (0-100) and feedback list
    """
    score = 0
    feedback = []
    
    # 1. Length check (20 points)
    word_count = count_words(text)
    if 50 <= word_count <= 150:
        score += 20
        feedback.append("✅ Tamanho ideal (50-150 palavras)")
    elif word_count < 50:
        score += 10
        feedback.append("⚠️ Post muito curto (ideal: 50-150 palavras)")
    else:
        score += 15
        feedback.append("⚠️ Post muito longo (ideal: 50-150 palavras)")
    
    # 2. Hashtags (15 points)
    hashtags = extract_hashtags(text)
    if 3 <= len(hashtags) <= 5:
        score += 15
        feedback.append("✅ Quantidade ideal de hashtags (3-5)")
    elif len(hashtags) == 0:
        feedback.append("❌ Adicione hashtags (3-5 recomendado)")
    elif len(hashtags) < 3:
        score += 8
        feedback.append("⚠️ Poucas hashtags (3-5 recomendado)")
    else:
        score += 8
        feedback.append("⚠️ Muitas hashtags (3-5 recomendado)")
    
    # 3. Emojis (10 points)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE)
    emojis = emoji_pattern.findall(text)
    if 1 <= len(emojis) <= 3:
        score += 10
        feedback.append("✅ Uso adequado de emojis")
    elif len(emojis) == 0:
        score += 5
        feedback.append("💡 Considere adicionar 1-2 emojis")
    else:
        score += 5
        feedback.append("⚠️ Muitos emojis podem distrair")
    
    # 4. Question (15 points)
    if '?' in text:
        score += 15
        feedback.append("✅ Contém pergunta (engaja audiência)")
    else:
        feedback.append("💡 Adicione uma pergunta para engajar")
    
    # 5. Call to action (15 points)
    cta_keywords = ['comente', 'compartilhe', 'marque', 'siga', 'clique', 'saiba mais', 'confira', 'veja']
    if any(keyword in text.lower() for keyword in cta_keywords):
        score += 15
        feedback.append("✅ Tem call-to-action")
    else:
        feedback.append("💡 Adicione um call-to-action")
    
    # 6. Paragraphs (10 points)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) >= 2:
        score += 10
        feedback.append("✅ Bem formatado em parágrafos")
    else:
        score += 5
        feedback.append("💡 Divida em parágrafos para melhor leitura")
    
    # 7. Readability (15 points)
    readability = analyze_readability(text)
    if readability in ["Fácil", "Médio"]:
        score += 15
        feedback.append(f"✅ Leitura {readability.lower()}")
    else:
        score += 8
        feedback.append("⚠️ Texto complexo, simplifique")
    
    return score, feedback

