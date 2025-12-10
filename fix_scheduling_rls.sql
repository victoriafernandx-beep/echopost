-- 🛠️ SCRIPT DE CORREÇÃO DE PERMISSÃO (Agendamento)
-- Execute este script no SQL Editor do Supabase para corrigir o erro "new row violates row-level security policy"

-- 1. Habilitar RLS (caso não esteja)
ALTER TABLE scheduled_posts ENABLE ROW LEVEL SECURITY;

-- 2. Limpar TODAS as políticas antigas (para evitar conflitos)
DROP POLICY IF EXISTS "Users can view own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can insert own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can update own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can delete own scheduled posts" ON scheduled_posts;

-- 3. Criar políticas limpas e corretas usando auth.uid()
-- Nota: Usamos auth.uid()::text porque a coluna user_id é texto

CREATE POLICY "Users can view own scheduled posts" 
ON scheduled_posts FOR SELECT 
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own scheduled posts" 
ON scheduled_posts FOR INSERT 
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own scheduled posts" 
ON scheduled_posts FOR UPDATE 
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete own scheduled posts" 
ON scheduled_posts FOR DELETE 
USING (auth.uid()::text = user_id);

-- 4. Bônus: Garantir permissões na tabela de conexões (caso também dê erro)
ALTER TABLE user_connections ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own connections" ON user_connections;
CREATE POLICY "Users can view own connections" ON user_connections FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own connections" ON user_connections;
CREATE POLICY "Users can insert own connections" ON user_connections FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own connections" ON user_connections;
CREATE POLICY "Users can update own connections" ON user_connections FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own connections" ON user_connections;
CREATE POLICY "Users can delete own connections" ON user_connections FOR DELETE USING (auth.uid() = user_id);
