from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import re
from typing import Any

import httpx

from crawler.config import SourceDefinition


SUPPORTED_SOURCE_TYPES = {"greenhouse", "lever"}


KEYWORD_ALIASES = {
    "android": ("android", "kotlin"),
    "backend": ("backend", "back-end", "server", "api", "python", "django", "fastapi"),
    "cloud": ("cloud", "devops", "platform", "infra", "infrastructure", "linux"),
    "data": ("data", "analytics", "analyst", "sql", "bi"),
    "frontend": ("frontend", "front-end", "react", "typescript", "javascript", "ui"),
    "intern": ("intern", "internship"),
    "ios": ("ios", "swift"),
    "marketing": ("marketing", "growth"),
    "mobile": ("mobile", "android", "ios", "app"),
    "product": ("product", "pm", "program manager"),
    "qa": ("qa", "quality", "test", "testing"),
    "react": ("react",),
    "security": ("security", "secops"),
    "sql": ("sql",),
    "ux": ("ux", "user research", "design"),
}


def collect_source(
    source: SourceDefinition,
    client: httpx.Client,
    collected_at: datetime,
) -> list[dict[str, Any]]:
    if source.source_type == "greenhouse":
        return collect_greenhouse(source, client, collected_at)
    if source.source_type == "lever":
        return collect_lever(source, client, collected_at)
    raise ValueError(f"Unsupported source type: {source.source_type}")


def collect_greenhouse(
    source: SourceDefinition,
    client: httpx.Client,
    collected_at: datetime,
) -> list[dict[str, Any]]:
    if not source.board_token:
        raise ValueError(f"Greenhouse source {source.name!r} requires board_token.")

    url = f"https://boards-api.greenhouse.io/v1/boards/{source.board_token}/jobs"
    response = client.get(url, params={"content": "false"})
    response.raise_for_status()
    payload = response.json()
    jobs = payload.get("jobs", []) if isinstance(payload, dict) else []

    return [_from_greenhouse_job(source, job, collected_at) for job in jobs]


def collect_lever(
    source: SourceDefinition,
    client: httpx.Client,
    collected_at: datetime,
) -> list[dict[str, Any]]:
    if not source.company:
        raise ValueError(f"Lever source {source.name!r} requires company.")

    url = f"https://api.lever.co/v0/postings/{source.company}"
    response = client.get(url, params={"mode": "json"})
    response.raise_for_status()
    payload = response.json()
    jobs = payload if isinstance(payload, list) else []

    return [_from_lever_job(source, job, collected_at) for job in jobs]


def _from_greenhouse_job(
    source: SourceDefinition,
    job: dict[str, Any],
    collected_at: datetime,
) -> dict[str, Any]:
    external_id = str(job.get("id") or job.get("absolute_url") or "")
    title = _clean_text(job.get("title"), fallback="Untitled role")
    source_url = _clean_text(job.get("absolute_url"), fallback="")
    location = _nested_name(job.get("location")) or "Unspecified"
    departments = [
        _clean_text(item.get("name"), fallback="") for item in job.get("departments") or []
    ]
    offices = [_clean_text(item.get("name"), fallback="") for item in job.get("offices") or []]
    company = source.name
    summary = _summary(title=title, company=company, location=location)

    return {
        "id": _job_id(source.name, external_id, source_url),
        "external_id": external_id or None,
        "title": title,
        "company": company,
        "job_keywords": _keywords(source, [title, location, *departments, *offices]),
        "location": location,
        "employment_type": source.employment_type or _employment_type(title),
        "eligibility_tags": list(source.eligibility_tags),
        "deadline": None,
        "status": "active",
        "source_name": source.name,
        "source_url": source_url or f"https://boards.greenhouse.io/{source.board_token}",
        "collected_at": collected_at.isoformat(),
        "verified_at": collected_at.isoformat(),
        "summary": summary,
        "is_sample": False,
    }


def _from_lever_job(
    source: SourceDefinition,
    job: dict[str, Any],
    collected_at: datetime,
) -> dict[str, Any]:
    categories = job.get("categories") if isinstance(job.get("categories"), dict) else {}
    external_id = str(job.get("id") or "")
    title = _clean_text(job.get("text"), fallback="Untitled role")
    source_url = _clean_text(job.get("hostedUrl") or job.get("applyUrl"), fallback="")
    location = _clean_text(categories.get("location"), fallback="Unspecified")
    team = _clean_text(categories.get("team"), fallback="")
    commitment = _clean_text(categories.get("commitment"), fallback="")
    company = source.name

    return {
        "id": _job_id(source.name, external_id, source_url),
        "external_id": external_id or None,
        "title": title,
        "company": company,
        "job_keywords": _keywords(source, [title, location, team, commitment]),
        "location": location,
        "employment_type": source.employment_type or _employment_type(f"{title} {commitment}"),
        "eligibility_tags": list(source.eligibility_tags),
        "deadline": None,
        "status": "active",
        "source_name": source.name,
        "source_url": source_url or f"https://jobs.lever.co/{source.company}",
        "collected_at": collected_at.isoformat(),
        "verified_at": _lever_timestamp(job.get("updatedAt")) or collected_at.isoformat(),
        "summary": _summary(title=title, company=company, location=location),
        "is_sample": False,
    }


def _keywords(source: SourceDefinition, values: list[str]) -> list[str]:
    text = " ".join(values).casefold()
    keywords = set(source.keywords)
    for keyword, aliases in KEYWORD_ALIASES.items():
        if any(alias in text for alias in aliases):
            keywords.add(keyword)
    return sorted(keywords)


def _employment_type(value: str) -> str:
    normalized = value.casefold()
    if "intern" in normalized or "internship" in normalized:
        return "intern"
    if "part-time" in normalized or "part time" in normalized:
        return "part_time"
    return "entry_level"


def _job_id(source_name: str, external_id: str, source_url: str) -> str:
    stable_value = external_id or source_url
    if not stable_value:
        stable_value = hashlib.sha1(f"{source_name}:{datetime.now(timezone.utc)}".encode()).hexdigest()
    source_slug = _slug(source_name)
    value_slug = _slug(stable_value)
    if len(value_slug) > 80:
        value_slug = hashlib.sha1(stable_value.encode()).hexdigest()
    return f"{source_slug}-{value_slug}"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "unknown"


def _clean_text(value: Any, *, fallback: str) -> str:
    if value is None:
        return fallback
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or fallback


def _nested_name(value: Any) -> str | None:
    if isinstance(value, dict):
        return _clean_text(value.get("name"), fallback="") or None
    return None


def _summary(*, title: str, company: str, location: str) -> str:
    return f"{company} is hiring for {title} in {location}."


def _lever_timestamp(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
