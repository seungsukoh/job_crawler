# 프로젝트 현황

## 현재 결정 사항

- 저장소: `https://github.com/seungsukoh/job_crawler`
- 초기 운영 방식: 무료 티어 우선
- 프론트엔드 후보: Cloudflare Pages
- 백엔드 후보: Render Free
- DB 후보: Supabase Free
- 크롤러 실행: GitHub Actions 수동 실행에서 시작, 이후 하루 1~4회 예약 실행
- 검색 방식: 사용자 검색은 내부 DB 조회만 수행
- 수집 방식: 스케줄러 또는 관리자 수동 실행만 허용
- 안전 수집 원칙: 명시적으로 허용된 경로 우선, 불명확하면 수집하지 않음

## 2026-06-24 진행 내역

- GitHub 저장소 `seungsukoh/job_crawler` 연결 완료
- `PROJECT_PLAN.md` 작성
- `FREE_DEPLOYMENT_PLAN.md` 작성
- `ROADMAP.md` 작성
- `docs/crawling-policy.md` 작성
- 사용자 검색 시점 실시간 크롤링을 금지하고, 주기 수집 + DB 검색 구조를 공식 원칙으로 반영
- 토큰 절약을 위해 `CONTEXT_BRIEF.md`와 `docs/context-management.md` 작성
- 토큰 리밋/세션 종료 후 재개를 위해 `SESSION_HANDOFF.md` 작성

## 2026-06-25 진행 내역

- 전문가 그룹 관점으로 PM/제품전략, 기술 아키텍처, 크롤링/데이터 거버넌스 검토 수행
- MVP 방향을 `대학생용 신뢰 가능한 공고 탐색/저장 도구`로 확정
- 무료 운영과 배포 분리를 위해 `apps/web`, `apps/api`, `crawler`, `infra`, `docs` 기반 모노리포 구조를 권장 구조로 채택
- 전문가 그룹 결론을 `docs/mvp-implementation-strategy.md`에 기록
- 무료 운영에서 시작하되 유료 인프라로 쉽게 이전할 수 있도록 웹/API/크롤러/DB 경계를 분리하는 원칙을 명시
- 사용자 검색 시점 외부 크롤링 금지, Source Registry 기반 수집, 하루 1~2회부터 시작하는 수집 주기 원칙을 재확인
- `apps/web`, `apps/api`, `crawler`, `infra` 모노리포 기본 구조 생성
- 루트 `README.md`, `.gitignore`, `.env.example` 추가
- 각 영역별 README로 역할, 운영 방향, 다음 작업 범위 기록
- `apps/api`에 FastAPI 기본 앱과 `GET /health` 엔드포인트 추가
- API 구조를 `main`, `api/router`, 개별 route, `core/config`, `tests`로 분리해 병렬 작업이 가능하도록 구성
- `docs/development-lanes.md`로 API/Web/Crawler/Infra/PM 작업 경계 기록
- `docs/pm-operating-checklist.md`로 PM 책임, P0 수용 기준, 베타 검증 질문 정리
- `docs/engineering-principles.md`로 유지보수 가능한 개발 원칙 정리
- `docs/requirements.md`와 `docs/verification-criteria.md`로 요구사항 기반 검증 기준 수립
- `TEAM_SYNC.md`로 병렬 작업자가 공통으로 읽고 갱신해야 할 프로젝트 기준 파일 정리
- `apps/web`에 Next.js + TypeScript 기본 앱 추가
- 프론트엔드 API 주소를 `NEXT_PUBLIC_API_BASE_URL` 환경 변수 기준으로 분리
- Cloudflare Pages 정적 배포를 고려해 `next.config.mjs`에 `output: "export"` 설정
- API health 상태를 확인하는 기본 화면 추가
- `infra/docker-compose.yml`로 로컬 개발용 PostgreSQL Compose 설정 추가
- `.env.example`에 Compose와 API가 공유할 `POSTGRES_*` 로컬 DB 환경 변수 추가
- `infra/README.md`에 로컬 DB 실행, 상태 확인, 로그 확인, 중지, volume 초기화 방법 기록
- `apps/api/app/sample_data/sample_jobs.json`에 synthetic 샘플 공고 10개 추가
- `GET /jobs`, `GET /jobs/{id}`를 샘플 데이터 기반으로 구현
- `GET /jobs`에 `keyword`, `deadline_from`, `deadline_to`, `include_closed` query parameter 추가
- 샘플 공고 API 테스트 `apps/api/tests/test_jobs.py` 추가
- `JOB_DATA_SOURCE=sample|database` 기준으로 공고 API 데이터 소스를 전환하는 설정 추가
- PostgreSQL `jobs` 테이블 SQL migration `0001_create_jobs.sql` 추가
- SQL migration runner `python -m app.db.migrate` 추가
- 샘플 공고 DB seed runner `python -m app.db.seed --clear-sample` 추가
- `JOB_DATA_SOURCE=database`에서 같은 `GET /jobs`, `GET /jobs/{id}` 계약을 PostgreSQL에서 조회하는 DB query 경로 추가

