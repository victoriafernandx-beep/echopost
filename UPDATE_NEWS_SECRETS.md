# Atualizar Secrets do NewsAPI no Streamlit Cloud

## Passo a Passo

1. Acesse o [Streamlit Cloud](https://share.streamlit.io/)
2. Faça login com sua conta
3. Encontre o app **linkedin10x** na lista
4. Clique nos **três pontinhos (⋮)** ao lado do app
5. Selecione **Settings**
6. Na aba **Secrets**, clique em **Edit**
7. Adicione a seguinte linha ao final do arquivo:

```toml
NEWS_API_KEY = "960005a1774143418a92cd997887ee6e"
```

8. Clique em **Save**
9. O app irá reiniciar automaticamente

## Verificação

Após o reinício, acesse o app e vá em **📡 News Radar** para testar a busca de notícias.
