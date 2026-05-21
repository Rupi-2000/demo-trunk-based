from pathlib import Path

import pytest

from app.database import configure_database
from app.models import TaskCreate
from app.task_service import complete_task, create_task, list_tasks


@pytest.fixture(autouse=True)
def database(tmp_path: Path) -> None:
    configure_database(str(tmp_path / "test.db"))


def test_create_task() -> None:
    task = create_task(TaskCreate(title="Write demo", description="Prepare repository"))

    assert task.id == 1
    assert task.title == "Write demo"
    assert task.description == "Prepare repository"
    assert task.done is False


def test_complete_task() -> None:
    task = create_task(TaskCreate(title="Finish task"))

    completed = complete_task(task.id)

    assert completed is not None
    assert completed.done is True


def test_list_open_tasks_excludes_completed_tasks() -> None:
    first = create_task(TaskCreate(title="Open task"))
    second = create_task(TaskCreate(title="Completed task"))
    complete_task(second.id)

    open_tasks = list_tasks(open_only=True)

    assert [task.id for task in open_tasks] == [first.id]

