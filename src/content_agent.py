import os
import openai
import streamlit as st
from typing import List, Dict, Any

def get_api_key():
    """Retrieve API key from secrets or environment variables"""
    # 1. Try OS Environment (Prioritize local .env)
    try:
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key:
            return env_key
    except:
        pass

    # 2. Try Streamlit Secrets (Root)
    try:
        # Accessing st.secrets might raise error if no secrets.toml exists
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except:
        pass
        
    # 3. Try Streamlit Secrets (Nested)
    try:
        if "secrets" in st.secrets and "OPENAI_API_KEY" in st.secrets["secrets"]:
            return st.secrets["secrets"]["OPENAI_API_KEY"]
    except:
        pass
        
    return None

import re
import json

def get_agent_response(messages: List[Dict[str, str]], custom_system_prompt: str = None) -> Dict[str, Any]:
    """
    Interact with the Content Strategist Agent.
    It decides whether to ask another question or generate the post.
    """
    print("DEBUG: Calling Agent...")
    try:
        api_key = get_api_key()
        if not api_key:
            return {
                "message": "⚠️ Erro: API Key da OpenAI não encontrada. Verifique secrets.toml ou arquivo .env",
                "is_ready_to_post": False,
                "post_content": None
            }
            
        client = openai.OpenAI(api_key=api_key)
        
        # Default Prompt
        default_prompt = """
        Você é o "Editor Chefe" do EchoPost, um especialista em Personal Branding e Storytelling.
        
        SEU OBJETIVO:
        Ajudar o usuário a criar um post de LinkedIn único, autêntico e viral.
        
        COMO VOCÊ TRABALHA:
        1. Não aceite tópicos genéricos. Se o usuário disser "Liderança", pergunte "Qual foi a decisão mais difícil que você tomou como líder esta semana?".
        2. Faça perguntas qualitativas e provocativas para extrair a "história por trás da história".
        3. Fale de forma breve e direta, como um colega de trabalho sênior.
        4. Faça APENAS UMA pergunta por vez.
        5. Quando sentir que tem informações suficientes (geralmente após 2 ou 3 interações de qualidade), pergunte: "Tenho o suficiente. Quer que eu crie o rascunho agora?"
        6. Se o usuário confirmar, GERE O POST no formato final.
        
        ESTRUTURA DE RESPOSTA (JSON):
        {
            "message": "Sua resposta ou pergunta para o usuário aqui",
            "is_ready_to_post": boolean (true se você acabou de gerar o post final no campo message),
            "post_content": "O conteúdo do post (apenas se is_ready_to_post for true, senão null)"
        }
        """
        
        system_prompt = custom_system_prompt if custom_system_prompt and custom_system_prompt.strip() else default_prompt
        
        # Prepare messages including system prompt
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        print("DEBUG: Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_messages,
            temperature=0.7
        )
        
        raw_content = response.choices[0].message.content.strip()
        # print(f"DEBUG: Raw response: {raw_content[:100]}...") # Commented out to prevent Windows Unicode errors
        
        # Robust JSON extraction
        try:
            # Try finding JSON block between brackets
            match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                # Fallback: maybe the model didn't output JSON?
                return {
                    "message": raw_content,
                    "is_ready_to_post": False,
                    "post_content": None
                }
        except json.JSONDecodeError:
            return {
                "message": f"Erro ao processar resposta da IA. (Conteúdo bruto: {raw_content})",
                "is_ready_to_post": False,
                "post_content": None
            }
        
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        return {
            "message": f"Desculpe, tive um erro técnico. ({str(e)})",
            "is_ready_to_post": False,
            "post_content": None
        }
