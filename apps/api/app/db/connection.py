from __future__ import annotations

from typing import Any

from app.core.config import settings


def database_url_for_psycopg(database_url: str | None = None) -> str:
    url = database_url or settings.database_url
    if url.startswith("postgresql+psycopg://"):
        return "postgresql://" + url.removeprefix("postgresql+psycopg://")
    return url


def connect() -> Any:
    import psycopg
    from psycopg.rows import dict_row

    return psycopg.connect(database_url_for_psycopg(), row_factory=dict_row)
