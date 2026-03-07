from pydantic import BaseModel, Field
from typing import Optional, Literal


class BugCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Literal["low", "medium", "high", "critical"]


class BugUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[Literal["low", "medium", "high", "critical"]] = None
    status: Optional[Literal["open", "in_progress", "resolved", "closed"]] = None


class BugResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"