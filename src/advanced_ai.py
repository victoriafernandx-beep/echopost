"""
Advanced AI features for EchoPost
Includes: Sentiment Analysis, Post Variations, Real-time Suggestions, Engagement Prediction
"""
import openai
import streamlit as st
import re
from typing import List, Dict, Tuple


def configure_openai():
    """Configure OpenAI client"""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key:
            return None
        return openai.OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Erro na configuração da IA: {e}")
        return None


def analyze_sentiment(content: str) -> Dict[str, any]:
    """
    Analyze the emotional tone of the post
    
    Returns:
        dict: {
            'sentiment': 'positive' | 'neutral' | 'negative',
            'score': float (0-100),
            'emotion': str (specific emotion like 'inspirational', 'informative', etc),
            'confidence': float (0-1)
        }
    """
    client = configure_openai()
    if not client:
        return {
            'sentiment': 'neutral',
            'score': 50,
            'emotion': 'informativo',
            'confidence': 0.0
        }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em análise de sentimento para posts de LinkedIn."
                },
                {
                    "role": "user",
                    "content": f"""Analise o sentimento deste post de LinkedIn:

"{content}"

Retorne APENAS um JSON válido com esta estrutura exata:
{{
    "sentiment": "positive" ou "neutral" ou "negative",
    "score": número de 0 a 100,
    "emotion": uma palavra descrevendo a emoção (ex: "inspirador", "informativo", "crítico", "motivacional"),
    "confidence": número de 0 a 1
}}

Não adicione explicações, apenas o JSON."""
                }
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        result_text = re.sub(r'```json\s*|\s*```', '', result_text).strip()
        
        import json
        result = json.loads(result_text)
        return result
        
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {
            'sentiment': 'neutral',
            'score': 50,
            'emotion': 'informativo',
            'confidence': 0.0
        }


def generate_variations(content: str, topic: str, num_variations: int = 3) -> List[Dict[str, str]]:
    """
    Generate multiple variations of the same post with different tones
    
    Returns:
        list: [
            {'style': 'Storytelling', 'content': '...'},
            {'style': 'Lista', 'content': '...'},
            {'style': 'Provocativo', 'content': '...'}
        ]
    """
    client = configure_openai()
    if not client:
        return []
    
    styles = [
        {
            'name': 'Storytelling',
            'description': 'Narrativa pessoal, começa com uma história ou experiência'
        },
        {
            'name': 'Lista Direta',
            'description': 'Formato de lista numerada, direto ao ponto'
        },
        {
            'name': 'Provocativo',
            'description': 'Começa com uma afirmação controversa ou pergunta provocativa'
        },
        {
            'name': 'Dados & Insights',
            'description': 'Baseado em estatísticas, dados e insights analíticos'
        }
    ]
    
    variations = []
    
    for style in styles[:num_variations]:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em criar posts virais para LinkedIn."
                    },
                    {
                        "role": "user",
                        "content": f"""Reescreva este post sobre "{topic}" no estilo: {style['name']}

Post original:
{content}

Estilo desejado: {style['description']}

Diretrizes:
- Mantenha o mesmo tema e mensagem principal
- Use o estilo {style['name']} de forma marcante
- 500-1000 caracteres
- Inclua emojis apropriados (2-4)
- Termine com CTA ou pergunta
- Adicione 3-5 hashtags relevantes

Escreva APENAS o novo post, sem título ou explicações."""
                    }
                ],
                temperature=0.8
            )
            
            variation_content = response.choices[0].message.content.strip()
            variations.append({
                'style': style['name'],
                'content': variation_content
            })
            
        except Exception as e:
            print(f"Error generating variation {style['name']}: {e}")
            continue
    
    return variations


