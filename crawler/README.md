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

GitHub Actions `Collect jobs` workflow로 수동 실행과 15분 주기 예약 실행을 지원한다. 실제 수집 대상은 `CRAWLER_SOURCES_JSON` 또는 로컬 `crawler/sources.json`에 등록된 allowlist만 사용한다.

지원하는 초기 소스 타입:

- `greenhouse`: Greenhouse public job board API
- `lever`: Lever public postings API

로컬 dry-run 예시:

```powershell
python -m pip install -e apps/api -e crawler
python -m crawler.run --sources-file crawler/sources.example.json --dry-run
```

`sources.example.json`의 소스는 모두 `paused`라 수집되지 않는다. 실제 수집 전에는 정책 검토 후 `status`를 `allowed` 또는 `conditional`로 바꾼 별도 `crawler/sources.json` 파일이나 GitHub secret `CRAWLER_SOURCES_JSON`을 사용한다.

## 다음 작업

첫 실제 수집 소스 후보를 정책 검토한 뒤 `CRAWLER_SOURCES_JSON`에 등록하고 GitHub Actions에서 수동 실행으로 검증한다.
