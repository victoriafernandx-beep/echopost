import google.generativeai as genai
import streamlit as st
from src import database

def configure_genai():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return True
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
    """Generate a post using Gemini AI"""
    
    if not configure_genai():
        return "Erro: Chave de API não configurada."

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    style_context = get_style_examples()
    
    prompt = f"""
    Atue como um especialista em LinkedIn e criador de conteúdo viral.
    
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
    
    Escreva o post agora:
    """
    
    try:
        with st.spinner('🤖 A IA está pensando e escrevendo...'):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Erro ao gerar conteúdo: {str(e)}\n\nVerifique sua API Key."

