from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database import init_db
from app.models import Task, TaskCreate
from app.task_service import complete_task, create_task, list_tasks
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
