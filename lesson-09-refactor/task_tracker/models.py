"""Pydantic data models for tasks, priorities, and statuses."""

from enum import Enum
from pydantic import BaseModel,Field

class Priority(str,Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(str,Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1,max_length=200)
    priority: Priority
    status: Status = Status.TODO
    created_date: str
    tags: list[str] = Field(default_factory=list, max_length=10)