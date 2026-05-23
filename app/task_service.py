from app.database import get_connection
from app.models import Task, TaskCreate


def _row_to_task(row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        priority=row["priority"],
        due_date=row["due_date"],
        status=row["status"],
        done=bool(row["done"]),
    )


def create_task(task: TaskCreate) -> Task:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, priority, due_date, status, done)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task.title,
                task.description,
                task.priority,
                task.due_date.isoformat() if task.due_date else None,
                task.status,
                1 if task.status == "done" else 0,
            ),
        )
        row = connection.execute(
            """
            SELECT id, title, description, priority, due_date, status, done
            FROM tasks
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return _row_to_task(row)


def list_tasks(open_only: bool = False) -> list[Task]:
    query = "SELECT id, title, description, priority, due_date, status, done FROM tasks"
    params = ()

    if open_only:
        query += " WHERE done = ?"
        params = (0,)

    query += " ORDER BY id"

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [_row_to_task(row) for row in rows]


def complete_task(task_id: int) -> Task | None:
    with get_connection() as connection:
        connection.execute(
            "UPDATE tasks SET done = 1, status = 'done' WHERE id = ?",
            (task_id,),
        )
        row = connection.execute(
            """
            SELECT id, title, description, priority, due_date, status, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_task(row)


def update_task_status(task_id: int, status: str) -> Task | None:
    done = 1 if status == "done" else 0

    with get_connection() as connection:
        connection.execute(
            "UPDATE tasks SET status = ?, done = ? WHERE id = ?",
            (status, done, task_id),
        )
        row = connection.execute(
            """
            SELECT id, title, description, priority, due_date, status, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_task(row)
