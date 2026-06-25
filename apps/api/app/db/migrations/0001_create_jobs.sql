CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    external_id TEXT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    job_keywords TEXT[] NOT NULL DEFAULT '{}',
    location TEXT NOT NULL,
    employment_type TEXT NOT NULL,
    eligibility_tags TEXT[] NOT NULL DEFAULT '{}',
    deadline DATE,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'closed', 'deadline_unknown')),
    source_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    collected_at TIMESTAMPTZ NOT NULL,
    verified_at TIMESTAMPTZ NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    is_sample BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS jobs_source_external_id_uidx
    ON jobs (source_name, external_id)
    WHERE external_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS jobs_source_url_uidx
    ON jobs (source_url);

CREATE INDEX IF NOT EXISTS jobs_status_deadline_idx
    ON jobs (status, deadline);

CREATE INDEX IF NOT EXISTS jobs_job_keywords_gin_idx
    ON jobs USING gin (job_keywords);

CREATE INDEX IF NOT EXISTS jobs_eligibility_tags_gin_idx
    ON jobs USING gin (eligibility_tags);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS jobs_set_updated_at ON jobs;

CREATE TRIGGER jobs_set_updated_at
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
