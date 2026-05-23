from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


TaskPriority = Literal["low", "normal", "high"]
TaskStatus = Literal["open", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""
    priority: TaskPriority = "low"
    due_date: date | None = None
    status: TaskStatus = "open"


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: TaskPriority
    due_date: date | None
    status: TaskStatus
    assigned_to: str | None
    done: bool


class TaskAssignment(BaseModel):
    email: str = Field(..., min_length=3)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)


class User(BaseModel):
    id: int
    name: str
    email: str
