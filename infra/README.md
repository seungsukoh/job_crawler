# Infra

로컬 개발과 무료 배포를 돕는 설정 파일이 들어갈 위치다.

## 로컬 PostgreSQL

로컬 개발용 PostgreSQL은 `infra/docker-compose.yml`로 실행한다.

루트에서 `.env`를 아직 만들지 않았다면 예시 파일을 복사한다.

```powershell
Copy-Item .env.example .env
```

DB를 실행한다.

```powershell
docker compose --env-file .env -f infra/docker-compose.yml up -d
```

상태를 확인한다.

```powershell
docker compose --env-file .env -f infra/docker-compose.yml ps
```

로그를 확인한다.

```powershell
docker compose --env-file .env -f infra/docker-compose.yml logs -f postgres
```

DB를 중지한다.

```powershell
docker compose --env-file .env -f infra/docker-compose.yml down
```

로컬 DB 데이터를 모두 초기화하려면 volume까지 삭제한다.

```powershell
docker compose --env-file .env -f infra/docker-compose.yml down -v
```

기본 접속 값은 `.env.example`과 같다.

- Host: `localhost`
- Port: `5432`
- Database: `job_crawler`
- User: `job_crawler`
- Password: `job_crawler`
- API connection string: `DATABASE_URL`

이 설정은 로컬 개발 전용이다. 실제 운영 secret은 Git에 커밋하지 않는다.

## 예정 파일

- Cloudflare Pages 설정 참고 문서
- Render 배포 설정 참고 문서
- GitHub Actions 크롤러 실행 설정

## 원칙

- 무료 운영으로 시작한다.
- 유료 전환이 필요해도 앱 구조를 바꾸지 않도록 환경 변수와 표준 PostgreSQL을 우선한다.
- Secret은 코드와 문서에 실제 값으로 기록하지 않는다.
