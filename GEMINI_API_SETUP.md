# 🔑 Configuração da API Key do Gemini

## Problema Identificado

A API Key atual do Gemini está **inválida** ou **expirada**. Você precisa gerar uma nova chave válida.

## ✅ Passo a Passo para Obter uma Nova API Key

### 1. Acesse o Google AI Studio

Abra seu navegador e vá para:
**https://aistudio.google.com/app/apikey**

### 2. Faça Login

- Use sua conta Google
- Aceite os termos de serviço se solicitado

### 3. Crie uma Nova API Key

1. Clique em **"Create API Key"** ou **"Criar chave de API"**
2. Selecione um projeto do Google Cloud (ou crie um novo)
3. Copie a chave gerada (ela começa com `AIza...`)

> [!IMPORTANT]
> Guarde essa chave em um lugar seguro! Você não poderá vê-la novamente depois de fechar a janela.

### 4. Configure no EchoPost

Após obter a nova chave, você tem duas opções:

#### Opção A: Usando o script de atualização (Recomendado)

1. Abra o arquivo `update_secrets.py`
2. Substitua a chave antiga pela nova:
   ```python
   GEMINI_API_KEY = "SUA_NOVA_CHAVE_AQUI"
   ```
3. Execute o script:
   ```bash
   python update_secrets.py
   ```

#### Opção B: Editar manualmente

1. Abra o arquivo `.streamlit/secrets.toml`
2. Atualize a linha:
   ```toml
   GEMINI_API_KEY = "SUA_NOVA_CHAVE_AQUI"
   ```
3. Salve o arquivo

### 5. Verifique a Configuração

Execute o script de verificação:
```bash
python verify_gemini.py
```

Se tudo estiver correto, você verá:
```
✅ Success! Response received:
---
Hello, EchoPost!
---
```

## 🔍 Modelos Disponíveis

O EchoPost está configurado para usar o modelo **`gemini-flash-latest`**, que é:
- ✅ Gratuito (com limites)
- ✅ Rápido
- ✅ Estável e amplamente disponível
- ✅ Ótimo para geração de conteúdo

## 📊 Limites da API Gratuita

- **15 requisições por minuto**
- **1 milhão de tokens por minuto**
- **1.500 requisições por dia**

Para uso do EchoPost, esses limites são mais do que suficientes!

## ❓ Problemas Comuns

### Erro: "API key not valid"
- ✅ Gere uma nova chave no Google AI Studio
- ✅ Verifique se copiou a chave completa (sem espaços extras)
- ✅ Certifique-se de que a API Generative Language está habilitada no seu projeto

### Erro: "404 models/gemini-pro not found"
- ✅ Use `gemini-flash-latest` ou `gemini-1.5-flash` (já configurado no código)
- ✅ O modelo `gemini-pro` foi descontinuado

### Erro: "Quota exceeded"
- ⏰ Aguarde alguns minutos (limite de requisições por minuto)
- 📅 Se for limite diário, aguarde até o próximo dia

## 🚀 Próximos Passos

Após configurar a API Key:

1. ✅ Teste a geração de posts no EchoPost
2. ✅ Experimente diferentes tons de voz (Profissional, Casual, Inspirador)
3. ✅ Use o News Radar para gerar posts sobre notícias
4. ✅ Continue com o deploy para produção (Supabase + Streamlit Cloud)
