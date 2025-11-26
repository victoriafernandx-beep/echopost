# 🔄 Atualizar Secrets no Streamlit Cloud

## Situação Atual

✅ **App já existe**: https://linkedin10x.streamlit.app/  
✅ **Nova API Key do Gemini configurada localmente**  
⚠️ **Precisa atualizar secrets no Streamlit Cloud**

---

## 📝 Passo a Passo

### 1. Acessar o Dashboard do Streamlit Cloud

Vá para: **https://share.streamlit.io/**

### 2. Encontrar Sua App

Procure pela app **"linkedin10x"** ou **"echopost"** na lista de apps

### 3. Acessar Configurações

Clique nos **três pontinhos (⋮)** ao lado da app e selecione **"Settings"** ou **"⚙️ Settings"**

### 4. Ir para Secrets

No menu lateral, clique em **"Secrets"**

### 5. Atualizar os Secrets

**Substitua todo o conteúdo** da caixa de secrets por este:

```toml
SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
```

### 6. Salvar

Clique em **"Save"** ou **"Salvar"**

### 7. Reiniciar a App (Automático)

O Streamlit Cloud vai **reiniciar automaticamente** a aplicação após salvar os secrets.

Aguarde 1-2 minutos para a app reiniciar.

---

## ✅ Testar

Depois que a app reiniciar:

1. Acesse: **https://linkedin10x.streamlit.app/**
2. Vá em **"Gerador de Posts"**
3. Digite um tópico de teste
4. Clique em **"Gerar Post"**
5. Verifique se o Gemini gera o conteúdo sem erros

---

## 🎯 Resultado Esperado

✅ App carrega sem erros  
✅ Gemini gera posts corretamente  
✅ Sem mensagem de "API key not valid"  

---

## 🔐 Seus Secrets (para referência)

```toml
SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
```
