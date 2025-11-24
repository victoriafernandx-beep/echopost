-- Schema updates for UX/UI enhancements
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
