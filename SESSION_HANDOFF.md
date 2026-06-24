# Session Handoff

이 파일은 토큰 리밋, 세션 종료, 컨텍스트 초기화가 발생했을 때 다음 세션에서 바로 이어가기 위한 인수인계 문서다.

## 다음 세션 시작 절차

1. `CONTEXT_BRIEF.md`를 읽는다.
2. `PROJECT_STATUS.md`를 읽는다.
3. 이 파일의 `현재 중단 지점`과 `다음 명령`을 확인한다.
4. 작업과 직접 관련된 문서만 추가로 읽는다.
5. 작업을 이어간다.

## 현재 중단 지점

- 저장소 연결 완료
- 기획/로드맵/무료 배포/안전 수집 정책 문서화 완료
- 토큰 절약 작업 방식과 세션 인수인계 문서화 완료
- 전문가 그룹 검토를 통해 `apps/web`, `apps/api`, `crawler`, `infra`, `docs` 기반 모노리포 구조를 권장 구조로 확정
- `docs/mvp-implementation-strategy.md`에 MVP 구현 전략 기록 완료
- `apps/web`, `apps/api`, `crawler`, `infra` 기본 구조와 README 문서 생성 완료
- 루트 `README.md`, `.gitignore`, `.env.example` 생성 완료
- 아직 FastAPI/Next.js 실제 앱 코드는 생성하지 않음

## 다음 명령

다음 개발 작업은 아래 순서로 시작한다.

```text
이번 작업: FastAPI 백엔드 기본 앱 추가
범위: apps/api 안에 FastAPI 앱, /health 엔드포인트, Python 의존성 파일, 로컬 실행 문서
제외: DB 모델, 실제 크롤러, 배포 자동화, 인증
```

## 반드시 유지할 결정

- 사용자 검색 시점에 외부 사이트를 크롤링하지 않는다.
- 검색은 내부 DB 조회로 처리한다.
- 크롤링은 GitHub Actions 스케줄 또는 관리자 수동 실행으로만 수행한다.
- 수집 소스는 공식 API/RSS/직접 등록/허용된 공개 페이지부터 시작한다.
- 대형 민간 채용 플랫폼 무단 크롤링은 MVP 범위에서 제외한다.
- 진행 내용은 `PROJECT_STATUS.md`에 남긴다.
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
