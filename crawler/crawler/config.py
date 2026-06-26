from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_SOURCES_FILE = Path("crawler/sources.json")


@dataclass(frozen=True)
class CrawlerSettings:
    user_agent: str
    timeout_seconds: float
    rate_limit_seconds: float
    max_jobs_per_source: int | None


@dataclass(frozen=True)
class SourceDefinition:
    source_type: str
    name: str
    status: str
    board_token: str | None
    company: str | None
    keywords: tuple[str, ...]
    eligibility_tags: tuple[str, ...]
    employment_type: str | None

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> SourceDefinition:
        return cls(
            source_type=str(value.get("type", "")).strip().lower(),
            name=str(value.get("name", "")).strip(),
            status=str(value.get("status", "paused")).strip().lower(),
            board_token=_optional_string(value.get("board_token")),
            company=_optional_string(value.get("company")),
            keywords=_string_tuple(value.get("keywords", [])),
            eligibility_tags=_string_tuple(value.get("eligibility_tags", [])),
            employment_type=_optional_string(value.get("employment_type")),
        )


def load_settings() -> CrawlerSettings:
    return CrawlerSettings(
        user_agent=os.getenv("CRAWLER_USER_AGENT")
        or "job-crawler/0.1 contact:replace-with-email@example.com",
        timeout_seconds=float(os.getenv("CRAWLER_DEFAULT_TIMEOUT_SECONDS", "20")),
        rate_limit_seconds=float(os.getenv("CRAWLER_DEFAULT_RATE_LIMIT_SECONDS", "3")),
        max_jobs_per_source=_optional_int(os.getenv("CRAWLER_MAX_JOBS_PER_SOURCE")),
    )


def load_sources(sources_file: str | None = None) -> list[SourceDefinition]:
    raw_sources = os.getenv("CRAWLER_SOURCES_JSON")

    if raw_sources:
        payload = json.loads(raw_sources)
    else:
        path_value = sources_file or os.getenv("CRAWLER_SOURCES_FILE")
        source_path = Path(path_value) if path_value else DEFAULT_SOURCES_FILE
        if not source_path.exists():
            return []
        payload = json.loads(source_path.read_text(encoding="utf-8"))

    items = payload.get("sources", payload) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("Crawler source configuration must be a JSON list or {'sources': [...]}.")

    return [SourceDefinition.from_mapping(item) for item in items if isinstance(item, dict)]


def active_sources(sources: list[SourceDefinition]) -> list[SourceDefinition]:
    return [source for source in sources if source.status in {"allowed", "conditional"}]


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def _optional_int(value: str | None) -> int | None:
    if not value:
        return None
    return int(value)
