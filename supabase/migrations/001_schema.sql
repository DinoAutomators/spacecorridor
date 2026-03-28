-- SpaceCorridor Database Schema

create table if not exists ports (
  id text primary key,
  name text not null,
  country text not null,
  lat float8 not null,
  lng float8 not null,
  harbor_type text,
  cargo_capability text[],
  services_score int default 0,
  strategic_score int default 0,
  no2_mean float8 default 0,
  viirs_mean float8 default 0
);

create table if not exists corridors (
  id text primary key,
  name text not null,
  from_port_id text references ports(id),
  to_port_id text references ports(id),
  region text not null,
  geometry jsonb,
  description text
);

create table if not exists corridor_scores (
  id text primary key,
  corridor_id text unique references corridors(id),
  emissions_score int default 0,
  no2_score int default 0,
  lights_score int default 0,
  strategic_score int default 0,
  feasibility_score int default 0,
  readiness_score float8 default 0,
  bottleneck text,
  recommendation text,
  ai_explanation text
);

-- RLS: public read for anon
alter table ports enable row level security;
alter table corridors enable row level security;
alter table corridor_scores enable row level security;

create policy "Public read ports" on ports for select using (true);
create policy "Public read corridors" on corridors for select using (true);
create policy "Public read corridor_scores" on corridor_scores for select using (true);
