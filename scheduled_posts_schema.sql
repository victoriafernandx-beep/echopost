-- Schema for scheduled posts feature
-- Run this in your Supabase SQL Editor to create the scheduled_posts table

CREATE TABLE IF NOT EXISTS scheduled_posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  content TEXT NOT NULL,
  topic TEXT,
  tags TEXT[],
  
  -- Scheduling info
  scheduled_time TIMESTAMPTZ NOT NULL,
  timezone TEXT DEFAULT 'UTC',
  status TEXT DEFAULT 'pending', -- pending, published, failed, cancelled
  
  -- Publishing info
  published_at TIMESTAMPTZ,
  linkedin_post_id TEXT,
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_status CHECK (status IN ('pending', 'published', 'failed', 'cancelled'))
);

-- Index for efficient queries by user and status
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_user_status 
ON scheduled_posts(user_id, status);

-- Index for finding posts ready to publish
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_scheduled_time 
ON scheduled_posts(scheduled_time) 
WHERE status = 'pending';

-- Index for user's scheduled posts ordered by time
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_user_time 
ON scheduled_posts(user_id, scheduled_time DESC);

-- Function to auto-update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to call the function before any update
DROP TRIGGER IF EXISTS update_scheduled_posts_updated_at ON scheduled_posts;
CREATE TRIGGER update_scheduled_posts_updated_at 
BEFORE UPDATE ON scheduled_posts
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE scheduled_posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own scheduled posts
CREATE POLICY "Users can view own scheduled posts" 
ON scheduled_posts FOR SELECT 
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub');

-- Policy: Users can insert their own scheduled posts
CREATE POLICY "Users can insert own scheduled posts" 
ON scheduled_posts FOR INSERT 
WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub');

-- Policy: Users can update their own scheduled posts
CREATE POLICY "Users can update own scheduled posts" 
ON scheduled_posts FOR UPDATE 
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub');

-- Policy: Users can delete their own scheduled posts
CREATE POLICY "Users can delete own scheduled posts" 
ON scheduled_posts FOR DELETE 
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub');
