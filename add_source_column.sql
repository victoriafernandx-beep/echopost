-- Add 'source' column to track if post came from 'web' or 'whatsapp'
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS source text DEFAULT 'web';

-- Optional: Add metrics columns if you haven't already (Good for manual import)
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS likes integer DEFAULT 0;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS comments integer DEFAULT 0;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS shares integer DEFAULT 0;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS views integer DEFAULT 0;
