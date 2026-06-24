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

다음 백엔드 작업에서 FastAPI 기본 앱과 `/health` 엔드포인트를 추가하고 실행 방법을 이 문서에 갱신한다.
