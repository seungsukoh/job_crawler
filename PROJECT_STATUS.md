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

## 현재 리스크

- 아직 실제 앱 코드가 없다.
- 실제 수집 가능한 공공 API/RSS 소스가 확정되지 않았다.
- 무료 API 호스팅은 sleep으로 첫 응답이 느릴 수 있다.
- Supabase/Render/GitHub Actions 무료 한도 내에서 크롤러 실행 시간을 관리해야 한다.
- 민간 대형 채용 플랫폼은 무단 크롤링하지 않는 전제로 대체 소스 확보가 필요하다.

## 다음 작업

1. 레포 기본 구조 생성
2. FastAPI 백엔드 기본 앱 추가
3. Next.js 프론트엔드 기본 앱 추가
4. 로컬 개발용 PostgreSQL Docker Compose 추가
5. 샘플 공고 seed 데이터 추가
6. 공고 목록/상세 API 구현
7. 공고 목록/상세 UI 구현
8. 안전한 첫 수집 소스 후보 조사 및 Source Registry 초안 작성

## 진행 기록 규칙

새 기능, 정책 변경, 배포 변경, 크롤링 소스 추가, 리스크 발견, 테스트 결과는 이 파일에 날짜별로 기록한다.

