# job_crawler

대학생이 직무 키워드와 마감일 기준으로 채용 공고를 찾고 저장할 수 있는 웹앱 프로젝트다.

초기 목표는 채용 플랫폼 전체를 만드는 것이 아니라, 신뢰할 수 있는 최신 공고 탐색 경험을 작게 검증하는 것이다. 사용자 검색은 외부 사이트를 직접 크롤링하지 않고, 사전에 수집된 내부 DB만 조회한다.

## 현재 방향

- Frontend: Next.js + TypeScript
- Backend: FastAPI
- Database: PostgreSQL
- Crawler: Python CLI
- Frontend hosting: Cloudflare Pages 후보
- API hosting: Render Free 후보
- DB hosting: Supabase Free 후보
- Scheduler: GitHub Actions 수동 실행에서 시작

## 구조

```text
apps/
  web/        Next.js frontend
  api/        FastAPI backend
crawler/      scheduled/manual collection CLI
infra/        local and deployment support files
docs/         planning, policy, operation documents
```

## 개발 순서

1. FastAPI `/health` 앱 추가
2. Next.js 기본 앱 추가
3. 로컬 PostgreSQL Docker Compose 추가
4. 샘플 공고 seed 데이터 추가
5. 공고 목록/상세 API 구현
6. 공고 목록/상세 UI 구현
7. Source Registry 모델 추가
8. GitHub Actions 수동 크롤러 실행 추가

## 로컬 실행

아직 실제 앱 코드는 생성하지 않았다. 각 앱이 추가되면 아래 위치의 README에 실행 방법을 갱신한다.

- `apps/api/README.md`
- `apps/web/README.md`
- `crawler/README.md`
- `infra/README.md`

## 환경 변수

`.env.example`을 기준으로 로컬 `.env` 파일을 만든다. 실제 secret은 Git에 커밋하지 않는다.

## 수집 원칙

크롤링은 명시적으로 허용된 소스만 대상으로 한다.

- 공식 API/RSS/직접 등록/허용된 공개 페이지 우선
- 사용자 검색 시점 외부 크롤링 금지
- 로그인, CAPTCHA, 봇 차단, 비공개 API 우회 금지
- 공고 본문 전문, 이미지, 첨부파일 저장 금지

세부 정책은 `docs/crawling-policy.md`를 따른다.

## 주요 문서

- `CONTEXT_BRIEF.md`: 다음 세션을 위한 짧은 프로젝트 요약
- `PROJECT_STATUS.md`: 최신 진행 상황과 다음 작업
- `SESSION_HANDOFF.md`: 중단 후 재개 기준
- `docs/mvp-implementation-strategy.md`: MVP 구현 전략
- `docs/crawling-policy.md`: 안전 수집 정책
- `FREE_DEPLOYMENT_PLAN.md`: 무료 운영 배포 전략
- `ROADMAP.md`: 6주 MVP 로드맵
