from __future__ import annotations

from importlib import resources

from app.db.connection import connect


MIGRATIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


def apply_migrations() -> list[str]:
    applied_now: list[str] = []

    with connect() as connection:
        connection.execute(MIGRATIONS_TABLE_SQL)
        applied_rows = connection.execute("SELECT version FROM schema_migrations").fetchall()
        applied_versions = {row["version"] for row in applied_rows}

        for migration in _migration_files():
            version = migration.name.removesuffix(".sql")
            if version in applied_versions:
                continue

            connection.execute(migration.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (%(version)s)",
                {"version": version},
            )
            applied_now.append(version)

        connection.commit()

    return applied_now


def _migration_files():
    migrations = resources.files("app.db.migrations")
    return sorted(
        (path for path in migrations.iterdir() if path.name.endswith(".sql")),
        key=lambda path: path.name,
    )


def main() -> None:
    applied = apply_migrations()
    if applied:
        print("Applied migrations: " + ", ".join(applied))
    else:
        print("No pending migrations")


if __name__ == "__main__":
    main()
