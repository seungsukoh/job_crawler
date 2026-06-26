from __future__ import annotations

import argparse
from datetime import datetime, timezone
import sys
import time

import httpx

from crawler.config import active_sources, load_settings, load_sources
from crawler.sources import SUPPORTED_SOURCE_TYPES, collect_source


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Collect approved job sources into PostgreSQL.")
    parser.add_argument(
        "--sources-file",
        help="Optional JSON source registry file. Defaults to CRAWLER_SOURCES_JSON or crawler/sources.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and normalize jobs without writing them to the database.",
    )
    args = parser.parse_args(argv)

    settings = load_settings()
    sources = active_sources(load_sources(args.sources_file))
    if not sources:
        print("No active crawler sources configured.")
        return

    collected_at = datetime.now(timezone.utc)
    jobs: list[dict[str, object]] = []
    failures = 0

    with httpx.Client(
        headers={"User-Agent": settings.user_agent, "Accept": "application/json"},
        timeout=settings.timeout_seconds,
    ) as client:
        for index, source in enumerate(sources):
            if source.source_type not in SUPPORTED_SOURCE_TYPES:
                print(f"Skipping unsupported source type: {source.name} ({source.source_type})")
                continue

            if index > 0 and settings.rate_limit_seconds > 0:
                time.sleep(settings.rate_limit_seconds)

            try:
                source_jobs = collect_source(source, client, collected_at)
                if settings.max_jobs_per_source is not None:
                    source_jobs = source_jobs[: settings.max_jobs_per_source]
                jobs.extend(source_jobs)
                print(f"Collected {len(source_jobs)} jobs from {source.name}.")
            except Exception as error:  # noqa: BLE001 - keep source failures isolated in scheduled runs.
                failures += 1
                print(f"Failed to collect {source.name}: {error}", file=sys.stderr)

    if args.dry_run:
        print(f"Dry run complete. Normalized {len(jobs)} jobs.")
    else:
        from app.db.upsert import upsert_jobs

        upserted_count = upsert_jobs(jobs)
        print(f"Upserted {upserted_count} jobs.")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
