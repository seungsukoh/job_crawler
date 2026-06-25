# 검증 기준

검증 기준은 `docs/requirements.md`의 요구사항 ID를 기준으로 관리한다. 기능이 완료되려면 관련 요구사항의 검증 기준을 만족해야 한다.

## 검증 방식

- Automated: 테스트 코드로 자동 확인
- Manual: 로컬 실행 또는 브라우저 확인
- Review: 코드/문서/정책 검토
- Metric: 베타 지표 또는 운영 지표로 확인

## 기능 검증 기준

| 요구사항 ID | 검증 기준 | 방식 | 단계 |
|---|---|---|---|
| FR-001 | 공고 목록 화면 또는 API에서 공고 배열을 조회할 수 있다. | Automated/Manual | API/UI |
| FR-002 | 목록 응답 또는 화면에 제목, 회사명, 직무 키워드, 지역, 고용형태, 마감일, 출처, 수집 시각이 포함된다. | Automated/Manual | API/UI |
| FR-003 | 키워드 입력 시 해당 키워드와 관련된 공고만 반환하거나 표시한다. | Automated/Manual | API/UI |
| FR-004 | 마감일 범위 조건에 맞는 공고만 반환하거나 표시한다. | Automated/Manual | API/UI |
| FR-005 | 공고 ID로 상세 정보를 조회하고 화면에 표시할 수 있다. | Automated/Manual | API/UI |
| FR-006 | 원문 링크가 존재하고 새 탭 또는 현재 탭으로 이동 가능하다. | Manual | UI |
| FR-007 | 관심 공고 저장/해제가 동작한다. | Manual/Automated | UI |
| FR-008 | 로그인 없이 새로고침 후에도 관심 공고가 localStorage 기준으로 유지된다. | Manual | UI |
| FR-009 | 마감 임박 기준에 해당하는 공고가 구분 표시된다. | Manual/Automated | UI |
| FR-010 | 수집 시각과 원문 확인 시각이 사용자에게 표시된다. | Manual | UI |
| FR-011 | 검색 API 또는 UI 검색 과정에서 외부 사이트로 네트워크 수집을 실행하지 않는다. | Review/Automated | API/Crawler |
| FR-012 | 수집 실행 경로가 사용자 검색 요청과 분리되어 있다. | Review | Crawler/API |
| FR-013 | Source Registry 상태가 `allowed` 또는 `conditional`인 소스만 수집한다. | Automated/Review | Crawler |
| FR-014 | 수집 실행 기록을 조회할 수 있다. | Manual/Automated | API/Admin |
| FR-015 | 저장 공고 상태를 변경하고 유지할 수 있다. | Manual | UI |

## 데이터 검증 기준

| 요구사항 ID | 검증 기준 | 방식 | 단계 |
|---|---|---|---|
| DR-001 | 저장된 공고에 원문 URL, 출처명, 수집 시각, 원문 확인 시각이 있다. | Automated/Review | DB/API |
| DR-002 | 동일 원문 또는 동일 외부 ID 공고가 중복 노출되지 않는다. | Automated/Metric | DB/API |
| DR-003 | 공고 본문 전문, 이미지, 첨부파일을 저장하지 않는다. | Review | DB/Crawler |
| DR-004 | 마감된 공고가 기본 목록에서 제외되거나 마감 상태로 표시된다. | Automated/Manual | API/UI |
| DR-005 | 삭제/중단 대상 공고가 재수집되지 않는다. | Automated/Review | Crawler |

## 시스템 검증 기준

| 요구사항 ID | 검증 기준 | 방식 | 단계 |
|---|---|---|---|
| SR-001 | `GET /health`가 HTTP 200과 `status: ok`를 반환한다. | Automated/Manual | API |
| SR-002 | 프론트엔드 API 주소가 코드 고정값이 아니라 환경 변수로 설정된다. | Review | Web |
| SR-003 | `uvicorn app.main:app`으로 API가 실행된다. | Manual | API |
| SR-004 | DB 설계가 PostgreSQL 표준 기능을 우선 사용한다. | Review | DB |
| SR-005 | DB schema 변경에 migration 파일이 포함된다. | Review/Manual | DB |
| SR-006 | 크롤러가 API 서버 프로세스와 독립된 CLI로 실행된다. | Review/Manual | Crawler |
| SR-007 | secret 실제 값이 Git에 커밋되지 않는다. | Review | All |

## 비기능 검증 기준

| 요구사항 ID | 검증 기준 | 방식 | 단계 |
|---|---|---|---|
| NFR-001 | 초기 배포 계획이 무료 티어 기준으로 작성되어 있다. | Review | Ops |
| NFR-002 | Web, API, Crawler, DB가 독립적으로 이전 가능한 구조다. | Review | Architecture |
| NFR-003 | 별도 검색 엔진 의존성이 없다. | Review | Architecture |
| NFR-004 | 크롤링 관련 기능이 `docs/crawling-policy.md`를 따른다. | Review | Crawler |
| NFR-005 | 사용자 화면 또는 API 응답에 출처와 수집 시각이 포함된다. | Manual/Automated | API/UI |
| NFR-006 | 작업 완료 후 상태/인수인계 문서가 갱신된다. | Review | Docs/Ops |

## 현재 구현 검증

| 항목 | 상태 | 확인 방법 |
|---|---|---|
| SR-001 | 구현, runtime 검증 대기 | `apps/api/tests/test_health.py`, `GET /health` |
| SR-002 | 구현, 정적 검증 통과, runtime 검증 대기 | `apps/web/src/lib/config.ts`, `NEXT_PUBLIC_API_BASE_URL` |
| FR-001 | API 구현, runtime 검증 대기 | `GET /jobs`, `apps/api/tests/test_jobs.py` |
| FR-002 | API 구현, runtime 검증 대기 | `apps/api/app/sample_data/sample_jobs.json`, `GET /jobs` |
| FR-003 | API 구현, runtime 검증 대기 | `GET /jobs?keyword=python` |
| FR-004 | API 구현, runtime 검증 대기 | `GET /jobs?deadline_from=2026-06-26&deadline_to=2026-06-30` |
| FR-005 | API 구현, runtime 검증 대기 | `GET /jobs/sample-job-004` |
| FR-010 | API 구현, runtime 검증 대기 | `collected_at`, `verified_at` fields in sample response |
| SR-004 | DB schema/migration 구현, runtime 검증 대기 | `infra/docker-compose.yml`, `apps/api/app/db/migrations/0001_create_jobs.sql` |
| SR-005 | SQL migration runner 구현, runtime 검증 대기 | `python -m app.db.migrate` |
| NFR-002 | 반영 | `apps/web`, `apps/api`, `crawler`, `infra` 분리 |
| NFR-006 | 반영 중 | `PROJECT_STATUS.md`, `SESSION_HANDOFF.md` |
