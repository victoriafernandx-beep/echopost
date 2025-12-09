-- 🛠️ SCRIPT DE CORREÇÃO DE ERRO NO SIGNUP
-- Execute este script no SQL Editor do Supabase para corrigir o erro "Database error saving new user"

-- 1. Remover triggers antigas que podem estar quebradas
-- (Muitos tutoriais pedem para criar essa trigger, e se a função handle_new_user não existir ou tiver erro, o cadastro falha)
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;
DROP FUNCTION IF EXISTS public.handle_new_user CASCADE;

-- 2. Garantir permissões corretas no schema public
-- (As vezes o usuário interno do Supabase perde permissão de escrever em tabelas públicas)
GRANT USAGE ON SCHEMA public TO postgres;
GRANT USAGE ON SCHEMA public TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO service_role;

GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- 3. Recriar a tabela de conexões (caso não exista)
CREATE TABLE IF NOT EXISTS user_connections (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  provider TEXT NOT NULL,
  access_token TEXT NOT NULL,
  refresh_token TEXT,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_user_provider UNIQUE (user_id, provider)
);

-- 4. Habilitar RLS nela
ALTER TABLE user_connections ENABLE ROW LEVEL SECURITY;

-- 5. Recriar políticas básicas (dropando antes para evitar erro de duplicidade)
DROP POLICY IF EXISTS "Users can view own connections" ON user_connections;
CREATE POLICY "Users can view own connections" ON user_connections FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage own connections" ON user_connections;
CREATE POLICY "Users can manage own connections" ON user_connections FOR ALL USING (auth.uid() = user_id);