## 2026-06-25 검증

- `apps/api` Python 파일 19개 AST 문법 검사 통과
- `apps/api/app/sample_data/sample_jobs.json` JSON 파싱 통과
- sample jobs service 로딩, keyword filter, detail lookup 확인 통과
- `DATABASE_URL`의 `postgresql+psycopg://` 값을 psycopg 접속용 `postgresql://`로 변환하는 정적 확인 통과
- sample mode에서 `GET /jobs` service 경로가 psycopg 미설치 상태에서도 동작하는지 확인
- `apps/web/package.json` JSON 파싱 통과
- `apps/web/next.config.mjs` Node 문법 검사 통과
- `NEXT_PUBLIC_API_BASE_URL` 환경 변수 사용 위치 확인
- 로컬 PostgreSQL Compose 설정이 `.env.example`의 기본 DB 값과 일치하는지 검토
- `npm.cmd --version` 확인: `11.13.0`
- `git diff --check` 통과
- `docker compose -f infra/docker-compose.yml config`는 현재 환경에 Docker CLI가 없어 실행하지 못함
- FastAPI/pytest runtime 테스트는 현재 환경에서 의존성 설치가 DNS 문제로 실패해 실행하지 못함
  - 실패 명령: `apps/api`에서 `.venv\Scripts\python -m pip install -e ".[dev]"`
  - 실패 원인: package index DNS resolution 실패
  - 후속 조치: 네트워크가 가능한 환경에서 `python -m pip install -e ".[dev]"` 후 `python -m pytest` 실행
- Next.js runtime/build/typecheck 검증은 사용자 요청에 따라 의존성 설치가 필요한 단계라 이번 작업에서는 실행하지 않음
  - 후속 조치: `apps/web`에서 `npm.cmd install`, `npm.cmd run typecheck`, `npm.cmd run build` 실행

## 2026-06-26 진행 내역

- `apps/web`에 공고 목록/상세 탐색 UI `JobExplorer` 추가
- `GET /jobs` 계약에 맞춘 Web API client `apps/web/src/lib/jobs.ts` 추가
- 키워드, 마감일 범위, 마감 포함 필터를 UI에서 호출하도록 연결
- 선택한 공고 상세, 원문 링크, 상태/마감일/출처/수집 시각 표시 추가
- 관심 공고를 `localStorage`에 저장/해제하는 최소 UI 추가
- 필터 초기화가 기본 조건으로 목록을 즉시 다시 조회하도록 보정
- DB-backed keyword 검색에서 `%`, `_`, `\`를 SQL wildcard가 아닌 literal 문자로 처리하도록 보강
- CSS `align-items: start`를 `flex-start`로 바꿔 Next.js build 경고 제거
- `apps/web`을 Next.js에서 React + Vite + TypeScript로 전환
- Cloudflare Pages 설정을 Vite 기준으로 정리: build command `npm run build`, output `dist`, env `VITE_API_BASE_URL`
- 저장소 루트에서도 `npm run build`가 `apps/web` Vite build를 실행하고 루트 `dist/`를 생성하도록 root workspace package 설정 추가
- Cloudflare Linux 빌드에서 Rollup native optional package가 누락되지 않도록 `@rollup/rollup-linux-x64-gnu` optional dependency를 명시
- 프론트엔드 API 환경 변수를 `NEXT_PUBLIC_API_BASE_URL`에서 `VITE_API_BASE_URL`로 변경
- 로컬 Vite dev server 포트 `5173`을 FastAPI CORS 기본 허용 origin에 추가
- API 미설정 또는 API 연결 실패 상태에서도 검색 화면이 비지 않도록 Web 내장 샘플 공고 fallback 추가

## 2026-06-26 검증

- `apps/web`에서 `npm.cmd run typecheck` 통과
- `apps/web`에서 `npm.cmd run build` 통과
- `apps/web`에서 `npm.cmd install --registry=https://registry.npmjs.org/`로 Vite 의존성 설치 및 lockfile 갱신
- `apps/web` Vite production build가 `dist/` 산출물 생성 확인
- `apps/web` Vite dev server `http://localhost:5173/` 실행 및 HTTP 200 확인
- 저장소 루트에서 `npm.cmd run build` 통과
- 저장소 루트 `dist/index.html` 생성 확인
- 저장소 루트에서 `npm.cmd run typecheck` 통과
- Web 내장 샘플 공고가 production bundle에 포함되는지 확인
- Rollup Linux optional dependency lockfile 엔트리 포함 확인
- `apps/api` Python 파일 20개 AST 파싱 통과
- DB keyword escape helper 직접 확인 통과
- `git diff --check` 통과
- `python -m compileall app tests -q`는 `__pycache__` 쓰기 권한 문제로 실패해 AST 파싱으로 대체

