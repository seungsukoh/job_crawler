from dataclasses import dataclass
import os


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    environment: str
    allowed_origins: tuple[str, ...]
    database_url: str
    job_data_source: str


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "job-crawler-api"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        environment=os.getenv("APP_ENV", "local"),
        allowed_origins=_split_csv(os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://job_crawler:job_crawler@localhost:5432/job_crawler",
        ),
        job_data_source=os.getenv("JOB_DATA_SOURCE", "sample"),
    )


settings = load_settings()
