from app.version import APP_VERSION


def test_version_is_initial_release() -> None:
    assert APP_VERSION == "1.0.0"

