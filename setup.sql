-- Enable the pgvector extension to work with embeddings
create extension if not exists vector;

-- Create the jobs table
create table if not exists jobs (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  company text not null,
  location text,
  description text,
  required_skills text[],
  experience_required text,
  embedding vector(384),
  unique(title, company)
);

-- Create a function to search for jobs by similarity
create or replace function match_jobs (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  title text,
  company text,
  location text,
  description text,
  required_skills text[],
  experience_required text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    jobs.id,
    jobs.title,
    jobs.company,
    jobs.location,
    jobs.description,
    jobs.required_skills,
    jobs.experience_required,
    1 - (jobs.embedding <=> query_embedding) as similarity
  from jobs
  where 1 - (jobs.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
end;
$$;
