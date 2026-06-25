from __future__ import annotations

from importlib import resources
import argparse
import json
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


UPSERT_SAMPLE_JOB_SQL = f"""
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


def load_sample_jobs() -> list[dict[str, Any]]:
    data_file = resources.files("app.sample_data").joinpath("sample_jobs.json")
    return json.loads(data_file.read_text(encoding="utf-8"))


def seed_sample_jobs(*, clear_sample: bool = False) -> int:
    jobs = load_sample_jobs()

    with connect() as connection:
        if clear_sample:
            connection.execute("DELETE FROM jobs WHERE is_sample = TRUE")

        with connection.cursor() as cursor:
            for job in jobs:
                cursor.execute(UPSERT_SAMPLE_JOB_SQL, _normalize_job(job))

        connection.commit()

    return len(jobs)


def _normalize_job(job: dict[str, Any]) -> dict[str, Any]:
    return {column: job.get(column) for column in JOB_COLUMNS}


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed synthetic sample jobs into PostgreSQL.")
    parser.add_argument(
        "--clear-sample",
        action="store_true",
        help="Delete existing sample jobs before upserting sample data.",
    )
    args = parser.parse_args()

    count = seed_sample_jobs(clear_sample=args.clear_sample)
    print(f"Seeded {count} sample jobs")


if __name__ == "__main__":
    main()