def get_realtime_suggestions(content: str) -> List[Dict[str, str]]:
    """
    Get real-time suggestions to improve the post
    
    Returns:
        list: [
            {'type': 'warning' | 'tip' | 'success', 'message': '...'},
            ...
        ]
    """
    suggestions = []
    
    # Basic checks (fast, no AI needed)
    word_count = len(content.split())
    char_count = len(content)
    
    # Length checks
    if char_count < 100:
        suggestions.append({
            'type': 'warning',
            'message': '⚠️ Post muito curto. Posts com 500-1000 caracteres tendem a ter melhor engajamento.'
        })
    elif char_count > 3000:
        suggestions.append({
            'type': 'warning',
            'message': '⚠️ Post muito longo. LinkedIn trunca posts acima de 3000 caracteres.'
        })
    elif 500 <= char_count <= 1500:
        suggestions.append({
            'type': 'success',
            'message': '✅ Tamanho ideal! Posts entre 500-1500 caracteres performam melhor.'
        })
    
    # Emoji check
    emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', content))
    if emoji_count == 0:
        suggestions.append({
            'type': 'tip',
            'message': '💡 Considere adicionar 2-4 emojis para tornar o post mais visual.'
        })
    elif emoji_count > 10:
        suggestions.append({
            'type': 'warning',
            'message': '⚠️ Muitos emojis podem parecer não profissional. Tente usar 2-4.'
        })
    
    # Hashtag check
    hashtag_count = len(re.findall(r'#\w+', content))
    if hashtag_count == 0:
        suggestions.append({
            'type': 'tip',
            'message': '💡 Adicione 3-5 hashtags relevantes para aumentar o alcance.'
        })
    elif hashtag_count > 10:
        suggestions.append({
            'type': 'warning',
            'message': '⚠️ Muitas hashtags podem parecer spam. Use 3-5 hashtags relevantes.'
        })
    elif 3 <= hashtag_count <= 5:
        suggestions.append({
            'type': 'success',
            'message': '✅ Número ideal de hashtags!'
        })
    
    # CTA check
    cta_patterns = [
        r'\?$',  # Ends with question
        r'(o que você acha|qual sua opinião|compartilhe|comente|concorda)',
        r'(vamos conversar|me conte|deixe um comentário)'
    ]
    has_cta = any(re.search(pattern, content.lower()) for pattern in cta_patterns)
    if not has_cta:
        suggestions.append({
            'type': 'tip',
            'message': '💡 Termine com uma pergunta ou CTA para gerar engajamento.'
        })
    
    # Line breaks check
    line_breaks = content.count('\n\n')
    if line_breaks < 2 and char_count > 300:
        suggestions.append({
            'type': 'tip',
            'message': '💡 Use parágrafos curtos e espaçamento para melhorar a leitura.'
        })
    
    return suggestions


def predict_engagement(content: str, topic: str) -> Dict[str, any]:
    """
    Predict potential engagement based on content patterns
    
    Returns:
        dict: {
            'score': int (0-100),
            'level': 'baixo' | 'médio' | 'alto' | 'viral',
            'factors': {
                'length': int (0-100),
                'structure': int (0-100),
                'hooks': int (0-100),
                'cta': int (0-100),
                'hashtags': int (0-100)
            },
            'recommendations': List[str]
        }
    """
    factors = {}
    recommendations = []
    
    # Length factor
    char_count = len(content)
    if 500 <= char_count <= 1500:
        factors['length'] = 100
    elif 300 <= char_count < 500 or 1500 < char_count <= 2000:
        factors['length'] = 70
    else:
        factors['length'] = 40
        if char_count < 300:
            recommendations.append("Aumente o tamanho do post para 500-1500 caracteres")
        else:
            recommendations.append("Reduza o tamanho do post para 500-1500 caracteres")
    
    # Structure factor (paragraphs, line breaks)
    line_breaks = content.count('\n\n')
    if line_breaks >= 3:
        factors['structure'] = 100
    elif line_breaks >= 1:
        factors['structure'] = 60
    else:
        factors['structure'] = 30
        recommendations.append("Use mais parágrafos curtos para melhorar a leitura")
    
    # Hook factor (strong opening)
    first_line = content.split('\n')[0] if '\n' in content else content[:100]
    hook_patterns = [
        r'^(você sabia|imagine|e se|já pensou)',
        r'\?',  # Question
        r'^\d+',  # Starts with number
        r'(nunca|sempre|todos|ninguém)',  # Absolutes
    ]
    has_hook = any(re.search(pattern, first_line.lower()) for pattern in hook_patterns)
    factors['hooks'] = 100 if has_hook else 50
    if not has_hook:
        recommendations.append("Comece com um gancho forte (pergunta, número, afirmação)")
    
    # CTA factor
    cta_patterns = [
        r'\?$',
        r'(o que você acha|qual sua opinião|compartilhe|comente)',
    ]
    has_cta = any(re.search(pattern, content.lower()) for pattern in cta_patterns)
    factors['cta'] = 100 if has_cta else 40
    if not has_cta:
        recommendations.append("Adicione uma pergunta ou CTA no final")
    
    # Hashtags factor
    hashtag_count = len(re.findall(r'#\w+', content))
    if 3 <= hashtag_count <= 5:
        factors['hashtags'] = 100
    elif 1 <= hashtag_count < 3 or 5 < hashtag_count <= 8:
        factors['hashtags'] = 70
    else:
        factors['hashtags'] = 40
        if hashtag_count == 0:
            recommendations.append("Adicione 3-5 hashtags relevantes")
        elif hashtag_count > 8:
            recommendations.append("Reduza para 3-5 hashtags")
    
    # Calculate overall score
    overall_score = sum(factors.values()) // len(factors)
    
    # Determine level
    if overall_score >= 85:
        level = 'viral'
    elif overall_score >= 70:
        level = 'alto'
    elif overall_score >= 50:
        level = 'médio'
    else:
        level = 'baixo'
    
    return {
        'score': overall_score,
        'level': level,
        'factors': factors,
        'recommendations': recommendations
    }


