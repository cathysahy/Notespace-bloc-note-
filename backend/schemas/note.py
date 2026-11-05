from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str | None = None
    category: str = "Personnel"


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None
    category: str | None = None
    is_favorite: bool | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str | None
    category: str | None
    is_favorite: bool
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
