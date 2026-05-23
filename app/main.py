from contextlib import asynccontextmanager

import sqlite3

from fastapi import FastAPI, HTTPException

from app.database import init_db
from app.models import Task, TaskAssignment, TaskCreate, TaskStatusUpdate, User, UserCreate
from app.task_service import (
    assign_task,
    complete_task,
    create_task,
    list_tasks,
    update_task_status,
)
from app.user_service import create_user, find_user_by_email
from app.version import APP_VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Task Manager Demo App", lifespan=lifespan)


@app.get("/version")
def get_version() -> dict[str, str]:
    return {"version": APP_VERSION}


@app.post("/tasks", response_model=Task, status_code=201)
def post_task(task: TaskCreate) -> Task:
    return create_task(task)


@app.get("/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    return list_tasks()


@app.get("/tasks/open", response_model=list[Task])
def get_open_tasks() -> list[Task]:
    return list_tasks(open_only=True)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def patch_task_complete(task_id: int) -> Task:
    task = complete_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/status", response_model=Task)
def patch_task_status(task_id: int, update: TaskStatusUpdate) -> Task:
    task = update_task_status(task_id, update.status)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/assign", response_model=Task)
def patch_task_assignment(task_id: int, assignment: TaskAssignment) -> Task:
    user = find_user_by_email(assignment.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    task = assign_task(task_id, assignment.email)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/users", response_model=User, status_code=201)
def post_user(user: UserCreate) -> User:
    try:
        return create_user(user)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="User already exists") from exc


@app.get("/users/{email}", response_model=User)
def get_user(email: str) -> User:
    user = find_user_by_email(email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
