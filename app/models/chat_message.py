from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Sender(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_context: Mapped[dict | None] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self) -> str:
        return f"<ChatMessage id={self.id} session_id={self.session_id} sender={self.sender}>"
