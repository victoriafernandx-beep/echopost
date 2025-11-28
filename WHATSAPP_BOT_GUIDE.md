# 🤖 Guia: WhatsApp Bot com IA - WhatsApp Business API

## 🎯 Objetivo
Criar um bot do WhatsApp que recebe áudios ou mensagens de texto e gera posts profissionais usando IA.

**Fluxo**:
```
Usuário → WhatsApp → Webhook → Servidor → Gemini AI → Resposta no WhatsApp
```

---

## 📋 Pré-requisitos

1. **Conta no Meta for Developers** (Facebook)
2. **Número de telefone** dedicado para o bot (não pode ser seu número pessoal)
3. **Conta no Facebook Business Manager**
4. **Servidor com HTTPS** (pode usar Streamlit Cloud, Heroku, Railway, etc.)

---

## 🚀 Passo 1: Configurar Meta for Developers

### 1.1 Criar Conta
1. Acesse: **[Meta for Developers](https://developers.facebook.com/)**
2. Faça login com sua conta Facebook
3. Clique em **"My Apps"** → **"Create App"**

### 1.2 Criar Aplicativo
1. Escolha tipo: **"Business"**
2. Nome do app: `EchoPost WhatsApp Bot`
3. Email de contato: seu email
4. Selecione **Business Manager** (ou crie um se não tiver)
5. Clique em **"Create App"**

### 1.3 Adicionar WhatsApp
1. No painel do app, procure **"WhatsApp"**
2. Clique em **"Set Up"**
3. Siga o wizard de configuração

---

## 📱 Passo 2: Configurar Número de Telefone

### 2.1 Número de Teste (Gratuito)
O Meta fornece um número de teste para desenvolvimento:
1. No painel WhatsApp, vá em **"API Setup"**
2. Você verá um número de teste (ex: +1 555...)
3. Adicione seu número pessoal como **"Recipient"** para testar

### 2.2 Número Real (Produção)
Para usar em produção, você precisa:
1. Comprar um número dedicado (Twilio, Vonage, etc.)
2. Ou usar um número de celular que **não** esteja em uso
3. Verificar o número no painel do Meta

**⚠️ Importante**: O número não pode estar cadastrado no WhatsApp pessoal.

---

## 🔧 Passo 3: Configurar Webhook

### 3.1 O que é Webhook?
É uma URL que o WhatsApp chama quando alguém envia mensagem para o bot.

### 3.2 Criar Servidor de Webhook

**Opção A: Usar Streamlit Cloud** (mais simples)
- Criar endpoint separado no app
- Limitação: Streamlit não é ideal para webhooks

**Opção B: Usar Railway/Render/Heroku** (recomendado)
- Criar servidor Flask/FastAPI dedicado
- Gratuito e confiável

**Opção C: Usar Twilio/Vonage** (mais fácil)
- Eles fornecem infraestrutura pronta
- Pode ter custo

### 3.3 Código do Webhook (Exemplo Flask)

```python
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "SEU_TOKEN_SECRETO"
WHATSAPP_TOKEN = "SEU_TOKEN_DO_META"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificação do webhook
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if token == VERIFY_TOKEN:
            return challenge
        return 'Invalid token', 403
    
    elif request.method == 'POST':
        # Receber mensagem
        data = request.get_json()
        
        # Processar mensagem
        process_message(data)
        
        return jsonify({'status': 'ok'}), 200

def process_message(data):
    # Extrair dados da mensagem
    message = data['entry'][0]['changes'][0]['value']['messages'][0]
    from_number = message['from']
    
    if message['type'] == 'text':
        text = message['text']['body']
        # Gerar post com IA
        response = generate_post_with_ai(text)
        send_whatsapp_message(from_number, response)
    
    elif message['type'] == 'audio':
        audio_id = message['audio']['id']
        # Baixar e transcrever áudio
        transcription = transcribe_audio(audio_id)
        response = generate_post_with_ai(transcription)
        send_whatsapp_message(from_number, response)

def generate_post_with_ai(text):
    # Integrar com Gemini (código que já temos!)
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""Transforme este texto em um post profissional para LinkedIn:
    
    {text}
    
    O post deve ser envolvente, profissional e ter entre 150-250 palavras."""
    
    response = model.generate_content(prompt)
    return response.text

def send_whatsapp_message(to_number, message):
    url = f"https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(port=5000)
```

### 3.4 Configurar Webhook no Meta
1. No painel WhatsApp, vá em **"Configuration"**
2. Em **"Webhook"**, clique em **"Edit"**
3. Cole a URL do seu servidor: `https://seu-servidor.com/webhook`
4. Callback URL: `https://seu-servidor.com/webhook`
5. Verify Token: `SEU_TOKEN_SECRETO`
6. Clique em **"Verify and Save"**

### 3.5 Subscrever a Eventos
Marque as opções:
- ✅ `messages`
- ✅ `message_status`

---

## 🎤 Passo 4: Transcrição de Áudio

### Opção 1: Google Speech-to-Text
```python
from google.cloud import speech

def transcribe_audio(audio_url):
    client = speech.SpeechClient()
    
    # Baixar áudio
    audio_content = download_audio(audio_url)
    
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        language_code="pt-BR"
    )
    
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript
```

### Opção 2: Gemini (Suporta Áudio!)
```python
def transcribe_with_gemini(audio_url):
    import google.generativeai as genai
    
    # Baixar áudio
    audio_file = download_audio(audio_url)
    
    # Upload para Gemini
    uploaded_file = genai.upload_file(audio_file)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([
        "Transcreva este áudio em português:",
        uploaded_file
    ])
    
    return response.text
```

---

## 💰 Custos

### Gratuito:
- ✅ Primeiras **1.000 conversas/mês** (Meta)
- ✅ Gemini API (tem cota gratuita generosa)

### Pagos (após limites):
- WhatsApp: ~$0.005 - $0.01 por mensagem
- Google Speech-to-Text: ~$0.006/minuto
- Servidor: Grátis (Railway/Render) ou ~$5-10/mês

---

## 🧪 Passo 5: Testar

1. Adicione seu número como recipiente de teste
2. Envie mensagem para o número do bot
3. Verifique se o webhook recebe a mensagem
4. Teste geração de post
5. Verifique resposta no WhatsApp

---

## 📚 Recursos Úteis

- [Documentação WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Flask Quickstart](https://flask.palletsprojects.com/)

---

## 🚨 Próximos Passos

1. **Criar conta no Meta for Developers** (hoje)
2. **Configurar app WhatsApp** (1 dia)
3. **Criar servidor webhook** (1-2 dias)
4. **Integrar com Gemini** (1 dia)
5. **Testar e validar** (1 dia)

**Tempo total estimado**: 1 semana

---

**Quer que eu te ajude a implementar o servidor webhook?** Posso criar o código completo para você! 🚀
