"""
Resource library for content creation
"""

# Emoji library organized by category
EMOJI_LIBRARY = {
    "Negócios": ["💼", "📊", "📈", "💰", "🎯", "🚀", "💡", "⚡"],
    "Emoções": ["😊", "🎉", "❤️", "🙌", "👏", "💪", "🔥", "✨"],
    "Tecnologia": ["💻", "📱", "🖥️", "⌨️", "🖱️", "💾", "🔧", "⚙️"],
    "Comunicação": ["💬", "📢", "📣", "💭", "🗣️", "📞", "✉️", "📧"],
    "Tempo": ["⏰", "⏱️", "⏳", "📅", "🗓️", "🕐", "🌅", "🌙"],
    "Sucesso": ["🏆", "🥇", "🎖️", "👑", "⭐", "🌟", "💫", "✅"],
    "Aprendizado": ["📚", "📖", "✏️", "📝", "🎓", "🧠", "💭", "🔍"],
    "Pessoas": ["👥", "👤", "👨‍💼", "👩‍💼", "🤝", "👋", "🙋", "💁"]
}

# Call-to-Action library
CTA_LIBRARY = [
    "O que você acha? Comente abaixo! 👇",
    "Compartilhe se você concorda! 🔄",
    "Marque alguém que precisa ver isso! 👥",
    "Qual sua experiência com isso? Conta aqui! 💬",
    "Salvem este post para referência futura! 📌",
    "Siga para mais conteúdo como este! ➕",
    "Clique no link nos comentários para saber mais! 🔗",
    "Reaja se isso fez sentido para você! 👍",
    "Vamos discutir nos comentários? 💭",
    "Compartilhe com seu time! 👥"
]

# Power phrases for engagement
POWER_PHRASES = [
    "Aqui está a verdade que ninguém te conta:",
    "Isso mudou completamente minha perspectiva:",
    "O erro que 90% das pessoas cometem:",
    "A estratégia que triplicou meus resultados:",
    "Se eu pudesse voltar no tempo, faria isso:",
    "O segredo que aprendi depois de [X] anos:",
    "A lição mais valiosa da minha carreira:",
    "Por que isso importa mais do que você pensa:",
    "O que descobri depois de [X] tentativas:",
    "A mudança que fez toda a diferença:"
]

# Hashtag suggestions by topic
HASHTAG_SUGGESTIONS = {
    "Geral": ["#LinkedIn", "#Networking", "#Carreira", "#Profissional"],
    "Negócios": ["#Negocios", "#Empreendedorismo", "#Startups", "#Business"],
    "Tecnologia": ["#Tech", "#Tecnologia", "#Inovacao", "#Digital"],
    "Marketing": ["#Marketing", "#MarketingDigital", "#Branding", "#Conteudo"],
    "Vendas": ["#Vendas", "#Sales", "#Comercial", "#Negociacao"],
    "RH": ["#RH", "#RecursosHumanos", "#Talentos", "#Gestao"],
    "Liderança": ["#Lideranca", "#Gestao", "#Time", "#Cultura"],
    "Desenvolvimento": ["#Programacao", "#Dev", "#Codigo", "#Software"]
}

def get_emoji_categories():
    """Return emoji categories"""
    return list(EMOJI_LIBRARY.keys())

def get_emojis(category):
    """Get emojis for a category"""
    return EMOJI_LIBRARY.get(category, [])

def get_ctas():
    """Get all CTAs"""
    return CTA_LIBRARY

def get_power_phrases():
    """Get all power phrases"""
    return POWER_PHRASES

def get_hashtags(topic):
    """Get hashtags for a topic"""
    return HASHTAG_SUGGESTIONS.get(topic, HASHTAG_SUGGESTIONS["Geral"])

B2B_STRATEGIST_TEMPLATE = """Você é um estrategista de conteúdo B2B especializado em LinkedIn.

SEU ESTILO DE ESCRITA (RITMO E ESTRUTURA):
Você NÃO escreve blocos de texto. Você escreve "poesia corporativa" (frases curtas, ritmo visual).
Inspire-se neste formato exato:

--- EXEMPLO DE ESTRUTURA IDEAL ---
Todo mundo fala de [X].
Pouca gente fala do que vem depois de [X].

Porque [A] não é só [B].
É [C].

[Conceito X] sem [Conceito Y] vira isso aqui:
📈 [Consequência 1]
📉 [Consequência 2]
💸 [Consequência 3]

[Conceito Y] entra exatamente para quebrar esse ciclo.

Enquanto [X] faz [ação],
o [Y] faz algo que o [X] sozinho não faz:
[Insight profundo].

É o [Y] que mostra:
– [Benefício 1]
– [Benefício 2]

[Frase de efeito comparativa].

E quando os dois trabalham juntos:
✔ [Benefício Claro]
✔ [Benefício Claro]

O erro de muita empresa é tratar [X] como [Y].

[Frase final de impacto].
----------------------------------

REGRAS DE OURO:
1. Use dualismos ("Growth descobre o que chama atenção / CRM descobre o que sustenta").
2. Frases curtas. Dê enter a cada 1 ou 2 frases.
3. Use emojis apenas como bullets (📈, 📉, ✔) ou raramente para ênfase.
4. Tom: Sênior, calmo, cirúrgico.

FLUXO DE TRABALHO (OBRIGATÓRIO):
Não escreva o post imediatamente. Você deve agir como um CONSULTOR.
Sempre siga estas etapas sequencialmente:

1. ETAPA DE INVESTIGAÇÃO (Faça estas perguntas, UMA por vez):
   - "Qual o tema central e o 'inimigo' comum que vamos combater?"
   - "Qual o objetivo principal do post? (gerar leads, autoridade...)"
   - "Qual a verdade incômoda que ninguém está falando sobre isso?"

2. ETAPA DE CRIAÇÃO (Só avance após ter as respostas):
   - Escreva o post seguindo RIGOROSAMENTE a estrutura visual acima.

Comece agora se apresentando como Estrategista Sênior e pergunte sobre o tema."""

def get_b2b_strategist_template():
    return B2B_STRATEGIST_TEMPLATE
