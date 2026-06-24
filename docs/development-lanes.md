# 병렬 개발 작업 경계

여러 작업을 동시에 진행할 때 파일 소유권과 계약을 분리해 충돌을 줄인다.

## 작업 레인

| 레인 | 소유 범위 | 주요 산출물 | 먼저 맞춰야 할 계약 |
|---|---|---|---|
| API | `apps/api` | FastAPI route, schema, tests | HTTP endpoint와 JSON response |
| Web | `apps/web` | 화면, API client, localStorage 저장 | API base URL, response type |
| Crawler | `crawler` | 수집 CLI, source adapter | Source Registry schema, normalized item |
| Infra | `infra`, `.github` | Docker Compose, CI, scheduler | env var name, command entrypoint |
| PM | `PROJECT_STATUS.md`, `ROADMAP.md`, `docs/pm-operating-checklist.md` | 범위, 우선순위, 수용 기준, 지표 | MVP 정의와 완료 기준 |
| Docs/Ops | `docs`, root docs | 정책, status, handoff | 결정 사항과 진행 상태 |

## 병렬 작업 규칙

- 한 작업은 가능한 한 한 레인 안의 파일만 수정한다.
- 다른 레인과 맞물리는 변경은 문서나 schema를 먼저 갱신한다.
- 구조 변경은 `docs/engineering-principles.md` 기준을 먼저 확인한다.
- 기능 작업은 `docs/requirements.md`의 요구사항 ID와 `docs/verification-criteria.md`의 검증 기준을 연결한다.
- API 응답 형태가 바뀌면 Web 작업자가 볼 수 있도록 README 또는 API contract 문서를 함께 갱신한다.
- DB schema가 바뀌면 API, Crawler, Infra 레인이 모두 영향받으므로 migration과 상태 문서를 함께 갱신한다.
- 크롤링 관련 변경은 `docs/crawling-policy.md` 기준을 통과해야 한다.
- 실제 secret 값은 어느 레인에서도 커밋하지 않는다.

## 가까운 병렬화 가능 작업

1. API 레인: `GET /jobs`, `GET /jobs/{id}`의 mock 또는 seed 기반 응답 설계
2. Web 레인: 공고 목록/상세 화면 skeleton과 API client 구조
3. Infra 레인: 로컬 PostgreSQL Docker Compose
4. Crawler 레인: Source Registry schema 초안과 첫 안전 소스 후보 조사
5. PM 레인: P0 기능별 수용 기준과 베타 검증 질문 관리

처음에는 API contract가 Web/Crawler/Infra의 기준점이 되므로 API 응답 형태를 작게 먼저 고정한다.
