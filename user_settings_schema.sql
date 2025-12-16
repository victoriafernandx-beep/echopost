-- Create table for storing user preferences and settings
create table if not exists public.user_settings (
  user_id text not null,
  setting_key text not null,
  setting_value text,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
  primary key (user_id, setting_key)
);

-- Enable RLS (Optional, depending on your setup)
alter table public.user_settings enable row level security;

-- Policy: Users can view their own settings
create policy "Users can view their own settings"
  on public.user_settings for select
  using (auth.uid()::text = user_id or user_id = 'user_123'); -- Including default dev user

-- Policy: Users can update their own settings
create policy "Users can update their own settings"
  on public.user_settings for insert
  with check (auth.uid()::text = user_id or user_id = 'user_123');

create policy "Users can update their own settings update"
  on public.user_settings for update
  using (auth.uid()::text = user_id or user_id = 'user_123');
