# Deployment Runbook

This runbook connects the Cloudflare Pages frontend to a deployed FastAPI API, a Supabase PostgreSQL database, and a GitHub Actions scheduled collector.

## Target Architecture

```text
Cloudflare Pages
  -> FastAPI on Render
      -> Supabase PostgreSQL
GitHub Actions schedule
  -> crawler CLI
      -> Supabase PostgreSQL
```

User searches only query the internal API and database. External job sources are collected on schedule.

## 1. Create Supabase Database

1. Create a Supabase project.
2. Copy the Postgres connection string.
3. Use the pooled or direct connection string that works from GitHub Actions and Render.
4. Store it in GitHub repository secret `DATABASE_URL`.

Use this format if needed:

```text
postgresql://<user>:<password>@<host>:5432/<database>
```

If Supabase requires TLS, append:

```text
?sslmode=require
```

The app also accepts:

```text
postgresql+psycopg://<user>:<password>@<host>:5432/<database>
```

## 2. Bootstrap Database

In GitHub:

```text
Actions -> Bootstrap database -> Run workflow
```

Keep `seed_sample=true` for the first run. This applies migrations and inserts synthetic sample jobs so the deployed API can be verified before live sources are configured.

## 3. Deploy API To Render

Use the root `render.yaml` blueprint.

Required Render environment variables:

```text
APP_ENV=production
JOB_DATA_SOURCE=database
ALLOWED_ORIGINS=https://apply-finder.pages.dev
DATABASE_URL=<Supabase connection string>
```

Render start command from `render.yaml`:

```text
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, verify:

```text
https://<render-service>.onrender.com/health
https://<render-service>.onrender.com/jobs
```

## 4. Connect Cloudflare Pages

Set Cloudflare Pages environment variable:

```text
VITE_API_BASE_URL=https://<render-service>.onrender.com
```

Redeploy Cloudflare Pages. The frontend will then use the deployed API instead of static fallback data.

## 5. Configure Scheduled Collection

Add GitHub repository secret `CRAWLER_SOURCES_JSON`.

Greenhouse source example:

```json
{
  "sources": [
    {
      "type": "greenhouse",
      "name": "Company Name",
      "status": "allowed",
      "board_token": "company-board-token",
      "keywords": ["intern", "entry_level"],
      "eligibility_tags": ["student"]
    }
  ]
}
```

Lever source example:

```json
{
  "sources": [
    {
      "type": "lever",
      "name": "Company Name",
      "status": "allowed",
      "company": "company-slug",
      "keywords": ["intern", "entry_level"],
      "eligibility_tags": ["student"]
    }
  ]
}
```

Only sources with `status` set to `allowed` or `conditional` are collected. Keep sources as `paused` until the source policy review is complete.

Set repository variable or secret:

```text
CRAWLER_USER_AGENT=job-crawler/0.1 contact:<contact-email>
```

The scheduled workflow runs every 15 minutes:

```text
Actions -> Collect jobs
```

Manual run is also available from the same workflow.

## Verification

1. `Bootstrap database` succeeds.
2. Render `/health` returns `status: ok`.
3. Render `/jobs` returns database-backed items.
4. Cloudflare Pages displays items from the API.
5. `Collect jobs` logs `Upserted N jobs`.
6. A searched job appears through `/jobs?keyword=<term>`.
