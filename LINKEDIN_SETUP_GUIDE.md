# 🔗 Guia de Configuração do LinkedIn OAuth

## ⚠️ IMPORTANTE: Siga estes passos ANTES de usar

### PASSO 1: Criar App no LinkedIn Developer Portal

1. **Acesse**: https://www.linkedin.com/developers/apps
2. **Faça login** com sua conta LinkedIn
3. **Clique em**: "Create app"
4. **Preencha os dados**:
   - **App name**: `EchoPost`
   - **LinkedIn Page**: Selecione sua página/empresa (ou crie uma)
   - **Privacy policy URL**: `https://seu-site.com/privacy` (pode ser genérica)
   - **App logo**: Upload de uma logo (256x256px)
   - **Legal agreement**: Aceite os termos
5. **Clique em**: "Create app"

---

### PASSO 2: Configurar Produtos (Products)

1. No app criado, vá na aba **"Products"**
2. **Solicite acesso** para:
   - ✅ **Share on LinkedIn** (para postar) - ESSENCIAL
   - ✅ **Sign In with LinkedIn** (para login) - ESSENCIAL
   - ⚠️ **Marketing Developer Platform** (para analytics) - OPCIONAL (requer aprovação)

3. **Aguarde aprovação**:
   - "Share on LinkedIn" e "Sign In" são aprovados instantaneamente
   - "Marketing Developer Platform" pode levar dias/semanas

---

### PASSO 3: Configurar OAuth 2.0

1. Vá na aba **"Auth"**
2. Em **"Redirect URLs"**, clique em "Add redirect URL"
3. **Adicione**:
   ```
   https://echopost.streamlit.app
   ```
   OU se estiver testando localmente:
   ```
   http://localhost:8501
   ```

4. **Copie as credenciais**:
   - **Client ID**: `abc123...`
   - **Client Secret**: `xyz789...` (clique em "Show" para ver)

---

### PASSO 4: Adicionar Credenciais no Streamlit

#### No Streamlit Cloud:

1. Vá em: https://share.streamlit.io
2. Abra seu app **EchoPost**
3. Clique em **"Settings"** (⚙️)
4. Vá em **"Secrets"**
5. **Cole este código** (substitua pelos seus valores):

```toml
LINKEDIN_CLIENT_ID = "seu_client_id_aqui"
LINKEDIN_CLIENT_SECRET = "seu_client_secret_aqui"
LINKEDIN_REDIRECT_URI = "https://echopost.streamlit.app"
```

6. **Salve**

#### Localmente (.streamlit/secrets.toml):

```toml
LINKEDIN_CLIENT_ID = "seu_client_id_aqui"
LINKEDIN_CLIENT_SECRET = "seu_client_secret_aqui"
LINKEDIN_REDIRECT_URI = "http://localhost:8501"
```

---

### PASSO 5: Testar Conexão

1. **Recarregue o app**
2. Vá em **"Configurações"**
3. Na seção **"Integração LinkedIn"**:
   - Se aparecer "⚠️ Credenciais não configuradas" → Volte ao Passo 4
   - Se aparecer link "Clique aqui para conectar" → **SUCESSO!**

4. **Clique no link** para autorizar
5. **Autorize** o app no LinkedIn
6. Você será redirecionado de volta

---

### PASSO 6: Publicar Post de Teste

1. Vá em **"Gerador de Posts"**
2. Gere ou escreva um post
3. Clique em **"🔗 Publicar no LinkedIn"**
4. **Verifique** seu perfil LinkedIn!

---

## 🔒 Segurança

**NUNCA compartilhe**:
- ❌ Client Secret
- ❌ Access Tokens
- ❌ Arquivo secrets.toml

**Sempre use**:
- ✅ Secrets do Streamlit
- ✅ HTTPS em produção
- ✅ Redirect URI exata

---

## 🐛 Troubleshooting

### "Credenciais não configuradas"
→ Adicione as credenciais no secrets.toml

### "Erro ao conectar: invalid_client"
→ Client ID ou Secret incorretos

### "Erro ao conectar: redirect_uri_mismatch"
→ Redirect URI no LinkedIn deve ser EXATAMENTE igual ao configurado

### "Erro ao publicar: insufficient_permissions"
→ Solicite "Share on LinkedIn" no Products

### "Erro ao publicar: unauthorized"
→ Reconecte sua conta (desconecte e conecte novamente)

---

## 📊 Métricas Reais

Para buscar métricas reais (followers, impressions, etc):

1. **Solicite** "Marketing Developer Platform" no Products
2. **Aguarde aprovação** (pode levar dias)
3. **Preencha formulário** detalhado do LinkedIn
4. Quando aprovado, as métricas serão reais!

Até lá, métricas são simuladas (mock).

---

## ✅ Checklist Final

- [ ] App criado no LinkedIn Developers
- [ ] "Share on LinkedIn" aprovado
- [ ] "Sign In with LinkedIn" aprovado
- [ ] Redirect URI configurada
- [ ] Client ID copiado
- [ ] Client Secret copiado
- [ ] Credenciais adicionadas no Streamlit Secrets
- [ ] App recarregado
- [ ] Conexão testada
- [ ] Post de teste publicado

---

## 🚀 Pronto!

Quando tudo estiver configurado, você terá:
- ✅ Login real com LinkedIn
- ✅ Publicação real de posts
- ✅ Integração completa
- ⏳ Métricas reais (quando aprovado)

**Qualquer dúvida, me avise!** 😊
