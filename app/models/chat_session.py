from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self) -> str:
        return f"<ChatSession id={self.id} user_id={self.user_id} title={self.title}>"
