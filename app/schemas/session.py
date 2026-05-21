from datetime import datetime
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100, examples=["user_123"])
    title: str = Field(..., min_length=1, max_length=255, examples=["Loan eligibility conversation"])


class SessionRename(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class SessionFavoriteUpdate(BaseModel):
    is_favorite: bool


class SessionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
