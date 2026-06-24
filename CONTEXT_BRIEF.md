# Context Brief

이 파일은 토큰 사용량을 줄이기 위한 짧은 프로젝트 브리프다. 새 작업을 시작할 때는 이 파일과 `PROJECT_STATUS.md`를 먼저 읽고, 필요한 경우에만 세부 문서를 연다.

## 프로젝트

- 이름: `job_crawler`
- 저장소: `https://github.com/seungsukoh/job_crawler`
- 목적: 대학생이 직무 키워드와 기간 기준으로 채용 공고를 모아 보고 저장할 수 있는 웹앱
- 초기 포지션: 대학생을 위한 직무 키워드 기반 채용 공고 캘린더

## 현재 결정

- 무료 운영 우선
- 구조: `apps/web`, `apps/api`, `crawler`, `infra`, `docs` 기반 모노리포
- Frontend: Next.js + TypeScript, Cloudflare Pages 후보
- Backend: Python FastAPI, Render Free 후보
- DB: PostgreSQL, Supabase Free 후보
- Crawler: GitHub Actions 수동 실행에서 시작, 이후 하루 1~4회 예약 실행
- 검색: 사용자 요청 시 외부 사이트를 긁지 않고 내부 DB만 조회
- 수집: 스케줄러 또는 관리자 수동 실행으로만 수행
- 안전 수집: 공식 API/RSS/직접 등록/허용된 공개 페이지 우선
- 금지: 대형 민간 채용 플랫폼 무단 대량 크롤링, 로그인/CAPTCHA/차단 우회, 공고 본문 전문 복제

## 핵심 문서

- `PROJECT_STATUS.md`: 최신 진행 상황과 다음 작업
- `SESSION_HANDOFF.md`: 토큰 리밋/세션 종료 후 재개 지점
- `ROADMAP.md`: 6주 MVP 로드맵과 우선순위
- `docs/mvp-implementation-strategy.md`: 전문가 그룹 검토 기반 MVP 구현 전략
- `docs/crawling-policy.md`: 안전 수집 정책
- `FREE_DEPLOYMENT_PLAN.md`: 무료 운영 배포 전략
- `PROJECT_PLAN.md`: 초기 제품/기술 기획 전체본
- `docs/context-management.md`: 토큰 절약 작업 방식

## 다음 작업

1. FastAPI 백엔드 기본 앱 추가
2. Next.js 프론트엔드 기본 앱 추가
3. 로컬 개발용 PostgreSQL Docker Compose 추가
4. 샘플 공고 seed 데이터 추가
5. 공고 목록/상세 API 구현
6. 공고 목록/상세 UI 구현
7. 안전한 첫 수집 소스 후보 조사 및 Source Registry 초안 작성

## 작업 원칙

- 한 번에 한 기능 단위로 진행한다.
- 큰 설명은 문서에 기록하고, 대화에는 결정/결과/다음 행동만 간단히 남긴다.
- 작업 후 `PROJECT_STATUS.md`를 갱신한다.
- 크롤링 관련 변경은 `docs/crawling-policy.md` 기준으로 검토한다.
- 프론트엔드 구현 후에는 브라우저로 실제 화면을 확인한다.
