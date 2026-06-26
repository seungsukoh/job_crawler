# Session Handoff

이 파일은 토큰 리밋, 세션 종료, 컨텍스트 초기화가 발생했을 때 다음 세션에서 바로 이어가기 위한 인수인계 문서다.

## 다음 세션 시작 절차

1. `TEAM_SYNC.md`를 읽는다.
2. `CONTEXT_BRIEF.md`를 읽는다.
3. `PROJECT_STATUS.md`를 읽는다.
4. 이 파일의 `현재 중단 지점`과 `다음 명령`을 확인한다.
5. 작업과 직접 관련된 문서만 추가로 읽는다.
6. 작업을 이어간다.

## 현재 중단 지점

- 저장소 연결 완료
- 기획/로드맵/무료 배포/안전 수집 정책 문서화 완료
- 토큰 절약 작업 방식과 세션 인수인계 문서화 완료
- 전문가 그룹 검토를 통해 `apps/web`, `apps/api`, `crawler`, `infra`, `docs` 기반 모노리포 구조를 권장 구조로 확정
- `docs/mvp-implementation-strategy.md`에 MVP 구현 전략 기록 완료
- `apps/web`, `apps/api`, `crawler`, `infra` 기본 구조와 README 문서 생성 완료
- 루트 `README.md`, `.gitignore`, `.env.example` 생성 완료
- `apps/api`에 FastAPI 기본 앱과 `GET /health` 엔드포인트 생성 완료
- API 구조를 route/config/test 단위로 분리해 이후 병렬 작업 가능하게 구성
- PM 운영 체크리스트, 유지보수 원칙, 요구사항, 검증 기준 문서 생성 완료
- `TEAM_SYNC.md`로 병렬 작업용 공유 기준 파일 정리 완료
- `apps/api` AST 문법 검사는 통과했으나, FastAPI/pytest 의존성 설치가 DNS 문제로 실패해 runtime 테스트는 미실행
- `apps/web`은 React + Vite + TypeScript 앱으로 전환 완료
- Cloudflare Pages 설정 기준은 build command `npm run build`, output `dist`, env `VITE_API_BASE_URL`
- Cloudflare Pages가 저장소 루트에서 빌드해도 root build command `npm run build`가 루트 `dist/`를 생성하도록 지원
- `apps/web` API health 확인 화면 생성 완료
- `apps/web`에 공고 목록/상세 탐색 UI와 관심 공고 localStorage 저장 UI 추가 완료
- Web `npm.cmd run typecheck`, `npm.cmd run build` 통과
- Web Vite dev server `http://localhost:5173/` HTTP 200 확인
- `infra/docker-compose.yml`로 로컬 PostgreSQL Compose 설정 생성 완료
- `.env.example`에 로컬 DB용 `POSTGRES_*` 값을 추가하고 `DATABASE_URL`과 기본값을 맞춤
- `.env.example`의 frontend API 환경 변수는 `VITE_API_BASE_URL`
- FastAPI 기본 CORS origin에 Vite dev server `http://localhost:5173` 포함
- `infra/README.md`에 로컬 DB 실행/중지/초기화 절차 기록 완료
- `apps/api/app/sample_data/sample_jobs.json`에 synthetic 샘플 공고 10개 추가 완료
- `GET /jobs`, `GET /jobs/{id}`를 샘플 데이터 기반으로 구현 완료
- `GET /jobs`는 `keyword`, `deadline_from`, `deadline_to`, `include_closed` query parameter를 지원
- 샘플 jobs API 테스트 파일 `apps/api/tests/test_jobs.py` 추가 완료
- `JOB_DATA_SOURCE=sample|database` 설정으로 공고 API 데이터 소스를 전환하는 구조 추가 완료
- PostgreSQL `jobs` 테이블 SQL migration과 migration runner 추가 완료
- 샘플 공고 DB seed runner `python -m app.db.seed --clear-sample` 추가 완료
- DB-backed keyword 검색에서 SQL wildcard 문자를 literal로 처리하도록 escape 보강 완료

## 보류한 검증 항목

아래 검증은 승인, 네트워크, 의존성 설치, 로컬 도구가 필요한 단계라 현재 작업 흐름에서는 보류했다.

- API 의존성 설치: `apps/api`에서 `.venv\Scripts\python -m pip install -e ".[dev]"`
- API 테스트: `apps/api`에서 `python -m pytest`
- API DB migration: `apps/api`에서 `python -m app.db.migrate`
- API DB seed: `apps/api`에서 `python -m app.db.seed --clear-sample`
- Infra Compose 설정 확인: 루트에서 `docker compose -f infra/docker-compose.yml config`

API 의존성 설치는 승인 후에도 package index DNS resolution 실패로 완료하지 못했다. 우선순위가 꼬이지 않도록, 다음 개발 작업은 예정대로 진행하고 위 검증은 네트워크/승인/로컬 도구 조건이 맞을 때 별도 검증 작업으로 처리한다.

## 다음 명령

다음 개발 작업은 아래 순서로 시작한다.

```text
이번 작업: DB migration/seed/runtime API 검증
범위: Docker PostgreSQL 실행, API 의존성 설치, migration/seed 실행, JOB_DATA_SOURCE=database로 GET /jobs 확인
제외: 실제 외부 수집, Source Registry 구현, 관심 공고 저장, 배포 자동화, 인증
```

## 반드시 유지할 결정

- 사용자 검색 시점에 외부 사이트를 크롤링하지 않는다.
- 검색은 내부 DB 조회로 처리한다.
- 크롤링은 GitHub Actions 스케줄 또는 관리자 수동 실행으로만 수행한다.
- 수집 소스는 공식 API/RSS/직접 등록/허용된 공개 페이지부터 시작한다.
- 대형 민간 채용 플랫폼 무단 크롤링은 MVP 범위에서 제외한다.
- 진행 내용은 `PROJECT_STATUS.md`에 남긴다.
- 병렬 작업자는 `TEAM_SYNC.md`를 먼저 확인하고 요구사항/검증 기준과 작업 레인을 맞춘다.
- 세션이 길어지거나 문제가 생기면 `PROJECT_STATUS.md`와 `SESSION_HANDOFF.md`를 갱신하고, 커밋 후 GitHub에 push한 뒤 작업을 끊는다.

## 다음 세션에서 읽을 필요가 없는 문서

특별한 이유가 없으면 처음부터 아래 문서를 전문으로 읽지 않는다.

- `PROJECT_PLAN.md`
- `FREE_DEPLOYMENT_PLAN.md`
- `ROADMAP.md`

필요한 경우 관련 섹션만 확인한다.

## 세션 종료 전 체크리스트

- 변경사항이 있다면 테스트 또는 최소 확인을 수행했는가?
- `PROJECT_STATUS.md`를 갱신했는가?
- 다음 작업이 바뀌었다면 `CONTEXT_BRIEF.md`를 갱신했는가?
- 작업이 중간에 끊길 수 있다면 이 파일의 `현재 중단 지점`과 `다음 명령`을 갱신했는가?
- 끊김, 오류, 재시작 가능성이 있으면 현재 변경을 커밋하고 GitHub에 push했는가?
