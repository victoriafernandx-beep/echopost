-- Schema for user connections (LinkedIn tokens)
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS user_connections (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  provider TEXT NOT NULL, -- 'linkedin'
  access_token TEXT NOT NULL,
  refresh_token TEXT,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Ensure one connection per provider per user
  CONSTRAINT unique_user_provider UNIQUE (user_id, provider)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_user_connections_user_provider 
ON user_connections(user_id, provider);

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_connections_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_user_connections_updated_at ON user_connections;
CREATE TRIGGER update_user_connections_updated_at 
BEFORE UPDATE ON user_connections
FOR EACH ROW 
EXECUTE FUNCTION update_connections_updated_at_column();

-- Enable RLS
ALTER TABLE user_connections ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own connections" 
ON user_connections FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own connections" 
ON user_connections FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own connections" 
ON user_connections FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own connections" 
ON user_connections FOR DELETE 
USING (auth.uid() = user_id);

-- Update Policies for existing tables to ensure they work with auth.uid()
-- (These might already exist, but good to ensure consistency)

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own posts" ON posts;
CREATE POLICY "Users can view own posts" 
ON posts FOR SELECT 
USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can insert own posts" ON posts;
CREATE POLICY "Users can insert own posts" 
ON posts FOR INSERT 
WITH CHECK (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can update own posts" ON posts;
CREATE POLICY "Users can update own posts" 
ON posts FOR UPDATE 
USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can delete own posts" ON posts;
CREATE POLICY "Users can delete own posts" 
ON posts FOR DELETE 
USING (auth.uid()::text = user_id);

-- Same for scheduled_posts
ALTER TABLE scheduled_posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own scheduled posts" ON scheduled_posts;
CREATE POLICY "Users can view own scheduled posts" 
ON scheduled_posts FOR SELECT 
USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can insert own scheduled posts" ON scheduled_posts;
CREATE POLICY "Users can insert own scheduled posts" 
ON scheduled_posts FOR INSERT 
WITH CHECK (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can update own scheduled posts" ON scheduled_posts;
CREATE POLICY "Users can update own scheduled posts" 
ON scheduled_posts FOR UPDATE 
USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can delete own scheduled posts" ON scheduled_posts;
CREATE POLICY "Users can delete own scheduled posts" 
ON scheduled_posts FOR DELETE 
USING (auth.uid()::text = user_id);
