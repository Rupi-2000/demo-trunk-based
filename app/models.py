from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


TaskPriority = Literal["low", "normal", "high"]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""
    priority: TaskPriority = "normal"
    due_date: date | None = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: TaskPriority
    due_date: date | None
    done: bool
