# 🔧 Atualização do Banco de Dados - Tags e Busca

## ⚠️ IMPORTANTE: Execute este SQL ANTES de usar as novas features

### Passo 1: Acesse o Supabase
1. Vá para [https://supabase.com](https://supabase.com)
2. Faça login
3. Selecione seu projeto EchoPost

### Passo 2: Abra o SQL Editor
1. No menu lateral, clique em "SQL Editor"
2. Clique em "New query"

### Passo 3: Cole e Execute o SQL

Copie e cole o código abaixo:

```sql
-- Schema updates for Tags and Search
-- Run this in Supabase SQL Editor

-- Add tags column (array of text)
ALTER TABLE posts ADD COLUMN IF NOT EXISTS tags TEXT[];

-- Add favorite flag
ALTER TABLE posts ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE;

-- Add word count
ALTER TABLE posts ADD COLUMN IF NOT EXISTS word_count INTEGER;

-- Add hashtags column
ALTER TABLE posts ADD COLUMN IF NOT EXISTS hashtags TEXT[];

-- Create index for better search performance
CREATE INDEX IF NOT EXISTS idx_posts_tags ON posts USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_posts_content_search ON posts USING GIN(to_tsvector('portuguese', content));
CREATE INDEX IF NOT EXISTS idx_posts_topic_search ON posts USING GIN(to_tsvector('portuguese', topic));
```

### Passo 4: Execute
1. Clique no botão "Run" (ou pressione Ctrl+Enter)
2. Aguarde a mensagem de sucesso
3. Pronto! ✅

### O que isso faz?
- ✅ Adiciona coluna `tags` para organizar posts
- ✅ Adiciona coluna `is_favorite` para favoritar posts
- ✅ Adiciona coluna `word_count` para contagem de palavras
- ✅ Cria índices para busca rápida

### Depois de executar:
Me avise que executou e eu continuo implementando a UI! 🚀
