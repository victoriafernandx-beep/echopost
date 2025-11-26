# 🤖 EchoPost WhatsApp Bot

Bot do WhatsApp que recebe áudios ou mensagens de texto e gera posts profissionais para LinkedIn usando IA (Gemini).

## 🎯 Funcionalidades

- ✅ Recebe mensagens de texto
- ✅ Recebe e transcreve áudios
- ✅ Gera posts profissionais com IA
- ✅ Responde automaticamente no WhatsApp

## 🚀 Deploy no Railway

### 1. Criar Conta no Railway
1. Acesse: [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"

### 2. Deploy do Repositório
1. Selecione "Deploy from GitHub repo"
2. Conecte sua conta GitHub
3. Selecione o repositório `echopost`
4. Railway vai detectar automaticamente o Python

### 3. Configurar Variáveis de Ambiente
No painel do Railway, vá em **Variables** e adicione:

```
VERIFY_TOKEN=echopost_webhook_2024
WHATSAPP_TOKEN=<seu_token_do_meta>
PHONE_NUMBER_ID=893421050521305
GEMINI_API_KEY=<sua_chave_gemini>
```

### 4. Obter URL do Webhook
Após o deploy, Railway vai gerar uma URL tipo:
```
https://seu-app.up.railway.app
```

Sua URL do webhook será:
```
https://seu-app.up.railway.app/webhook
```

### 5. Configurar no Meta for Developers
1. Volte no painel do WhatsApp
2. Vá em "Configuração" → "Webhook"
3. Cole a URL: `https://seu-app.up.railway.app/webhook`
4. Verify Token: `echopost_webhook_2024`
5. Clique em "Verificar e Salvar"
6. Inscreva-se em "messages"

## 🧪 Testar

1. Envie uma mensagem de texto para o número do bot
2. Ou envie um áudio
3. O bot vai responder com um post gerado pela IA!

## 📝 Estrutura do Código

- `app.py` - Servidor Flask principal
- `requirements.txt` - Dependências Python
- `Procfile` - Configuração para Railway/Heroku
- `.env.example` - Exemplo de variáveis de ambiente

## 🔧 Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Copiar .env.example para .env e preencher
cp .env.example .env

# Rodar servidor
python app.py
```

## 📚 Documentação

- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Gemini API](https://ai.google.dev/docs)
- [Railway Docs](https://docs.railway.app/)
