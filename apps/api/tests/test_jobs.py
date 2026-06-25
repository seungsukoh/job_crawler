from fastapi.testclient import TestClient

from app.main import app


def test_list_jobs_returns_sample_items_without_closed_jobs() -> None:
    client = TestClient(app)

    response = client.get("/jobs")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data_source"] == "sample"
    assert payload["count"] == 9
    assert payload["items"]
    assert all(job["status"] != "closed" for job in payload["items"])
    assert {
        "id",
        "title",
        "company",
        "job_keywords",
        "location",
        "employment_type",
        "deadline",
        "source_name",
        "source_url",
        "collected_at",
        "verified_at",
    }.issubset(payload["items"][0])
    assert "body" not in payload["items"][0]


def test_list_jobs_filters_by_keyword() -> None:
    client = TestClient(app)

    response = client.get("/jobs", params={"keyword": "python"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert all("python" in job["job_keywords"] for job in payload["items"])


def test_list_jobs_filters_by_deadline_range() -> None:
    client = TestClient(app)

    response = client.get(
        "/jobs",
        params={
            "deadline_from": "2026-06-26",
            "deadline_to": "2026-06-30",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert [job["id"] for job in payload["items"]] == ["sample-job-001", "sample-job-002"]


def test_list_jobs_can_include_closed_jobs() -> None:
    client = TestClient(app)

    response = client.get("/jobs", params={"include_closed": "true"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 10
    assert any(job["status"] == "closed" for job in payload["items"])


def test_get_job_returns_detail() -> None:
    client = TestClient(app)

    response = client.get("/jobs/sample-job-004")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "sample-job-004"
    assert payload["source_url"].startswith("https://example.com/jobs/")
    assert payload["is_sample"] is True


def test_get_job_returns_404_for_unknown_id() -> None:
    client = TestClient(app)

    response = client.get("/jobs/unknown")

    assert response.status_code == 404
