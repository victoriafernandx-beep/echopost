import google.generativeai as genai
import streamlit as st

def configure_genai():
    # genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    pass

def generate_post(topic, tone="Professional"):
    """Generate a post template based on topic and tone"""
    
    # Different templates based on tone
    if tone == "Profissional":
        return f"""🎯 {topic}

[Compartilhe sua perspectiva sobre este tema]

💡 Principais pontos:
• [Ponto 1]
• [Ponto 2]
• [Ponto 3]

O que você acha sobre isso?

#LinkedIn #Profissional"""
    
    elif tone == "Casual":
        return f"""Hey! Vamos falar sobre {topic}? 👋

[Conte sua história ou experiência]

Já passaram por isso também?

#Networking #Compartilhando"""
    
    elif tone == "Inspiracional":
        return f"""✨ {topic}

[Compartilhe uma lição ou insight inspirador]

Lembre-se: [Mensagem motivacional]

Qual sua maior lição sobre isso? 💭

#Inspiracao #Crescimento"""
    
    else:
        return f"""📝 {topic}

[Escreva seu conteúdo aqui]

[Adicione detalhes, exemplos ou insights]

[Finalize com uma pergunta ou call-to-action]

#LinkedIn"""

