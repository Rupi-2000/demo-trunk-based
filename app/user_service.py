from app.database import get_connection
from app.models import User, UserCreate


def _row_to_user(row) -> User:
    return User(id=row["id"], name=row["name"], email=row["email"])


def create_user(user: UserCreate) -> User:
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        row = connection.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return _row_to_user(row)


def find_user_by_email(email: str) -> User | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, name, email FROM users WHERE email = ?",
            (email,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_user(row)
