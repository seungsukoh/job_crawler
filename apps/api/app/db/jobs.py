from __future__ import annotations

from datetime import date, datetime
from typing import Any

from app.db.connection import connect


JOB_RESPONSE_COLUMNS = (
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


def list_jobs_from_database(
    *,
    keyword: str | None = None,
    deadline_from: date | None = None,
    deadline_to: date | None = None,
    include_closed: bool = False,
) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if not include_closed:
        conditions.append("status <> 'closed'")

    if keyword:
        params["keyword_pattern"] = f"%{keyword}%"
        conditions.append(
            """
            (
              title ILIKE %(keyword_pattern)s
              OR company ILIKE %(keyword_pattern)s
              OR location ILIKE %(keyword_pattern)s
              OR employment_type ILIKE %(keyword_pattern)s
              OR summary ILIKE %(keyword_pattern)s
              OR EXISTS (
                SELECT 1
                FROM unnest(job_keywords || eligibility_tags) AS terms(term)
                WHERE terms.term ILIKE %(keyword_pattern)s
              )
            )
            """
        )

    if deadline_from:
        params["deadline_from"] = deadline_from
        conditions.append("deadline >= %(deadline_from)s")

    if deadline_to:
        params["deadline_to"] = deadline_to
        conditions.append("deadline <= %(deadline_to)s")

    sql = f"SELECT {', '.join(JOB_RESPONSE_COLUMNS)} FROM jobs"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY deadline IS NULL, deadline ASC, collected_at DESC, id ASC"

    with connect() as connection:
        rows = connection.execute(sql, params).fetchall()

    return [_serialize_job(row) for row in rows]


def get_job_from_database(job_id: str) -> dict[str, Any] | None:
    sql = f"SELECT {', '.join(JOB_RESPONSE_COLUMNS)} FROM jobs WHERE id = %(job_id)s"

    with connect() as connection:
        row = connection.execute(sql, {"job_id": job_id}).fetchone()

    return _serialize_job(row) if row else None


def _serialize_job(row: dict[str, Any]) -> dict[str, Any]:
    serialized = dict(row)
    for key, value in list(serialized.items()):
        if isinstance(value, (date, datetime)):
            serialized[key] = value.isoformat()
    return serialized
