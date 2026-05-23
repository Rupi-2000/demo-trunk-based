import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.environ.get("TASK_MANAGER_DB_PATH", "app.db"))


def configure_database(path: str) -> None:
    global DB_PATH
    DB_PATH = Path(path)
    init_db()


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'normal',
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'open',
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )

        task_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(tasks)").fetchall()
        }

        if "priority" not in task_columns:
            connection.execute(
                "ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal'"
            )

        if "due_date" not in task_columns:
            connection.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

        if "status" not in task_columns:
            connection.execute(
                "ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'open'"
            )