def analyze_style_dna(content: str) -> Dict[str, any]:
    """
    Analyze the style/DNA of a post to create a reusable profile
    """
    client = configure_openai()
    if not client:
        return {}
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em análise linguística de conteúdo viral."
                },
                {
                    "role": "user",
                    "content": f"""Analise o estilo de escrita deste post e extraia seu "DNA":

"{content}"

Retorne um JSON com:
{{
    "tone": "tom principal (ex: Autoridade, Vulnerável, Humor)",
    "structure": "estrutura (ex: Lista, História, Frase Curta)",
    "keywords": ["três", "palavras", "chave"],
    "emoji_usage": "descrição do uso de emojis"
}}"""
                }
            ]
        )
        
        # Clean and parse JSON
        result_text = response.choices[0].message.content.strip()
        result_text = re.sub(r'```json\s*|\s*```', '', result_text).strip()
        
        import json
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error analyzing style: {e}")
        return {
            "tone": "Profissional",
            "structure": "Padrão",
            "keywords": [],
            "emoji_usage": "Moderado"
        }


def extract_insights_from_transcript(transcript_text: str) -> List[Dict[str, str]]:
    """
    Analyze a meeting transcript and extract potential LinkedIn post ideas
    """
    client = configure_openai()
    if not client:
        return []

    # Limit transcript length to avoid context limits (approx 15k chars)
    truncated_text = transcript_text[:15000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um estrategista de conteúdo para LinkedIn. Sua missão é ler transcrições de reuniões e identificar insights valiosos que podem virar posts."
                },
                {
                    "role": "user",
                    "content": f"""Analise a seguinte transcrição de reunião e extraia 3 a 5 ideias de posts para o LinkedIn.
                    
                    Foque em:
                    1. Insights de negócios ou liderança
                    2. Soluções técnicas interessantes discutidas
                    3. Aprendizados ou 'Aha moments'
                    4. Decisões estratégicas (sem revelar segredos industriais)

                    Transcrição:
                    "{truncated_text}..."

                    Retorne APENAS um JSON válido (lista de objetos) com este formato:
                    [
                        {{
                            "topic": "Título curto do tópico",
                            "summary": "Resumo do que foi discutido sobre isso e por que é relevante",
                            "angle": "Ângulo sugerido (ex: Educativo, Provocativo, Bastidores)"
                        }}
                    ]"""
                }
            ],
            temperature=0.7
        )
        
        result_text = response.choices[0].message.content.strip()
        result_text = re.sub(r'```json\s*|\s*```', '', result_text).strip()
        
        import json
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error extracting insights: {e}")
        return []
