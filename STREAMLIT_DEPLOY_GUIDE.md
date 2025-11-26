# 🚀 Deploy no Streamlit Cloud - Guia Rápido

## ✅ Repositório GitHub Pronto!

Seu código já está no GitHub: **https://github.com/victoriafernandx-beep/echopost**

---

## 📋 Próximos Passos no Streamlit Cloud

### 1. Acessar Streamlit Cloud

Vou abrir o navegador em: **https://share.streamlit.io/**

### 2. Fazer Login

- Clique em **"Sign in"**
- Escolha **"Continue with GitHub"**
- Autorize o Streamlit a acessar sua conta GitHub

### 3. Criar Nova App

1. Clique em **"New app"** ou **"Create app"**
2. Selecione:
   - **Repository**: `victoriafernandx-beep/echopost`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Clique em **"Advanced settings"** (IMPORTANTE!)

### 4. Configurar Secrets (CRÍTICO!)

Na seção **"Secrets"**, cole exatamente este conteúdo:

```toml
SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
```

> ⚠️ **IMPORTANTE**: Cole exatamente como está acima, sem a seção `[secrets]`

### 5. Deploy!

1. Clique em **"Deploy!"**
2. Aguarde alguns minutos enquanto o Streamlit:
   - Instala as dependências
   - Inicia a aplicação
   - Gera uma URL pública

### 6. Sua App Estará Online! 🎉

Você receberá uma URL como:
```
https://echopost.streamlit.app
```

ou

```
https://victoriafernandx-beep-echopost-app-xxxxx.streamlit.app
```

---

## 🧪 Testar Após Deploy

1. Acesse a URL fornecida
2. Vá em "Gerador de Posts"
3. Digite um tópico de teste
4. Clique em "Gerar Post"
5. Verifique se o Gemini gera o conteúdo

---

## 🔧 Troubleshooting

### Se aparecer erro de API Key:
- Verifique se os secrets foram colados corretamente
- Reinicie a app no painel do Streamlit Cloud

### Se aparecer erro de dependências:
- Verifique se o `requirements.txt` está no repositório
- Reinicie a app

### Para ver logs de erro:
- No painel do Streamlit Cloud, clique em "Manage app"
- Veja a seção "Logs" para detalhes

---

## 📝 Seus Secrets (para referência)

```toml
SUPABASE_URL = "https://nqiaokjpdszfuehvprep.supabase.co"
SUPABASE_KEY = "sb_publishable_k-bAvB9t_FNS3zeNoEInHA_PdMcAW-n"
GEMINI_API_KEY = "AIzaSyBSXMVqA8KmNuHS7Wh2w1cpbCURQJsofgE"
```

**Guarde essas informações em local seguro!** 🔐
