from pydantic import BaseModel, Field
from enum import Enum

class User(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    email:str
    age:int = Field(ge=0,le=120)
    is_active:bool = True

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
    assignee: User | None = None
    tags: list[str] = Field(default_factory = list,max_length = 10)
    notes: str | None = None