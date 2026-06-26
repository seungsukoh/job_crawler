from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from app.db.connection import connect


JOB_COLUMNS = (
    "id",
    "external_id",
    "title",
    "company",
    "job_keywords",
    "location",
    "employment_type",
    "eligibility_tags",
    "deadline",
    "status",
    "source_name",
    "source_url",
    "collected_at",
    "verified_at",
    "summary",
    "is_sample",
)


UPSERT_JOB_SQL = f"""
INSERT INTO jobs ({', '.join(JOB_COLUMNS)})
VALUES ({', '.join(f'%({column})s' for column in JOB_COLUMNS)})
ON CONFLICT (id) DO UPDATE SET
    external_id = EXCLUDED.external_id,
    title = EXCLUDED.title,
    company = EXCLUDED.company,
    job_keywords = EXCLUDED.job_keywords,
    location = EXCLUDED.location,
    employment_type = EXCLUDED.employment_type,
    eligibility_tags = EXCLUDED.eligibility_tags,
    deadline = EXCLUDED.deadline,
    status = EXCLUDED.status,
    source_name = EXCLUDED.source_name,
    source_url = EXCLUDED.source_url,
    collected_at = EXCLUDED.collected_at,
    verified_at = EXCLUDED.verified_at,
    summary = EXCLUDED.summary,
    is_sample = EXCLUDED.is_sample
"""


def upsert_jobs(jobs: Iterable[dict[str, Any]]) -> int:
    normalized_jobs = [_normalize_job(job) for job in jobs]
    if not normalized_jobs:
        return 0

    with connect() as connection:
        with connection.cursor() as cursor:
            for job in normalized_jobs:
                cursor.execute(UPSERT_JOB_SQL, job)

        connection.commit()

    return len(normalized_jobs)


def _normalize_job(job: dict[str, Any]) -> dict[str, Any]:
    return {column: job.get(column) for column in JOB_COLUMNS}
