from pathlib import Path
from datetime import date

import pytest

from app.database import configure_database
from app.models import TaskCreate
from app.task_service import complete_task, create_task, list_tasks


@pytest.fixture(autouse=True)
def database(tmp_path: Path) -> None:
    configure_database(str(tmp_path / "test.db"))


def test_create_task() -> None:
    task = create_task(
        TaskCreate(
            title="Write demo",
            description="Prepare repository",
            priority="high",
            due_date="2026-06-15",
        )
    )

    assert task.id == 1
    assert task.title == "Write demo"
    assert task.description == "Prepare repository"
    assert task.priority == "high"
    assert task.due_date == date(2026, 6, 15)
    assert task.status == "open"
    assert task.done is False


def test_create_task_uses_normal_priority_by_default() -> None:
    task = create_task(TaskCreate(title="Default priority"))

    assert task.priority == "normal"


def test_create_task_due_date_is_optional() -> None:
    task = create_task(TaskCreate(title="No due date"))

    assert task.due_date is None


def test_complete_task() -> None:
    task = create_task(TaskCreate(title="Finish task"))

    completed = complete_task(task.id)

    assert completed is not None
    assert completed.done is True
    assert completed.status == "done"


def test_create_done_task_marks_task_as_done() -> None:
    task = create_task(TaskCreate(title="Done task", status="done"))

    assert task.status == "done"
    assert task.done is True


def test_list_open_tasks_excludes_completed_tasks() -> None:
    first = create_task(TaskCreate(title="Open task"))
    second = create_task(TaskCreate(title="Completed task"))
    complete_task(second.id)

    open_tasks = list_tasks(open_only=True)

    assert [task.id for task in open_tasks] == [first.id]
