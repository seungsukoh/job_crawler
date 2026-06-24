# 대학생 취업 공고 통합 앱 기획 및 구현 계획

## 1. 현재 상태

- 작업 대상 저장소로 안내받은 `github.com/seungcukoh/job_crawler`는 현재 `Repository not found`로 클론되지 않았다.
- 따라서 이 문서는 기존 코드 분석이 아니라, 빈 저장소 또는 신규 프로젝트 기준의 제품 방향성, 타당성 검증, 구현 계획이다.
- 저장소 접근이 가능해지면 이 문서를 기준으로 실제 코드 구조와 구현 우선순위를 조정한다.

## 2. 제품 방향성

`job_crawler`의 초기 포지션은 "대학생을 위한 직무 키워드 기반 채용 공고 캘린더"가 적합하다.

핵심 사용자는 취업 준비 중인 대학생, 졸업 예정자, 인턴십을 찾는 저학년/고학년 학생이다. 이들은 공고가 부족해서가 아니라, 여러 채널에 흩어진 공고를 본인의 직무 관심사와 지원 가능 기간 기준으로 빠르게 좁히지 못해서 어려움을 겪는다.

초기 제품은 채용 플랫폼 전체를 대체하려고 하면 안 된다. 기존 플랫폼, 기업 채용 페이지, 공공 채용 정보, 학교 취업센터 정보를 사용자가 확인하기 쉽게 정리하고 원문으로 연결하는 보조 도구로 시작하는 편이 현실적이다.

## 3. 핵심 문제

1. 채용 공고가 플랫폼, 기업 홈페이지, 학교 취업센터, 공공기관 사이트에 흩어져 있다.
2. 대학생은 `데이터 분석`, `백엔드`, `마케팅`, `서비스 기획`, `금융`, `반도체` 같은 직무 키워드로 보고 싶지만 공고 제목과 분류 체계가 제각각이다.
3. 마감일, 신입/인턴 여부, 졸업예정자 가능 여부, 근무지역, 전환형 여부를 한눈에 비교하기 어렵다.
4. 매일 같은 검색을 반복해야 하고, 마감 임박 공고를 놓치기 쉽다.
5. 같은 공고가 여러 출처에 중복으로 올라와 탐색 피로가 커진다.

## 4. MVP 범위

MVP는 "특정 기간 동안 직무 키워드별 채용 공고를 한 곳에서 보고 저장한다"에 집중한다.

필수 기능:

- 직무 키워드 기반 공고 목록
- 기간 필터: 오늘 마감, 3일 내 마감, 이번 주 마감, 이번 달 등록, 직접 기간 선택
- 공고 카드: 회사명, 공고명, 직무, 고용형태, 신입/인턴 여부, 지역, 마감일, 출처, 원문 링크
- 관심 공고 저장
- 저장 공고의 마감 임박 표시
- 원문 링크 이동
- 중복 공고 병합
- 최신 확인 시각 표시

MVP에서 제외할 기능:

- 자기소개서 첨삭
- AI 면접
- 커뮤니티
- 합격 후기
- 복잡한 개인화 추천
- 민간 대형 채용 플랫폼의 무리한 본문 크롤링

## 5. 차별화 전략

- 직무 키워드 중심: 회사명이나 플랫폼 중심이 아니라 학생이 실제로 찾는 직무 기준으로 정리한다.
- 기간 중심: "이번 주에 지원해야 할 공고", "마감 3일 이내 공고"를 빠르게 확인하게 한다.
- 대학생 친화 필터: 신입, 인턴, 체험형 인턴, 채용연계형 인턴, 졸업예정자 가능, 전공무관 같은 태그를 전면에 둔다.
- 중복 제거: 같은 공고를 여러 번 보지 않게 대표 공고로 묶는다.
- 신뢰도 표시: 수집 시각이 아니라 원문 확인 시각을 보여준다. 예: `오늘 09:20 확인`.

## 6. 데이터 소싱 전략

데이터 수집 우선순위는 다음 순서가 안전하다.

1. 공식 API
2. RSS/Atom 피드
3. 제휴 또는 제공 피드
4. 약관과 robots.txt 확인 후 허용된 공개 페이지 크롤링
5. 직접 등록 또는 수동 큐레이션