## 보류한 검증 항목

승인, 네트워크, 의존성 설치가 필요한 작업은 현재 순서를 꼬이게 만들 수 있어 보류한다. 아래 항목은 실행 가능한 환경이 준비되면 별도 검증 작업으로 처리한다.

| 영역 | 보류 항목 | 이유 | 실행 조건 |
|---|---|---|---|
| API | `.venv\Scripts\python -m pip install -e ".[dev]"` | package index DNS resolution 실패 | 네트워크/DNS 정상화 |
| API | `python -m pytest` | FastAPI/pytest 의존성 미설치 | API 의존성 설치 완료 |
| API | `python -m app.db.migrate` | psycopg 의존성 및 Docker/PostgreSQL 실행 필요 | API 의존성 설치와 로컬 DB 실행 완료 |
| API | `python -m app.db.seed --clear-sample` | psycopg 의존성 및 DB migration 필요 | migration 실행 완료 |
| Infra | `docker compose -f infra/docker-compose.yml config` | Docker CLI 미설치 | Docker Desktop 또는 Docker CLI 설치 |

## Git 반영 상태

주요 작업은 기능 단위 커밋으로 관리한다. 원격 push 여부는 `git status`, `git log`, `git remote -v`로 확인한다.

| 커밋 | 내용 |
|---|---|
| `f0d4cdf` | 모노리포 기본 구조 추가 |
| `08c8f6c` | FastAPI 기본 앱과 공유 계획 문서 추가 |
| `0ba9c8f` | Next.js Web 기본 앱 추가 |
| `1c84e59` | 보류한 검증 항목 문서화 |
| `025ea5c` | 로컬 PostgreSQL Docker Compose 설정 추가 |
| `da58dcd` | 샘플 공고 API 계약 추가 |
| `f1f2db5` | push된 프로젝트 상태 커밋 기록 |
| `764e434` | PostgreSQL jobs seed pipeline 추가 |
| `463e648` | 공고 탐색 UI 추가 |

## 현재 리스크

- DB 모델과 DB-backed 공고 API 경로는 생겼지만 runtime 검증은 아직 못 했다.
- 실제 수집 가능한 공공 API/RSS 소스가 확정되지 않았다.
- 무료 API 호스팅은 sleep으로 첫 응답이 느릴 수 있다.
- Supabase/Render/GitHub Actions 무료 한도 내에서 크롤러 실행 시간을 관리해야 한다.
- 민간 대형 채용 플랫폼은 무단 크롤링하지 않는 전제로 대체 소스 확보가 필요하다.
- 현재 로컬 환경에서 Python 의존성 설치가 네트워크 DNS 문제로 막혀 FastAPI runtime 테스트는 미실행 상태다.
- Cloudflare Pages 배포 후 실제 Pages 도메인을 API `ALLOWED_ORIGINS`에 추가해야 한다.

## 다음 작업

1. DB migration/seed/runtime API 검증
2. 안전한 첫 수집 소스 후보 조사 및 Source Registry 초안 작성
3. GitHub Actions CI 또는 최소 검증 자동화 추가
4. Cloudflare Pages 프로젝트 연결과 API CORS 설정 확인
5. DB-backed jobs API query 성능과 검색 semantics 보강

## 진행 기록 규칙

새 기능, 정책 변경, 배포 변경, 크롤링 소스 추가, 리스크 발견, 테스트 결과는 이 파일에 날짜별로 기록한다.

토큰 리밋, 오류, 세션 재시작 가능성이 있으면 `PROJECT_STATUS.md`와 `SESSION_HANDOFF.md`를 갱신하고 커밋한 뒤 GitHub에 push한다.
