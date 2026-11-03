"""Pydantic models for the note-taking application."""

from enum import Enum
from pydantic import BaseModel, Field

class Category(str,Enum):
    """Valid categories available for a note."""
    PERSONAL = "personal"
    WORK = "work"
    LEARNING = "learning"
    IDEA = "idea"


class Note(BaseModel):
    """Represent one validated note."""
    id: int = Field(gt=0)
    title: str = Field(min_length=1,max_length=100)
    body: str = Field(min_length=1,max_length=10000)
    category: Category
    is_pinned: bool = False
    created_date: str
    word_count: int = Field(gt=0)
    