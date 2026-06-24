# Crawler

예약 또는 관리자 수동 실행으로 채용 공고를 수집하는 독립 CLI가 들어갈 위치다.

## 역할

- Source Registry에서 허용된 소스만 수집
- 공식 API/RSS 우선 처리
- 수집 데이터 정규화
- 중복 제거 키 생성
- 수집 실행 결과 기록

## 원칙

- 사용자 검색 시점에는 실행하지 않는다.
- `allowed`, `conditional` 소스만 수집한다.
- `paused`, `blocked` 소스는 실행하지 않는다.
- 로그인, CAPTCHA, 봇 차단, 비공개 API 우회는 하지 않는다.
- 공고 본문 전문, 이미지, 첨부파일은 저장하지 않는다.

## 실행 방식

초기에는 GitHub Actions `workflow_dispatch` 수동 실행을 목표로 한다. 안정화 후 하루 1~2회 예약 실행으로 확장한다.

## 다음 작업

Source Registry 모델과 첫 안전 수집 소스가 확정된 뒤 Python CLI를 추가한다.
