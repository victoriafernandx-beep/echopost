# ⚠️ Gemini API Key Vazada - Solução Rápida

## O que aconteceu?
A API Key do Gemini foi detectada como exposta publicamente (provavelmente no código do GitHub) e foi automaticamente desativada pelo Google por segurança.

## Solução (5 minutos)

### 1. Gerar Nova API Key
1. Acesse: **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Faça login com sua conta Google
3. Clique em **"Create API Key"** ou **"Get API Key"**
4. **Copie a nova chave** (começa com `AIza...`)

### 2. Atualizar no Streamlit Cloud
1. Acesse **[Streamlit Cloud](https://share.streamlit.io/)**
2. Encontre o app **linkedin10x**
3. Clique nos **⋮** → **Settings**
4. Na aba **Secrets**, clique em **Edit**
5. **Substitua** a linha `GEMINI_API_KEY` pela nova chave:
   ```toml
   GEMINI_API_KEY = "SUA_NOVA_CHAVE_AQUI"
   ```
6. Clique em **Save**

### 3. Verificar
Após o reinício automático do app, teste gerando um post para confirmar que está funcionando.

## ⚠️ Importante
**NÃO** adicione a chave diretamente no código. Sempre use apenas nos **Secrets** do Streamlit Cloud.
