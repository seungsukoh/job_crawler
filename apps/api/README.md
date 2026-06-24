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
- DB 변경은 Alembic migration으로 관리한다.
- 수집 작업은 API 서버 내부 작업으로 넣지 않고 `crawler/`의 독립 CLI로 분리한다.

## 다음 작업

다음 백엔드 작업은 DB 없이 공고 목록/상세 API의 요청/응답 형태를 먼저 잡는 것이다.

## 구조

```text
app/
  main.py          FastAPI app factory
  api/
    router.py      API router composition
    health.py      health endpoint
  core/
    config.py      environment-based settings
tests/
  test_health.py
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
