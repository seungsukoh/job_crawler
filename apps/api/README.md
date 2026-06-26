# API App

FastAPI 백엔드가 들어갈 위치다.

## 역할

- 공고 조회 API
- 소스 조회 API
- 수집 실행 기록 조회 API
- 로컬/배포 환경 설정 관리

## 초기 API 범위

- `GET /health`
- `GET /jobs`
- `GET /jobs/{id}`
- `GET /sources`
- `GET /crawl-runs`

## 운영 방향

- Render Free 배포를 우선 고려한다.
- PostgreSQL은 `DATABASE_URL` 환경 변수로 연결한다.
- DB 변경은 `app/db/migrations`의 SQL migration 파일과 `python -m app.db.migrate`로 관리한다.
- 수집 작업은 API 서버 내부 작업으로 넣지 않고 `crawler/`의 독립 CLI로 분리한다.
- Render 배포는 저장소 루트 `render.yaml`을 기준으로 한다.

## 공고 샘플 API

기본값에서는 `GET /jobs`와 `GET /jobs/{id}`가 `app/sample_data/sample_jobs.json`의 synthetic sample 데이터를 반환한다. 이 데이터는 UI/API 계약 검증용이며 실제 채용 사이트에서 수집한 데이터가 아니다.

`JOB_DATA_SOURCE=database`로 설정하면 같은 API 계약을 PostgreSQL `jobs` 테이블에서 조회한다. 이 모드에서는 먼저 DB migration과 seed를 실행해야 한다.

`GET /jobs` query parameters:

- `keyword`: 제목, 회사명, 직무 키워드, 지역, 고용형태, 요약에서 대소문자 구분 없이 검색
- `deadline_from`: `YYYY-MM-DD` 형식의 시작 마감일
- `deadline_to`: `YYYY-MM-DD` 형식의 종료 마감일
- `include_closed`: 기본값 `false`; `true`면 마감된 샘플 공고도 포함

응답 형태:

```json
{
  "items": [
    {
      "id": "sample-job-001",
      "title": "Backend API Intern",
      "company": "CampusWorks",
      "job_keywords": ["backend", "python", "fastapi"],
      "location": "Seoul",
      "employment_type": "intern",
      "eligibility_tags": ["intern", "graduating_soon"],
      "deadline": "2026-06-27",
      "status": "active",
      "source_name": "Sample Source",
      "source_url": "https://example.com/jobs/sample-job-001",
      "collected_at": "2026-06-25T00:30:00+09:00",
      "verified_at": "2026-06-25T00:45:00+09:00",
      "summary": "Build internal API features for a student-facing product team.",
      "is_sample": true
    }
  ],
  "count": 1,
  "filters": {
    "keyword": "python",
    "deadline_from": null,
    "deadline_to": null,
    "include_closed": false
  },
  "data_source": "sample"
}
```

`GET /jobs/{id}`는 단일 공고 객체를 반환하고, 존재하지 않는 ID는 `404`를 반환한다. 샘플 데이터에는 공고 본문 전문, 이미지, 첨부파일을 포함하지 않는다.

## DB migration과 seed

로컬 PostgreSQL 실행 방법은 `infra/README.md`를 따른다.

API 개발 의존성 설치 후 migration을 실행한다.

```powershell
cd apps/api
python -m app.db.migrate
```

샘플 공고를 DB에 적재한다.

```powershell
python -m app.db.seed --clear-sample
```

DB-backed API를 확인하려면 API 실행 전에 환경 변수를 바꾼다.

```powershell
$env:JOB_DATA_SOURCE = "database"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

`GET /jobs`와 `GET /jobs/{id}`의 응답 필드는 sample mode와 database mode에서 동일하게 유지한다.

## 다음 작업

다음 백엔드 작업은 DB-backed jobs API를 runtime으로 검증하고, 필요하면 query 성능과 migration 방식을 보강하는 것이다. API 응답 형태가 바뀌면 Web 작업자가 볼 수 있도록 이 README와 검증 기준을 함께 갱신한다.

## 구조

```text
app/
  main.py          FastAPI app factory
  api/
    router.py      API router composition
    health.py      health endpoint
    jobs.py        sample-backed jobs endpoints
  db/
    connection.py  PostgreSQL connection helper
    jobs.py        DB-backed jobs queries
    migrate.py     SQL migration runner
    seed.py        sample data seed runner
    migrations/    SQL migration files
  services/
    jobs.py        sample job loading and filtering
  sample_data/
    sample_jobs.json synthetic seed jobs
  core/
    config.py      environment-based settings
tests/
  test_health.py
  test_jobs.py
```

새 API는 `app/api/<resource>.py`에 라우터를 만들고 `app/api/router.py`에 연결한다. 이렇게 하면 `jobs`, `sources`, `crawl-runs`를 병렬로 추가하기 쉽다.

## 로컬 실행

PowerShell 기준:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

확인:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

예상 응답:

```json
{
  "status": "ok",
  "service": "job-crawler-api",
  "version": "0.1.0",
  "environment": "local"
}
```

테스트:

```powershell
cd apps/api
python -m pytest
```
