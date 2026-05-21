from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from app.models.chat_message import Sender


class MessageCreate(BaseModel):
    sender: Sender = Field(..., examples=["USER"])
    content: str = Field(..., min_length=1, examples=["What is my credit card limit?"])
    retrieved_context: Optional[Dict[str, Any]] = Field(default=None, description="Optional RAG retrieval metadata/chunks used to generate the answer")


class MessageResponse(BaseModel):
    id: str
    session_id: str
    sender: Sender
    content: str
    retrieved_context: Optional[Dict[str, Any]]
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedMessagesResponse(BaseModel):
    items: list[MessageResponse]
    total: int
    limit: int
    offset: int
