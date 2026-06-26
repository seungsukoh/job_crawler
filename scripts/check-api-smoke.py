from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test a deployed job-crawler API.")
    parser.add_argument(
        "--api-base-url",
        default=os.getenv("API_BASE_URL", ""),
        help="Deployed API base URL, for example https://service.onrender.com.",
    )
    parser.add_argument(
        "--expected-min-jobs",
        default=int(os.getenv("EXPECTED_MIN_JOBS", "1")),
        type=int,
        help="Minimum number of jobs expected from GET /jobs.",
    )
    args = parser.parse_args()

    api_base_url = args.api_base_url.strip()
    if not api_base_url:
        raise SystemExit("API base URL is required.")

    health = _get_json(api_base_url, "/health")
    if health.get("status") != "ok":
        raise SystemExit(f"Unexpected health response: {health}")

    jobs = _get_json(api_base_url, "/jobs")
    items = jobs.get("items")
    if not isinstance(items, list):
        raise SystemExit(f"Unexpected jobs response shape: {jobs}")

    if len(items) < args.expected_min_jobs:
        raise SystemExit(
            f"Expected at least {args.expected_min_jobs} jobs, received {len(items)}."
        )

    print(
        json.dumps(
            {
                "status": "ok",
                "api_base_url": api_base_url,
                "job_count": len(items),
                "data_source": jobs.get("data_source"),
            },
            indent=2,
            sort_keys=True,
        )
    )


def _get_json(api_base_url: str, path: str) -> dict[str, Any]:
    url = urljoin(api_base_url.rstrip("/") + "/", path.lstrip("/"))
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as error:
        raise SystemExit(f"HTTP {error.code} from {url}") from error
    except URLError as error:
        raise SystemExit(f"Failed to connect to {url}: {error.reason}") from error

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON from {url}: {payload[:200]}") from error

    if not isinstance(data, dict):
        raise SystemExit(f"Expected JSON object from {url}.")
    return data


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as error:  # noqa: BLE001 - command-line smoke test should fail clearly.
        print(f"Smoke test failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
