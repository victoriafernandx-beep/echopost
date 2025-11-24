"""
Templates library for quick post creation
"""

TEMPLATES = {
    "Vendas": [
        {
            "title": "Dica de Vendas",
            "content": """🎯 Dica de vendas que mudou meu jogo:

[Sua dica aqui]

Resultado? [Seu resultado]

Qual sua melhor técnica de vendas? 👇

#Vendas #Sales #Negociacao"""
        },
        {
            "title": "Case de Sucesso",
            "content": """💼 Case de sucesso que quero compartilhar:

Cliente: [Nome/Setor]
Desafio: [Problema]
Solução: [O que fizemos]
Resultado: [Números/Impacto]

Aprendizado: [Lição principal]

#CaseDeSuccesso #Vendas #Resultados"""
        }
    ],
    "Tecnologia": [
        {
            "title": "Novidade Tech",
            "content": """🚀 Acabei de descobrir [tecnologia/ferramenta]:

Por que é interessante:
• [Benefício 1]
• [Benefício 2]
• [Benefício 3]

Já usaram? Compartilhem suas experiências! 💬

#Tech #Tecnologia #Inovacao"""
        },
        {
            "title": "Aprendizado Técnico",
            "content": """💡 Aprendi algo importante sobre [tema]:

O problema: [Contexto]
A solução: [O que descobri]
O resultado: [Impacto]

Espero que ajude alguém! 🙌

#Programacao #DevLife #AprendizadoContinuo"""
        }
    ],
    "Carreira": [
        {
            "title": "Lição de Carreira",
            "content": """📈 Lição de carreira que levei anos para aprender:

[Sua lição]

Se eu pudesse voltar no tempo, diria para mim mesmo: [Conselho]

Qual lição você gostaria de ter aprendido antes? 

#Carreira #DesenvolvimentoProfissional #Crescimento"""
        },
        {
            "title": "Conquista Profissional",
            "content": """🎉 Conquista desbloqueada!

[Sua conquista]

Jornada:
→ [Passo 1]
→ [Passo 2]
→ [Passo 3]

Gratidão a todos que me apoiaram! 🙏

#Conquista #Carreira #Gratidao"""
        }
    ],
    "Marketing": [
        {
            "title": "Estratégia de Marketing",
            "content": """📊 Estratégia de marketing que funcionou:

Objetivo: [Meta]
Ação: [O que fizemos]
Resultado: [Números]

Dica: [Insight principal]

Testaram algo parecido? 

#Marketing #MarketingDigital #Estrategia"""
        },
        {
            "title": "Tendência de Mercado",
            "content": """🔥 Tendência que estou observando:

[Tendência]

Por que importa:
1. [Razão 1]
2. [Razão 2]
3. [Razão 3]

Como você está se preparando?

#Tendencias #Marketing #Mercado"""
        }
    ],
    "Liderança": [
        {
            "title": "Lição de Liderança",
            "content": """👥 O que aprendi sobre liderança:

[Sua lição]

Impacto no time: [Resultado]

Líderes, qual sua maior lição? 

#Lideranca #Gestao #Time"""
        },
        {
            "title": "Cultura Organizacional",
            "content": """🏢 Como construímos uma cultura forte:

Valores:
✓ [Valor 1]
✓ [Valor 2]
✓ [Valor 3]

Resultado: [Impacto no time/empresa]

#Cultura #Lideranca #RH"""
        }
    ]
}

def get_categories():
    """Return list of template categories"""
    return list(TEMPLATES.keys())

def get_templates(category):
    """Get templates for a specific category"""
    return TEMPLATES.get(category, [])

def get_all_templates():
    """Get all templates"""
    return TEMPLATES
