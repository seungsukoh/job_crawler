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

## 현재 리스크

- 아직 실제 앱 코드가 없다.
- 실제 수집 가능한 공공 API/RSS 소스가 확정되지 않았다.
- 무료 API 호스팅은 sleep으로 첫 응답이 느릴 수 있다.
- Supabase/Render/GitHub Actions 무료 한도 내에서 크롤러 실행 시간을 관리해야 한다.
- 민간 대형 채용 플랫폼은 무단 크롤링하지 않는 전제로 대체 소스 확보가 필요하다.

## 다음 작업

1. 모노리포 기본 구조 생성
2. FastAPI 백엔드 기본 앱 추가
3. Next.js 프론트엔드 기본 앱 추가
4. 로컬 개발용 PostgreSQL Docker Compose 추가
5. 샘플 공고 seed 데이터 추가
6. 공고 목록/상세 API 구현
7. 공고 목록/상세 UI 구현
8. 안전한 첫 수집 소스 후보 조사 및 Source Registry 초안 작성

## 진행 기록 규칙

새 기능, 정책 변경, 배포 변경, 크롤링 소스 추가, 리스크 발견, 테스트 결과는 이 파일에 날짜별로 기록한다.

토큰 리밋, 오류, 세션 재시작 가능성이 있으면 `PROJECT_STATUS.md`와 `SESSION_HANDOFF.md`를 갱신하고 커밋한 뒤 GitHub에 push한다.