초기 수집 대상:

- 공공 채용 API와 청년 인턴 정보
- 기업 채용 홈페이지 중 공개 접근이 가능한 신입/인턴 공고
- 대학 취업지원센터 또는 대학일자리플러스센터 공고
- RSS/피드를 제공하는 기관/기업 채용 공고
- 기업 또는 학교 담당자가 직접 등록한 공고

주의 대상:

- 사람인, 잡코리아, 원티드 등 대형 민간 플랫폼의 무단 크롤링은 MVP 핵심 전략에서 제외한다.
- 공식 API나 제휴 없이 본문 전체를 복제해 통합 검색 DB로 제공하는 방식은 약관, 데이터베이스권, 부정경쟁, 차단 리스크가 크다.
- 초기에는 메타데이터와 원문 링크 중심으로 제공하고, 원문 전체 복제는 피한다.

## 7. 최신성 및 품질 보장

필수 필드:

- `first_seen_at`: 처음 발견한 시각
- `last_seen_at`: 원천에서 마지막으로 확인한 시각
- `last_changed_at`: 원천 데이터 변경 감지 시각
- `fetched_at`: 시스템이 수집한 시각
- `deadline_at`: 마감 시각
- `status`: `active`, `closing_soon`, `expired`, `removed`, `unknown`

수집 주기:

- 공공 API/RSS: 1~3시간
- 기업 채용 페이지: 6~24시간
- 대학 게시판/기관 페이지: 6~12시간
- 마감 임박 공고: 별도 재검증

품질 규칙:

- 제목, 회사명, 원문 URL은 필수다.
- 마감일이 지난 공고는 기본 비노출한다.
- 마감일 파싱 실패 공고는 `unknown`으로 표시하거나 검수 큐로 보낸다.
- 원문이 404, 삭제, 마감 상태로 바뀌면 상태를 갱신한다.
- 대학생 대상과 무관한 고경력 공고는 필터링한다.

## 8. 중복 제거와 정규화

중복 제거는 MVP부터 포함해야 한다.

1차 강한 키:

- 원문 URL
- 접수 URL
- source별 공고 ID
- API 제공 공고 ID

2차 준강한 키:

- 정규화된 회사명
- 정규화된 공고 제목
- 마감일
- 근무지
- 고용형태
- 직무 카테고리

정규화 대상:

- 회사명: `삼성전자(주)`, `삼성전자`, `Samsung Electronics` 같은 표현을 대표명으로 매핑
- 고용형태: 신입, 인턴, 체험형 인턴, 채용연계형 인턴, 계약직, 정규직
- 경력요건: 신입, 경력무관, 졸업예정자 가능
- 지역: 시/도, 시/군/구, 원격, 하이브리드
- 직무: 개발, 데이터/AI, 기획/PM, 디자인, 마케팅, 영업, 금융, 연구/R&D, 생산/품질, 공공/행정, 기타

자동 병합이 애매한 공고는 검수 큐에 넣고, 마감일이나 접수 URL이 다르면 자동 병합하지 않는다.

## 9. 추천 아키텍처

초기에는 모듈형 모놀리포가 적합하다.

```text
job_crawler/
  apps/
    web/                 # Next.js 프론트엔드
    api/                 # FastAPI 백엔드
    worker/              # 크롤러/스케줄러
  packages/
    shared/              # 공통 타입, enum, 유틸
  infra/
    docker/
    nginx/
    scripts/
  docs/
```

권장 스택:

- 프론트엔드: Next.js, TypeScript, Tailwind CSS, TanStack Query
- 백엔드: FastAPI, Python, SQLAlchemy, Pydantic
- DB: PostgreSQL
- 검색: 초기 PostgreSQL Full Text Search, 이후 Meilisearch 또는 OpenSearch
- 크롤링: httpx, BeautifulSoup, 필요 시 Playwright
- 스케줄러: 초기 APScheduler, 확장 시 Celery + Redis
- 배포: Docker Compose 기반 단일 VPS 또는 Render/Fly.io/Railway + managed PostgreSQL

## 10. 핵심 데이터 모델

