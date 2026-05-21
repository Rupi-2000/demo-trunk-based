from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool

