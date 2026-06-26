from __future__ import annotations

from importlib import resources
import argparse
import json
from typing import Any

from app.db.connection import connect
from app.db.upsert import upsert_jobs


def load_sample_jobs() -> list[dict[str, Any]]:
    data_file = resources.files("app.sample_data").joinpath("sample_jobs.json")
    return json.loads(data_file.read_text(encoding="utf-8"))


def seed_sample_jobs(*, clear_sample: bool = False) -> int:
    jobs = load_sample_jobs()

    if clear_sample:
        with connect() as connection:
            connection.execute("DELETE FROM jobs WHERE is_sample = TRUE")
            connection.commit()

    return upsert_jobs(jobs)


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
