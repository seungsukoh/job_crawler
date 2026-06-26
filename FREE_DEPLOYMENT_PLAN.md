# 무료 운영 배포 계획

## 목표

초기 MVP는 가능한 한 무료 티어로 운영한다. 비용이 발생하는 유일한 항목은 선택 사항인 커스텀 도메인이다. 도메인을 사지 않으면 Cloudflare Pages 기본 도메인으로도 시작할 수 있다.

## 추천 무료 구성

```text
사용자
  -> Cloudflare Pages
      -> React Vite 프론트엔드
  -> 무료 API 호스팅
      -> FastAPI 백엔드
      -> 크롤러 수동 실행 또는 예약 실행
  -> 무료 PostgreSQL
      -> Supabase 또는 Neon
```

## 서비스별 선택

### 프론트엔드

추천:

- Cloudflare Pages 무료 플랜
- GitHub 저장소와 연결해 `main` 브랜치 push 시 자동 배포

초기 URL:

- `https://job-crawler.pages.dev` 형태의 무료 URL

도메인을 나중에 사면:

- `https://job-crawler.com`
- `https://www.job-crawler.com`

### 백엔드 API

무료 후보:

1. Render Free Web Service
2. Railway 무료 크레딧
3. Fly.io 무료 또는 저가 사용량
4. PythonAnywhere 무료 플랜

초기 추천은 Render Free다. 단, 무료 서버는 일정 시간 사용이 없으면 sleep 상태가 될 수 있다. MVP 검증에는 충분하지만, 사용자가 늘면 작은 유료 서버로 옮기는 것이 낫다.

### 데이터베이스

무료 후보:

1. Supabase Free
2. Neon Free

초기 추천은 Supabase Free다. 관리 UI가 편하고 PostgreSQL을 그대로 쓸 수 있다.

주의:

- 무료 티어는 용량, 연결 수, 프로젝트 sleep 정책이 있을 수 있다.
- 크롤러가 DB 연결을 너무 자주 만들지 않도록 connection pool과 batch upsert를 사용한다.

### 크롤러/스케줄러

무료 운영에서는 크롤러를 무겁게 돌리지 않는다.

1단계:

- 관리자 또는 개발자가 수동 실행
- GitHub Actions `workflow_dispatch`로 수동 크롤링

2단계:

- GitHub Actions scheduled workflow로 하루 1~4회 실행
- 공공 API/RSS처럼 안정적인 소스만 대상으로 실행

3단계:

- 사용자가 늘면 worker를 API 서버와 분리
- 작은 VPS 또는 유료 worker로 이전

GitHub Actions 무료 사용 시 주의:

- 너무 잦은 크롤링은 피한다.
- 민간 플랫폼 대량 크롤링은 하지 않는다.
- 실행 시간 제한을 고려해 소스별로 나누어 실행한다.

## MVP 무료 배포 순서

1. GitHub 저장소에 모노리포 구조 생성
2. React Vite 앱 생성
3. Cloudflare Pages에 GitHub 저장소 연결
4. Supabase 프로젝트 생성
5. FastAPI 앱 생성
6. Render Free에 FastAPI 배포
7. 프론트엔드 환경 변수에 API URL 연결
8. 샘플 데이터로 공고 검색 화면 검증
9. GitHub Actions로 크롤러 수동 실행 추가
10. 공공 API/RSS 소스 1개부터 연결

## 초기 환경 변수

프론트엔드:

```text
VITE_API_BASE_URL=https://<api-host>
```

백엔드:

```text
DATABASE_URL=postgresql+psycopg://...
ALLOWED_ORIGINS=https://<cloudflare-pages-domain>
JWT_SECRET=<random-secret>
CRAWLER_USER_AGENT=job-crawler/0.1 contact:<email>
```

GitHub Actions:

```text
DATABASE_URL
CRAWLER_USER_AGENT
```

## 무료 운영의 한계

- API 서버가 sleep될 수 있어 첫 요청이 느릴 수 있다.
- DB 연결 수와 저장 용량이 제한된다.
- 크롤러를 자주 실행하기 어렵다.
- Playwright 기반 동적 크롤링은 무료 환경에서 불안정할 수 있다.
- 트래픽이 늘면 무료 티어 한도에 걸릴 수 있다.

## 무료 단계에서 피해야 할 것

- 대형 채용 플랫폼 대량 크롤링
- 10분 단위 빈번한 스케줄링
- Playwright 상시 실행
- 공고 본문 전문 저장
- 이미지, 첨부파일, 로고 복제 저장
- 검색 엔진을 별도로 운영하는 것

## 유료 전환 기준

아래 중 하나가 발생하면 월 3~7만원 수준의 유료 운영으로 전환을 검토한다.

- 일 방문자가 100명 이상으로 안정화
- API 첫 응답 지연이 사용자 경험을 해침
- 크롤러를 하루 6회 이상 안정적으로 돌려야 함
- DB 무료 용량 또는 연결 수가 부족함
- 관리자/사용자 알림 기능이 중요해짐
- 공고 소스가 10개 이상으로 늘어남

## 결론

무료로 시작하는 것은 가능하다. 단, 무료 단계의 목표는 완벽한 자동화가 아니라 제품 가설 검증이다. 초기에는 Cloudflare Pages, Render Free, Supabase Free, GitHub Actions 조합으로 시작하고, 공고 수집은 공공 API/RSS 중심으로 작게 운영한다.
