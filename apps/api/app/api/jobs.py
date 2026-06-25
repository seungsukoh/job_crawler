from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.services.jobs import get_job, list_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def read_jobs(
    keyword: str | None = Query(default=None, min_length=1),
    deadline_from: date | None = None,
    deadline_to: date | None = None,
    include_closed: bool = False,
) -> dict[str, Any]:
    jobs = list_jobs(
        keyword=keyword,
        deadline_from=deadline_from,
        deadline_to=deadline_to,
        include_closed=include_closed,
    )
    return {
        "items": jobs,
        "count": len(jobs),
        "filters": {
            "keyword": keyword,
            "deadline_from": deadline_from.isoformat() if deadline_from else None,
            "deadline_to": deadline_to.isoformat() if deadline_to else None,
            "include_closed": include_closed,
        },
        "data_source": "sample",
    }


@router.get("/{job_id}")
def read_job(job_id: str) -> dict[str, Any]:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
