from pathlib import Path

import pytest

from app.database import configure_database
from app.models import UserCreate
from app.user_service import create_user, find_user_by_email


@pytest.fixture(autouse=True)
def database(tmp_path: Path) -> None:
    configure_database(str(tmp_path / "test-users.db"))


def test_create_user() -> None:
    user = create_user(UserCreate(name="Ada Lovelace", email="ada@example.com"))

    assert user.id == 1
    assert user.name == "Ada Lovelace"
    assert user.email == "ada@example.com"


def test_find_user_by_email() -> None:
    create_user(UserCreate(name="Grace Hopper", email="grace@example.com"))

    user = find_user_by_email("grace@example.com")

    assert user is not None
    assert user.name == "Grace Hopper"


def test_find_unknown_user_returns_none() -> None:
    assert find_user_by_email("missing@example.com") is None