```text
Company
- id
- name
- normalized_name
- website_url
- logo_url
- industry
- created_at
- updated_at

JobSource
- id
- name
- source_type          # api, rss, crawl, manual, partner
- base_url
- allowed_status
- terms_checked_at
- robots_checked_at
- crawl_interval_minutes
- last_crawled_at
- failure_count
- is_active

JobPosting
- id
- company_id
- title
- normalized_title
- description_summary
- employment_type
- experience_level
- education_level
- location
- location_code
- remote_type
- deadline_at
- posted_at
- first_seen_at
- last_seen_at
- last_changed_at
- status
- hash_key
- created_at
- updated_at

JobPostingSource
- id
- job_posting_id
- source_id
- external_id
- original_url
- apply_url
- raw_payload
- fetched_at
- source_updated_at
- is_primary

JobCategory
- id
- name
- parent_id

JobPostingCategory
- job_posting_id
- category_id

JobTag
- id
- name

SavedJob
- user_id
- job_posting_id
- status              # saved, planned, applied, archived
- created_at

SearchAlert
- id
- user_id
- keyword
- locations
- categories
- employment_types
- notify_channel
- is_active
```

## 11. API 초안

```text
GET    /api/jobs
GET    /api/jobs/{id}
GET    /api/jobs/facets
GET    /api/companies/{id}
GET    /api/sources

POST   /api/auth/signup
POST   /api/auth/login
GET    /api/me

GET    /api/me/saved-jobs
POST   /api/me/saved-jobs/{job_id}
DELETE /api/me/saved-jobs/{job_id}
PATCH  /api/me/saved-jobs/{job_id}

GET    /api/me/search-alerts
POST   /api/me/search-alerts
PATCH  /api/me/search-alerts/{id}
DELETE /api/me/search-alerts/{id}

GET    /api/admin/crawl-runs
POST   /api/admin/crawl-runs
GET    /api/admin/crawl-errors
GET    /api/admin/dedupe-candidates
```

검색 쿼리 예시:

```text
/api/jobs?keyword=데이터분석&category=data&employment_type=intern&location=seoul&deadline=7d&sort=deadline&page=1
```

## 12. 프론트엔드 화면

MVP 화면:

1. 공고 탐색 화면
   - 검색창
   - 직무/지역/고용형태/마감 필터
   - 마감 임박순, 최신순, 관련도순 정렬
   - 공고 카드 리스트

2. 공고 상세 화면
   - 핵심 요약
   - 지원 조건
   - 직무/고용형태/지역/마감일
   - 출처와 최신 확인 시각
   - 원문 보기 버튼
   - 저장 버튼

3. 저장한 공고 화면
   - 저장 공고 목록
   - 마감 임박 표시
   - `검토 중`, `지원 예정`, `지원 완료` 상태 변경

4. 관심 키워드/알림 화면
   - 관심 직무 키워드
   - 지역
   - 고용형태
   - 알림 주기

5. 운영자 화면
   - 소스별 마지막 수집 시각
   - 신규 수집 수
   - 파싱 실패
   - 중복 후보
   - 마감일 누락

## 13. 타당성 검증

제품 타당성:

- 대학생의 채용 탐색 문제는 명확하다.
- 기존 대형 채용 플랫폼을 대체하기보다 직무/기간/마감 관리에 집중하면 차별화 여지가 있다.
- 반복 사용은 "새 공고 확인"과 "마감 임박 관리"에서 나온다.

기술 타당성:

- API, RSS, 허용된 공개 페이지 중심으로 시작하면 4~6주 MVP 구현이 가능하다.
- 크롤링보다 정규화, 중복 제거, 최신성 관리가 더 큰 난이도다.
- 검색은 PostgreSQL로 시작하고, 데이터가 늘면 Meilisearch나 OpenSearch로 확장하면 된다.

운영/법적 타당성:

- 무단 대량 크롤링을 핵심 전략으로 삼으면 리스크가 크다.
- 공공 API, 직접 등록, 제휴, 허용된 기업 페이지 중심으로 가면 운영 가능성이 높다.
- 출처 표기, 원문 링크, 삭제 요청 프로세스, robots/약관 검토 기록은 초기에 갖춰야 한다.

검증해야 할 핵심 가설:

