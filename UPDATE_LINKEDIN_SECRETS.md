# 🔄 Atualizar Secrets do LinkedIn no Streamlit Cloud

## 📋 Passo a Passo

1.  Acesse **[Streamlit Cloud](https://share.streamlit.io/)**.
2.  Encontre o app **linkedin10x** (ou echopost).
3.  Clique em **Settings** (⚙️) -> **Secrets**.
4.  **Adicione** as novas chaves ao final do arquivo (ou substitua se já existirem):

```toml
LINKEDIN_CLIENT_ID = "SEU_CLIENT_ID"
LINKEDIN_CLIENT_SECRET = "SEU_CLIENT_SECRET"
LINKEDIN_REDIRECT_URI = "https://linkedin10x.streamlit.app"
```

> ⚠️ **Atenção:** A `LINKEDIN_REDIRECT_URI` em produção deve ser `https://linkedin10x.streamlit.app`. Localmente usamos `http://localhost:8503`.

5.  Clique em **Save**.

## ✅ Teste

Após salvar, a aplicação irá reiniciar.
1.  Acesse o app.
2.  Vá em **Configurações**.
3.  Clique em **Conectar LinkedIn**.
