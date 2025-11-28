from flask import Flask, request, jsonify
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
from rate_limiter import RateLimiter

load_dotenv()

app = Flask(__name__)

# Configurações
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "echopost_webhook_2024")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Rate limiter (5 messages per minute)
rate_limiter = RateLimiter(max_messages=5, time_window=60)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Endpoint principal do webhook"""
    
    if request.method == 'GET':
        # Verificação do webhook (Meta vai chamar isso para validar)
        return verify_webhook(request)
    
    elif request.method == 'POST':
        # Receber mensagem
        data = request.get_json()
        print(f"📩 Mensagem recebida: {data}")
        
        try:
            process_whatsapp_message(data)
            return jsonify({'status': 'ok'}), 200
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

def verify_webhook(request):
    """Verificar webhook do WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso!")
        return challenge, 200
    else:
        print("❌ Falha na verificação do webhook")
        return 'Forbidden', 403

def process_whatsapp_message(data):
    """Processar mensagem recebida do WhatsApp"""
    
    try:
        # Extrair dados da mensagem
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        # Verificar se há mensagens
        if 'messages' not in value:
            print("⚠️ Sem mensagens para processar")
            return
        
        message = value['messages'][0]
        from_number = message['from']
        message_type = message['type']
        
        print(f"📱 Mensagem de: {from_number}")
        print(f"📝 Tipo: {message_type}")
        
        # Check rate limit
        allowed, remaining = rate_limiter.is_allowed(from_number)
        if not allowed:
            wait_time = rate_limiter.get_wait_time(from_number)
            send_whatsapp_message(
                from_number,
                f"⏸️ Você atingiu o limite de mensagens.\\n\\nAguarde {wait_time} segundos antes de enviar outra mensagem."
            )
            return
        
        # Processar baseado no tipo
        if message_type == 'text':
            text = message['text']['body']
            print(f"💬 Texto: {text}")
            
            # Check for commands
            if text.startswith('/'):
                response = handle_command(text)
                send_whatsapp_message(from_number, response)
                return
            
            response = generate_post_from_text(text)
            send_whatsapp_message(from_number, response)
        
        elif message_type == 'audio':
            audio_id = message['audio']['id']
            print(f"🎤 Áudio ID: {audio_id}")
            
            # Baixar e transcrever áudio
            audio_url = get_media_url(audio_id)
            transcription = transcribe_audio(audio_url)
            print(f"📝 Transcrição: {transcription}")
            
            # Gerar post
            response = generate_post_from_text(transcription)
            send_whatsapp_message(from_number, response)
        
        else:
            # Tipo não suportado
            send_whatsapp_message(
                from_number, 
                "⚠️ Desculpe, só consigo processar mensagens de texto ou áudio no momento."
            )
    
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        raise

def handle_command(command_text):
    """Handle bot commands"""
    command = command_text.lower().strip()
    
    if command == '/help' or command == '/ajuda':
        return """🤖 *EchoPost Bot - Comandos Disponíveis*

📝 *Como usar:*
Envie uma mensagem ou áudio descrevendo o que você quer postar, e eu crio um post profissional para LinkedIn!

⚡ *Comandos:*
/help - Mostra esta mensagem
/templates - Ver templates de posts
/status - Status do bot

💡 *Dicas:*
• Seja específico sobre o tema
• Mencione o tom desejado (profissional, casual, inspiracional)
• Para áudios, fale claramente

🎯 *Exemplos:*
"Crie um post sobre IA no marketing"
"Post inspiracional sobre liderança"
"Dicas de produtividade para desenvolvedores"

Criado por EchoPost 🚀"""
    
    elif command == '/templates':
        return """📚 *Templates de Posts Disponíveis*

1️⃣ *Dica Profissional*
"Dica sobre [tema]: [sua dica]"

2️⃣ *História Pessoal*
"Conte uma história sobre [experiência]"

3️⃣ *Opinião sobre Tendência*
"Sua opinião sobre [tendência/notícia]"

4️⃣ *Lista de Aprendizados*
"5 lições que aprendi sobre [tema]"

5️⃣ *Pergunta Engajadora*
"Faça uma pergunta sobre [tema]"

💡 *Como usar:*
Escolha um template e me envie uma mensagem seguindo o formato!

Exemplo: "Dica sobre produtividade: use a técnica Pomodoro"
"""
    
    elif command == '/status':
        return """✅ *EchoPost Bot - Status*

🟢 Online e funcionando
🤖 IA: OpenAI GPT-4o-mini
🎤 Transcrição: Whisper
⚡ Limite: 5 mensagens/minuto

📊 *Recursos:*
✓ Geração de posts
✓ Transcrição de áudio
✓ Múltiplos idiomas
✓ Formatação profissional

🔗 Powered by EchoPost"""
    
    else:
        return f"""❓ Comando não reconhecido: {command_text}

Digite /help para ver os comandos disponíveis."""

def generate_post_from_text(text):
    """Gerar post profissional usando OpenAI"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em criar posts profissionais para LinkedIn."},
                {"role": "user", "content": f"""Transforme o seguinte texto/ideia em um post envolvente e profissional:

"{text}"

O post deve:
- Começar com um gancho forte
- Ser claro e objetivo
- Ter tom profissional mas acessível
- Usar emojis estrategicamente (máximo 3-4)
- Ter entre 150-250 palavras
- Terminar com uma pergunta ou call-to-action

Retorne APENAS o texto do post, sem explicações adicionais."""}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        post = response.choices[0].message.content.strip()
        
        # Adicionar cabeçalho
        final_message = f"""✨ *Post gerado com IA!*

{post}

---
📝 Criado pelo EchoPost Bot
💡 Edite como preferir antes de publicar!"""
        
        return final_message
    
    except Exception as e:
        print(f"❌ Erro ao gerar post: {e}")
        return f"❌ Desculpe, houve um erro ao gerar o post: {str(e)}"

def transcribe_audio(audio_url):
    """Transcrever áudio usando OpenAI Whisper"""
    
    try:
        # Baixar áudio
        audio_data = download_media(audio_url)
        
        # Salvar temporariamente
        temp_file = "/tmp/audio.ogg"
        with open(temp_file, 'wb') as f:
            f.write(audio_data)
        
        # Transcrever com Whisper
        with open(temp_file, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
        
        # Limpar arquivo temporário
        os.remove(temp_file)
        
        return transcription.text.strip()
    
    except Exception as e:
        print(f"❌ Erro ao transcrever áudio: {e}")
        return "Erro ao transcrever áudio"

def get_media_url(media_id):
    """Obter URL do arquivo de mídia"""
    
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data['url']

def download_media(media_url):
    """Baixar arquivo de mídia"""
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}"
    }
    
    response = requests.get(media_url, headers=headers)
    response.raise_for_status()
    
    return response.content

def send_whatsapp_message(to_number, message):
    """Enviar mensagem via WhatsApp"""
    
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ Mensagem enviada para {to_number}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return False

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'service': 'EchoPost WhatsApp Bot'
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
