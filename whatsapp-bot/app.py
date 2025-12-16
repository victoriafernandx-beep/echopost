from flask import Flask, request, jsonify
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
from rate_limiter import RateLimiter
from supabase import create_client, Client

from pathlib import Path
# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Configurações
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "echopost_webhook_2024")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configurar OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Configurar Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase conectado!")
    except Exception as e:
        print(f"❌ Erro ao conectar Supabase: {e}")

# Rate limiter (5 messages per minute)
rate_limiter = RateLimiter(max_messages=5, time_window=60)

def validate_message(text):
    """Simple checks for malicious content"""
    if len(text) > 1000:
        raise ValueError("Mensagem muito longa (limite 1000 caracteres)")
        
    suspicious = ['system:', 'ignore previous', 'jailbreak']
    if any(s in text.lower() for s in suspicious):
        raise ValueError("Conteúdo inválido detectado")
    return text

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

            try:
                text = validate_message(text)
            except ValueError as e:
                send_whatsapp_message(from_number, f"⛔ {str(e)}")
                return
            
            # Check for commands
            if text.startswith('/'):
                response = handle_command(text)
                send_whatsapp_message(from_number, response)
                return
            
            response = generate_post_from_text(text, from_number)
            send_whatsapp_message(from_number, response)
        
        elif message_type == 'audio':
            audio_id = message['audio']['id']
            print(f"🎤 Áudio ID: {audio_id}")
            
            # Baixar e transcrever áudio
            audio_url = get_media_url(audio_id)
            transcription = transcribe_audio(audio_url)
            print(f"📝 Transcrição: {transcription}")
            
            # Gerar post
            response = generate_post_from_text(transcription, from_number)
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

def generate_post_from_text(text, from_number):
    """Gerar post profissional usando OpenAI"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Você é um estrategista de conteúdo B2B sênior.
Seu objetivo é transformar insights em posts de altíssimo valor e clareza.

PRINCÍPIOS DE ESTILO:
1. Sênior e Direto: Vá direto ao ponto. Sem enrolação.
2. Ritmo Visual: Escreva frases curtas. Pule linhas para dar respiro. Evite "muros de texto".
3. Variedade: Não use sempre a mesma fórmula. Adapte a estrutura (lista, contraste, pergunta) ao conteúdo.
4. Emojis inteligentes: Use como marcadores de tópico ou destaque, não como enfeite.
5. Sem clichês: Evite linguagem de "guru" ou frases motivacionais vazias.

Seja autêntico e provocativo."""},
                {"role": "user", "content": f"""Transforme o seguinte insight/áudio em um post profissional seguindo os princípios acima:

"{text}"

Retorne APENAS o texto do post."""}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        post = response.choices[0].message.content.strip()
        
        # Salvar no Supabase
        save_post_to_db(post, from_number)
        
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

def save_post_to_db(content, from_number):
    """Salvar post no Supabase"""
    if not supabase:
        print("⚠️ Supabase não configurado, pulando salvamento.")
        return

    try:
        # Tentar encontrar usuário pelo telefone (lookup na tabela user_settings)
        user_id = os.getenv("WHATSAPP_BOT_USER_ID", "whatsapp-bot") # Fallback
        
        try:
            # Busca quem salvou esse número nas configurações
            response = supabase.table("user_settings")\
                .select("user_id")\
                .eq("setting_key", "whatsapp_number")\
                .eq("setting_value", from_number)\
                .execute()
            
            if response.data and len(response.data) > 0:
                user_id = response.data[0]['user_id']
                print(f"✅ Usuário identificado: {user_id}")
            else:
                print(f"⚠️ Usuário não identificado para {from_number}. Usando genérico.")
                
        except Exception as lookup_error:
            print(f"⚠️ Erro no lookup de usuário: {lookup_error}")

        data = {
            "content": content,
            "user_id": user_id,
            "topic": "WhatsApp Generated",
            "source": "whatsapp",
            "tags": ["whatsapp", f"phone_{from_number}"],
            "created_at": "now()"
        }

        response = supabase.table("posts").insert(data).execute()
        print(f"💾 Post salvo no banco: ID {response.data[0]['id']}")
        return response.data[0]['id']

    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

def transcribe_audio(audio_url):
    """Transcrever áudio usando OpenAI Whisper"""
    import tempfile
    import os
    
    temp_path = None
    try:
        # Baixar áudio
        audio_data = download_media(audio_url)
        
        # Salvar temporariamente de forma segura
        # delete=False is mandatory for Windows compatibility when re-opening the file
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file.flush()
            temp_path = temp_file.name
            
        # Transcrever com Whisper
        with open(temp_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
        
        return transcription.text.strip()
    
    except Exception as e:
        print(f"❌ Erro ao transcrever áudio: {e}")
        return "Erro ao transcrever áudio"
    finally:
        # Secure cleanup
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"⚠️ Warning: Could not delete temp file {temp_path}: {e}")

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
        
        if not response.ok:
            print(f"❌ Erro Detalhado Meta: {response.text}")
            
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
