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
