import openai
import streamlit as st
import re
from src import database

def configure_openai():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key:
            return False
        return api_key
    except Exception as e:
        st.error(f"Erro na configuração da IA: {e}")
        return False

def get_style_examples():
    """Fetch recent posts to use as style examples"""
    try:
        # Get last 3 posts to understand style
        posts = database.get_posts("test_user", limit=3)
        if posts:
            examples = "\n\n".join([f"Exemplo {i+1}:\n{p['content']}" for i, p in enumerate(posts)])
            return f"Aqui estão exemplos do meu estilo de escrita anterior. Tente imitar o tom, formatação e uso de emojis:\n\n{examples}"
        return ""
    except:
        return ""

def generate_post(topic, tone="Profissional"):
    """Generate a post using OpenAI GPT-4o"""
    from src.validation import validate_topic
    
    try:
        topic = validate_topic(topic)
    except ValueError as e:
        return f"Erro: {str(e)}"
    
    api_key = configure_openai()
    if not api_key:
        return "Erro: Chave de API não configurada."

    client = openai.OpenAI(api_key=api_key)
    
    style_context = get_style_examples()
    
    system_prompt = "Você é um especialista em LinkedIn e criador de conteúdo viral."
    
    user_prompt = f"""
    Sua tarefa é escrever um post sobre o tema: "{topic}"
    
    Tom de voz desejado: {tone}
    
    {style_context}
    
    Diretrizes:
    1. Use parágrafos curtos e fáceis de ler.
    2. Comece com um gancho forte (hook) para prender a atenção.
    3. Use emojis estrategicamente (não exagere, 2-4 por post).
    4. Inclua uma lista de pontos chave (bullet points) se fizer sentido.
    5. Termine com uma pergunta para gerar engajamento (CTA).
    6. Adicione 3-5 hashtags relevantes no final.
    7. O post deve ter entre 500-1000 caracteres.
    8. NÃO coloque título "Título:" ou "Assunto:", comece direto no texto.
    9. IMPORTANTE: Escreva APENAS texto puro. NÃO use HTML, tags, comentários ou qualquer código.
    
    Escreva o post agora:
    """
    
    try:
        with st.spinner('🤖 A IA está pensando e escrevendo...'):
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Using mini for speed/cost, can be gpt-4o
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            generated_text = response.choices[0].message.content
            # Strip any HTML tags and comments from the response
            # Clean HTML using bleach (safe sanitization)
            import bleach
            clean_content = bleach.clean(generated_text, tags=[], strip=True)
            # Clean up extra whitespace
            clean_content = re.sub(r'\n\s*\n', '\n\n', clean_content).strip()
            return clean_content
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return f"Erro de Autenticação (401): Sua chave API da OpenAI pode estar inválida. Verifique o arquivo secrets.toml.\nDetalhes: {error_msg}"
        return f"Erro ao gerar conteúdo: {error_msg}\n\nVerifique sua API Key."

