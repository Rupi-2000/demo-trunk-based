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
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )

