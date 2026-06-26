from app.db.jobs import _escape_like_pattern


def test_escape_like_pattern_treats_wildcards_as_literals() -> None:
    assert _escape_like_pattern(r"50%_remote\python") == r"50\%\_remote\\python"
