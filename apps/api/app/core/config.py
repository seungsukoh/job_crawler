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


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "job-crawler-api"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        environment=os.getenv("APP_ENV", "local"),
        allowed_origins=_split_csv(os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")),
    )


settings = load_settings()
