from flask import Flask, request, jsonify
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "echopost_webhook_2024")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

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
        
        # Processar baseado no tipo
        if message_type == 'text':
            text = message['text']['body']
            print(f"💬 Texto: {text}")
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

def generate_post_from_text(text):
    """Gerar post profissional usando Gemini"""
    
    try:
        # Tentar usar gemini-pro que é mais estável
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Você é um especialista em criar posts profissionais para LinkedIn.

Transforme o seguinte texto/ideia em um post envolvente e profissional:

"{text}"

O post deve:
- Começar com um gancho forte
- Ser claro e objetivo
- Ter tom profissional mas acessível
- Usar emojis estrategicamente (máximo 3-4)
- Ter entre 150-250 palavras
- Terminar com uma pergunta ou call-to-action

Retorne APENAS o texto do post, sem explicações adicionais."""

        response = model.generate_content(prompt)
        post = response.text.strip()
        
        # Adicionar cabeçalho
        final_message = f"""✨ *Post gerado com IA!*

{post}

---
📝 Criado pelo EchoPost Bot
💡 Edite como preferir antes de publicar!"""
        
        return final_message
    
    except Exception as e:
        print(f"❌ Erro ao gerar post: {e}")
        try:
            print("📋 Modelos disponíveis:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
        except Exception as list_error:
            print(f"Erro ao listar modelos: {list_error}")
            
        return f"❌ Desculpe, houve um erro ao gerar o post: {str(e)}"

def transcribe_audio(audio_url):
    """Transcrever áudio usando Gemini"""
    
    try:
        # Baixar áudio
        audio_data = download_media(audio_url)
        
        # Salvar temporariamente
        temp_file = "/tmp/audio.ogg"
        with open(temp_file, 'wb') as f:
            f.write(audio_data)
        
        # Upload para Gemini
        uploaded_file = genai.upload_file(temp_file)
        
        # Transcrever
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            "Transcreva este áudio em português. Retorne APENAS a transcrição, sem comentários adicionais.",
            uploaded_file
        ])
        
        transcription = response.text.strip()
        
        # Limpar arquivo temporário
        os.remove(temp_file)
        
        return transcription
    
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
