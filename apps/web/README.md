# Web App

React + Vite + TypeScript 프론트엔드다.

## 역할

- 공고 목록/상세 화면
- 직무 키워드 검색
- 마감일/기간 필터
- 관심 공고 저장
- 원문 링크 이동

## 운영 방향

- Cloudflare Pages 배포를 우선 고려한다.
- API 주소는 `VITE_API_BASE_URL` 환경 변수로 주입한다.
- MVP에서는 서버 기능 의존을 줄이고 클라이언트 API 호출 중심으로 시작한다.

## 다음 작업

다음 프론트엔드 작업은 실제 API/DB runtime 검증 후 Cloudflare Pages 환경 변수와 API CORS 설정을 맞추는 것이다.

## 구조

```text
src/
  App.tsx
  main.tsx
  components/
    api-health-panel.tsx
    job-explorer.tsx
  lib/
    config.ts
    jobs.ts
  styles/
    globals.css
```

## 환경 변수

API 주소는 `VITE_API_BASE_URL`로 설정한다.

기본값:

```text
http://localhost:8000
```

루트 `.env.example`에도 같은 변수가 있다.

## Cloudflare Pages

권장 Cloudflare Pages 설정:

```text
Framework preset: Vite
Build command: npm run build
Build output directory: dist
Environment variable: VITE_API_BASE_URL
Node version: 20
```

## 로컬 실행

PowerShell에서 `npm` 스크립트 실행이 막히면 `npm.cmd`를 사용한다.

```powershell
cd apps/web
npm.cmd install
npm.cmd run dev
```

확인:

```text
http://localhost:5173
```

타입 검사:

```powershell
cd apps/web
npm.cmd run typecheck
```

정적 빌드:

```powershell
cd apps/web
npm.cmd run build
```

## 검증 기준

- `SR-002`: API base URL은 `VITE_API_BASE_URL` 환경 변수로 설정된다.
- `NFR-002`: `apps/web`은 API와 독립적으로 실행/배포된다.
