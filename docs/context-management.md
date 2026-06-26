# 토큰 절약 작업 방식

## 목적

대화 토큰 한도에 걸리지 않도록 프로젝트의 장기 맥락은 저장소 문서에 보관하고, 대화에는 현재 작업에 필요한 최소 정보만 유지한다.

## 기본 원칙

- 대화는 작업 지시와 결과 확인에 집중한다.
- 긴 계획, 정책, 진행 상황은 파일로 남긴다.
- 새 작업을 시작할 때 모든 문서를 읽지 않는다.
- `CONTEXT_BRIEF.md`와 `PROJECT_STATUS.md`를 먼저 읽고, 필요한 문서만 추가로 연다.
- 전문가 그룹이나 장문 분석은 꼭 필요한 경우에만 사용한다.

## 새 작업 시작 절차

1. `CONTEXT_BRIEF.md` 확인
2. `PROJECT_STATUS.md` 확인
3. `SESSION_HANDOFF.md` 확인
4. 현재 작업과 관련된 문서만 추가 확인
   - 제품/우선순위: `ROADMAP.md`
   - 크롤링/데이터 수집: `docs/crawling-policy.md`
   - 배포/무료 운영: `FREE_DEPLOYMENT_PLAN.md`
   - 전체 배경: `PROJECT_PLAN.md`
5. 작업 범위를 작게 정하고 구현
6. 테스트 또는 검증
7. `PROJECT_STATUS.md` 갱신
8. 필요하면 `CONTEXT_BRIEF.md`와 `SESSION_HANDOFF.md`의 다음 작업만 갱신

## 대화 운영 규칙

사용자는 가능한 한 다음 형태로 요청한다.

```text
이번 작업: FastAPI 기본 앱 생성
범위: health endpoint, pyproject, README 실행법
제외: DB 모델, 크롤러
```

요청이 짧아도 괜찮지만, 한 번에 너무 많은 기능을 묶지 않는다.

좋은 작업 단위:

- FastAPI 기본 앱 추가
- React Vite 기본 앱 추가
- 공고 목록 API 추가
- 공고 목록 UI 추가
- Source Registry 모델 추가
- GitHub Actions 수동 크롤러 추가

피해야 할 작업 단위:

- 전체 앱을 한 번에 완성
- 모든 크롤러를 한 번에 구현
- 배포, 인증, 크롤링, UI를 한 PR에 모두 포함

## 문서별 역할

`CONTEXT_BRIEF.md`

- 다음 세션을 위한 짧은 요약
- 100줄 이하 유지
- 오래된 세부 내용은 넣지 않음

`PROJECT_STATUS.md`

- 날짜별 진행 상황
- 현재 리스크
- 다음 작업
- 테스트 결과

`SESSION_HANDOFF.md`

- 토큰 리밋이나 세션 종료 후 이어갈 중단 지점
- 다음 세션에서 실행할 작업 명령
- 반드시 유지할 결정

`ROADMAP.md`

- 6주 계획
- 우선순위
- 완료 기준

`docs/crawling-policy.md`

- 안전 수집 원칙
- 허용/금지 패턴
- 삭제 요청 및 중단 기준

## 커밋 기준

- 문서 변경도 의미 있는 단위로 커밋한다.
- 기능 구현 후에는 관련 문서와 상태 파일을 함께 갱신한다.
- 커밋 메시지는 짧고 명확하게 쓴다.

예:

```text
Add FastAPI health endpoint
Add scheduled crawling policy
Update project status
```

## 컨텍스트가 커졌을 때의 복구 방법

대화가 길어졌거나 토큰 한도에 가까워지면 다음 순서로 복구한다.

1. `PROJECT_STATUS.md`에 현재 작업 상태를 저장한다.
2. `CONTEXT_BRIEF.md`의 다음 작업과 결정 사항을 갱신한다.
3. `SESSION_HANDOFF.md`의 현재 중단 지점과 다음 명령을 갱신한다.
4. 변경사항을 커밋하고 GitHub에 push한다.
5. 대화를 새로 시작하더라도 `CONTEXT_BRIEF.md`, `PROJECT_STATUS.md`, `SESSION_HANDOFF.md`만 읽고 이어간다.
