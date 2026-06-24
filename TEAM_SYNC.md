# Team Sync

병렬 작업을 하더라도 모든 작업자는 같은 프로젝트 기준을 공유해야 한다. 새 작업을 시작하거나 넘겨받을 때 이 문서를 먼저 확인한다.

## 시작 전에 읽을 파일

필수:

- `CONTEXT_BRIEF.md`: 짧은 프로젝트 요약과 현재 결정
- `PROJECT_STATUS.md`: 최신 진행 상황과 다음 작업
- `SESSION_HANDOFF.md`: 중단 지점과 다음 작업 범위
- `docs/requirements.md`: 요구사항 기준
- `docs/verification-criteria.md`: 요구사항 기반 검증 기준
- `docs/development-lanes.md`: 병렬 작업 경계
- `docs/engineering-principles.md`: 유지보수 가능한 개발 원칙

작업 성격별 추가 파일:

- 제품/우선순위: `docs/pm-operating-checklist.md`, `ROADMAP.md`
- 크롤링/데이터 수집: `docs/crawling-policy.md`
- 배포/운영: `FREE_DEPLOYMENT_PLAN.md`
- 전체 배경: `PROJECT_PLAN.md`

## 종료 전에 갱신할 파일

의미 있는 변경이 있으면:

- `PROJECT_STATUS.md`

다음 작업이나 중단 지점이 바뀌면:

- `SESSION_HANDOFF.md`
- `CONTEXT_BRIEF.md`

요구사항이나 완료 기준이 바뀌면:

- `docs/requirements.md`
- `docs/verification-criteria.md`

구조나 병렬 작업 경계가 바뀌면:

- `docs/development-lanes.md`
- `docs/engineering-principles.md`

크롤링 정책이나 소스 판단이 바뀌면:

- `docs/crawling-policy.md`

## 동기화 규칙

- 작업 시작 시 `PROJECT_STATUS.md`의 다음 작업과 `SESSION_HANDOFF.md`의 다음 명령이 맞는지 확인한다.
- 기능 작업은 요구사항 ID와 검증 기준을 연결한다.
- 작업 완료 후 어떤 검증을 했는지 `PROJECT_STATUS.md`에 기록한다.
- 세션이 끊길 수 있거나 문제가 생기면 현재 상태를 문서에 남기고 커밋한 뒤 GitHub에 push한다.
- 병렬 작업자는 다른 레인의 파일을 수정하기 전에 공유 계약 문서를 먼저 갱신한다.

## 현재 기본 흐름

```text
요구사항 정리
  -> 검증 기준 수립
  -> 작업 레인 선택
  -> 작은 단위 구현
  -> 검증
  -> PROJECT_STATUS / SESSION_HANDOFF 갱신
  -> commit / push
```
