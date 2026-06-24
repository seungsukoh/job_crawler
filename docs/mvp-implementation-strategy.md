# MVP 구현 전략

## 전문가 그룹 결론

이 프로젝트는 초기부터 완성형 채용 플랫폼을 목표로 하지 않는다. MVP의 최선 방향은 대학생이 신뢰할 수 있는 최신 채용 공고를 직무 키워드와 마감일 기준으로 빠르게 찾고 저장하는 도구다.

## 제품 범위

MVP P0 범위:

- 직무 키워드 검색
- 마감일/기간 필터
- 공고 목록
- 공고 상세
- 원문 링크 이동
- 관심 공고 저장
- 마감 임박 표시
- 수집 시각과 원문 확인 시각 표시

MVP에서 제외:

- 사용자 검색 시점 외부 크롤링
- 대형 민간 채용 플랫폼 무단 크롤링
- AI 추천, 자기소개서, 면접, 커뮤니티
- 로그인 기반 개인화
- 별도 검색 엔진 운영
- 공고 본문 전문, 이미지, 첨부파일 저장

## 권장 구조

무료 운영과 배포 분리를 고려해 모노리포 구조로 시작한다.

```text
apps/
  web/        Next.js + TypeScript, Cloudflare Pages 배포 후보
  api/        FastAPI, Render Free 배포 후보
crawler/      GitHub Actions에서 실행하는 독립 CLI
infra/        Docker Compose, 배포 참고 파일
docs/         정책, 전략, 운영 문서
```

이 구조는 Cloudflare Pages, Render, GitHub Actions를 각각 독립적으로 운영하기 쉽다.

## 기술 방향

- Frontend: Next.js + TypeScript
- Frontend 운영: Cloudflare Pages
- Frontend 방식: 정적 페이지와 클라이언트 API 호출 중심
- Backend: Python FastAPI
- Backend 운영: Render Free
- Database: PostgreSQL, Supabase Free 후보
- Search: 초기에는 PostgreSQL `ILIKE` 또는 full-text search만 사용
- Crawler: API 서버와 분리된 Python CLI
- Scheduler: GitHub Actions `workflow_dispatch`에서 시작, 안정화 후 하루 1~2회 scheduled 실행

## API 범위

초기 FastAPI는 얇은 조회 API로 시작한다.

- `GET /health`
- `GET /jobs`
- `GET /jobs/{id}`
- `GET /sources`
- `GET /crawl-runs`

DB 모델은 수집 감사가 가능해야 한다.

- `job_postings`
- `sources`
- `crawl_runs`
- `raw_items` 또는 `source_snapshots`

공고에는 최소한 아래 필드를 둔다.

- 제목
- 회사명
- 직무 키워드
- 지역
- 고용형태
- 마감일
- 원문 URL
- 출처명
- 수집 시각
- 원문 확인 시각
- 중복 제거 키

## 관심 공고 저장

초기에는 인증을 붙이지 않는다. 관심 공고 저장은 브라우저 `localStorage` 기반으로 먼저 검증한다.

반복 사용 신호가 확인되면 Supabase Auth 또는 별도 JWT 기반 계정 기능을 붙인다.

## 안전 수집 방식

수집은 Source Registry를 통과한 소스만 실행한다.

허용 우선순위:

1. 공식 API
2. 공식 RSS/Atom
3. 직접 등록
4. robots.txt와 약관 검토 후 허용된 공개 HTML

소스 상태:

- `allowed`
- `conditional`
- `paused`
- `blocked`

`paused`, `blocked` 소스는 코드상 수집이 실행되지 않아야 한다.

기본 수집 주기는 하루 1~2회로 시작한다. 무료 운영 한도, 소스 안정성, API quota가 확인된 뒤에만 하루 4회까지 늘린다.

## 유료 전환을 고려한 설계

무료 운영으로 시작하지만 특정 서비스에 강하게 묶이지 않도록 설계한다.

- `apps/web`, `apps/api`, `crawler`를 분리해 프론트엔드, API, 수집기를 독립적으로 이전할 수 있게 한다.
- 프론트엔드는 `NEXT_PUBLIC_API_BASE_URL` 환경 변수로 API 주소만 바꾸면 되게 한다.
- 백엔드는 FastAPI 표준 ASGI 앱으로 유지해 Render Free에서 유료 Render, Fly.io, Railway, VPS, 컨테이너 환경으로 옮길 수 있게 한다.
- DB는 Supabase 전용 기능보다 표준 PostgreSQL과 Alembic migration을 우선해 Neon, RDS, Cloud SQL 같은 다른 PostgreSQL로 이전 가능하게 한다.
- 크롤러는 API 서버 내부 작업이 아니라 독립 CLI로 유지해 GitHub Actions에서 시작하되, 나중에 별도 worker, VPS, managed job runner로 옮길 수 있게 한다.
- 검색은 초기에는 PostgreSQL 인덱스와 full-text search를 사용하고, 트래픽이나 검색 품질 요구가 커질 때만 별도 검색 엔진을 검토한다.
- 환경 변수와 secret은 코드에 넣지 않고 `.env.example`, 배포 플랫폼 secret, GitHub Actions secret으로 분리한다.
- 수집 결과에는 원문 URL, 출처, 수집 시각, 중복 제거 키를 저장해 DB 이전이나 재처리 시 추적 가능하게 한다.

유료 전환은 앱 구조를 바꾸는 일이 아니라 실행 위치와 운영 한도를 바꾸는 일이 되도록 만드는 것이 목표다.

## 구현 순서

1. 모노리포 기본 구조 생성
2. FastAPI `/health` 앱 추가
3. Next.js 기본 앱 추가
4. 로컬 PostgreSQL Docker Compose 추가
5. DB migration과 샘플 공고 seed 추가
6. 공고 목록/상세 API 구현
7. 공고 목록/상세/검색/필터 UI 구현
8. 관심 공고 localStorage 저장 구현
9. Source Registry 모델 추가
10. 안전한 첫 수집 소스 후보 조사
11. GitHub Actions 수동 크롤러 실행 추가

## 검증 기준

베타 사용자 10~20명을 기준으로 아래 지표를 본다.

- 검색/필터 사용률 60% 이상
- 상세 진입률 40% 이상
- 원문 링크 클릭률 30% 이상
- 관심 공고 저장률 25% 이상
- 7일 내 재방문율 20% 이상

데이터 품질 기준:

- 활성 공고 100~300개
- 중복률 5% 이하
- 원문 링크 유효율 95% 이상
- 대학생 무관 공고 10% 이하

## 최종 판단

가장 안전한 방법은 앱 탐색 경험을 샘플 데이터로 먼저 완성하고, Source Registry 기반의 저위험 수집 파이프라인을 나중에 붙이는 순서다. 실제 수집은 제품의 핵심이지만, 무리한 크롤링을 먼저 붙이면 법적/운영 리스크가 커지고 무료 운영도 불안정해진다.
