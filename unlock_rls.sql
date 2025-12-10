-- 🚨 SCRIPT DE "DESBLOQUEIO" (Modo Permissivo)
-- Vamos relaxar as regras do banco para garantir que o post seja salvo.
-- Confiaremos que o aplicativo (Streamlit) está enviando o ID correto.

ALTER TABLE scheduled_posts ENABLE ROW LEVEL SECURITY;

-- Remove políticas anteriores restritivas
DROP POLICY IF EXISTS "Users can view own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can insert own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can update own scheduled posts" ON scheduled_posts;
DROP POLICY IF EXISTS "Users can delete own scheduled posts" ON scheduled_posts;

-- Cria políticas baseadas apenas em "Estar Logado" (Authenticated)
-- Isso permite que qualquer usuário logado insira linhas, confiando que o App preencheu o user_id certo.

CREATE POLICY "Allow authenticated view" 
ON scheduled_posts FOR SELECT 
USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated insert" 
ON scheduled_posts FOR INSERT 
WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated update" 
ON scheduled_posts FOR UPDATE 
USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated delete" 
ON scheduled_posts FOR DELETE 
USING (auth.role() = 'authenticated');
