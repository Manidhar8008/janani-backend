create extension if not exists pgcrypto;

create table if not exists public.writing_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  device_id text,
  source text not null check (source in ('mobile_text','mobile_camera','pen','import')),
  content_text text not null default '',
  media_url text,
  captured_at timestamptz not null default now(),
  word_count integer not null default 0,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists writing_events_user_time_idx on public.writing_events(user_id, captured_at desc);

create table if not exists public.behavior_snapshots (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  period_start date not null,
  period_end date not null,
  discipline_score numeric(5,2) not null,
  consistency_score numeric(5,2) not null default 0,
  clarity_score numeric(5,2) not null default 0,
  completion_score numeric(5,2) not null default 0,
  progress_score numeric(5,2) not null default 0,
  evidence jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.insights (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  behavior_snapshot_id uuid references public.behavior_snapshots(id) on delete set null,
  kind text not null,
  title text not null,
  body text not null,
  evidence_event_ids uuid[] not null default '{}',
  created_at timestamptz not null default now()
);

create table if not exists public.action_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  insight_id uuid references public.insights(id) on delete set null,
  action text not null,
  status text not null default 'open' check (status in ('open','done','dismissed')),
  due_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.devices (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  device_type text not null,
  device_name text,
  firmware_version text,
  last_seen_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- RLS should be enabled before production use. Policies must bind user_id to auth.uid().
-- Do not expose service-role credentials in the PWA.
