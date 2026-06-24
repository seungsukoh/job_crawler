# Infra

로컬 개발과 무료 배포를 돕는 설정 파일이 들어갈 위치다.

## 예정 파일

- `docker-compose.yml`: 로컬 PostgreSQL
- Cloudflare Pages 설정 참고 문서
- Render 배포 설정 참고 문서
- GitHub Actions 크롤러 실행 설정

## 원칙

- 무료 운영으로 시작한다.
- 유료 전환이 필요해도 앱 구조를 바꾸지 않도록 환경 변수와 표준 PostgreSQL을 우선한다.
- Secret은 코드와 문서에 실제 값으로 기록하지 않는다.