1. 대학생은 회사명 중심보다 직무 키워드 중심 공고 목록에서 더 많이 저장한다.
2. 마감 임박 중심 홈 화면은 최신순 홈보다 재방문율을 높인다.
3. `신입 가능`, `전공 무관`, `채용연계형`, `졸업예정자 가능` 태그가 클릭률과 저장률을 높인다.
4. 공고 수가 적더라도 정확하고 중복이 적은 목록이 더 높은 신뢰를 만든다.
5. 마감 3일 전 알림이 원문 클릭과 지원 완료 전환에 효과적이다.

## 14. 4주 구현 로드맵

### 1주차: 기반 구축

- 모노리포 구조 생성
- Docker Compose 구성
- PostgreSQL 스키마 설계 및 마이그레이션
- FastAPI 프로젝트 초기화
- Next.js 프로젝트 초기화
- JobPosting, Company, JobSource 기본 모델 구현
- `GET /api/jobs`, `GET /api/jobs/{id}` 구현
- 샘플 seed 데이터 작성
- 기본 검색/필터 UI 구현

완료 기준:

- 로컬에서 web, api, db가 실행된다.
- 샘플 공고를 검색하고 상세 화면으로 이동할 수 있다.

### 2주차: 수집 파이프라인 MVP

- Source Registry 구현
- API/RSS fetcher 구현
- 크롤러 베이스 클래스 구현
- 1~2개 합법적/저위험 소스 연동
- raw payload 저장
- 정규화 로직 구현
- URL/공고 ID 기반 중복 제거
- crawl_runs, crawl_errors 테이블 구현
- 마감 공고 상태 갱신

완료 기준:

- 실제 또는 테스트 소스에서 공고가 수집되어 DB에 저장된다.
- 실패 로그와 신규 수집 수를 확인할 수 있다.

### 3주차: 사용자 기능과 검색 품질

- 회원가입/로그인
- 관심 공고 저장
- 저장 공고 상태 관리
- 직무/지역/고용형태/마감 필터 개선
- facets API 구현
- 마감 임박순, 최신순, 관련도순 정렬
- 모바일 UI 정리
- 원문 확인 시각 표시

완료 기준:

- 사용자가 검색, 필터, 저장, 원문 이동을 할 수 있다.
- 대학생 기준 핵심 필터가 실제 사용 가능한 수준이다.

### 4주차: 안정화와 배포

- 백엔드/API 테스트
- 크롤러 파서 fixture 테스트
- 중복 제거 테스트
- 프론트엔드 주요 흐름 테스트
- Docker 배포 구성
- 환경 변수 정리
- 기본 운영 문서 작성
- 삭제 요청/문의 채널 추가
- MVP 배포

완료 기준:

- 외부에서 접속 가능한 MVP가 있다.
- 크롤러가 주기 실행된다.
- 기본 테스트가 통과한다.
- 운영자가 수집 실패와 데이터 품질을 확인할 수 있다.

## 15. 테스트 전략

백엔드:

- 공고 검색 필터 조합
- 공고 상세 조회
- 저장 공고 CRUD
- 인증/권한
- 마감 공고 비노출

크롤러:

- HTML/API fixture 기반 파서 테스트
- URL canonicalization
- 중복 제거
- 마감일 파싱
- 실패/타임아웃 처리

프론트엔드:

- 검색 화면 렌더링
- 필터 변경 시 쿼리 갱신
- 상세 화면 이동
- 저장 버튼 동작
- 모바일 viewport 확인

E2E:

- 키워드 검색
- 필터 적용
- 공고 상세 진입
- 로그인
- 공고 저장
- 저장 목록 확인

## 16. 다음 실행 순서

1. GitHub 저장소 접근 문제를 해결한다.
2. 저장소가 비어 있다면 위 아키텍처로 초기 프로젝트를 생성한다.
3. 저장소에 기존 코드가 있다면 현재 구조를 먼저 읽고 이 계획을 맞춰 조정한다.
4. MVP 소스 1~2개를 법적 리스크가 낮은 API/RSS/공개 기업 페이지 중에서 선정한다.
5. 샘플 데이터 기반 화면을 먼저 만들고, 이후 수집 파이프라인을 붙인다.

