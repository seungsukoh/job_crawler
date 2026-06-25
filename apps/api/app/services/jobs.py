from __future__ import annotations

from datetime import date
from functools import lru_cache
from importlib import resources
import json
from typing import Any

from app.core.config import settings
from app.db.jobs import get_job_from_database, list_jobs_from_database


JobRecord = dict[str, Any]


@lru_cache
def load_sample_jobs() -> tuple[JobRecord, ...]:
    data_file = resources.files("app.sample_data").joinpath("sample_jobs.json")
    jobs = json.loads(data_file.read_text(encoding="utf-8"))
    return tuple(jobs)


def list_jobs(
    *,
    keyword: str | None = None,
    deadline_from: date | None = None,
    deadline_to: date | None = None,
    include_closed: bool = False,
) -> list[JobRecord]:
    if settings.job_data_source == "database":
        return list_jobs_from_database(
            keyword=keyword,
            deadline_from=deadline_from,
            deadline_to=deadline_to,
            include_closed=include_closed,
        )

    if settings.job_data_source != "sample":
        raise ValueError(f"Unsupported JOB_DATA_SOURCE: {settings.job_data_source}")

    jobs = list(load_sample_jobs())

    if not include_closed:
        jobs = [job for job in jobs if job["status"] != "closed"]

    if keyword:
        normalized_keyword = keyword.casefold()
        jobs = [job for job in jobs if _matches_keyword(job, normalized_keyword)]

    if deadline_from or deadline_to:
        jobs = [
            job
            for job in jobs
            if _is_within_deadline_range(job.get("deadline"), deadline_from, deadline_to)
        ]

    return jobs


def get_job(job_id: str) -> JobRecord | None:
    if settings.job_data_source == "database":
        return get_job_from_database(job_id)

    if settings.job_data_source != "sample":
        raise ValueError(f"Unsupported JOB_DATA_SOURCE: {settings.job_data_source}")

    return next((job for job in load_sample_jobs() if job["id"] == job_id), None)


def current_job_data_source() -> str:
    return settings.job_data_source


def _matches_keyword(job: JobRecord, normalized_keyword: str) -> bool:
    searchable_values = [
        job["title"],
        job["company"],
        job["location"],
        job["employment_type"],
        job["summary"],
        *job["job_keywords"],
        *job["eligibility_tags"],
    ]
    return any(normalized_keyword in str(value).casefold() for value in searchable_values)


def _is_within_deadline_range(
    deadline_value: str | None,
    deadline_from: date | None,
    deadline_to: date | None,
) -> bool:
    if deadline_value is None:
        return False

    deadline = date.fromisoformat(deadline_value)
    if deadline_from and deadline < deadline_from:
        return False
    if deadline_to and deadline > deadline_to:
        return False
    return True
