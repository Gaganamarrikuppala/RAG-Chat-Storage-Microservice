from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.schemas.message import MessageCreate
from app.schemas.session import SessionCreate


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, payload: SessionCreate) -> ChatSession:
        session = ChatSession(user_id=payload.user_id, title=payload.title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def list_sessions(self, user_id: str, limit: int, offset: int, favorite_only: bool = False) -> list[ChatSession]:
        stmt = select(ChatSession).where(ChatSession.user_id == user_id)
        if favorite_only:
            stmt = stmt.where(ChatSession.is_favorite.is_(True))
        stmt = stmt.order_by(ChatSession.updated_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all())

    def get_session(self, session_id: str) -> ChatSession:
        session = self.db.get(ChatSession, session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        return session

    def rename_session(self, session_id: str, title: str) -> ChatSession:
        session = self.get_session(session_id)
        session.title = title
        self.db.commit()
        self.db.refresh(session)
        return session

    def update_favorite(self, session_id: str, is_favorite: bool) -> ChatSession:
        session = self.get_session(session_id)
        session.is_favorite = is_favorite
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete_session(self, session_id: str) -> None:
        session = self.get_session(session_id)
        self.db.delete(session)
        self.db.commit()

    def add_message(self, session_id: str, payload: MessageCreate) -> ChatMessage:
        self.get_session(session_id)
        message = ChatMessage(
            session_id=session_id,
            sender=payload.sender.value,
            content=payload.content,
            retrieved_context=payload.retrieved_context,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_messages(self, session_id: str, limit: int, offset: int) -> tuple[list[ChatMessage], int]:
        self.get_session(session_id)
        total_stmt = select(func.count()).select_from(ChatMessage).where(ChatMessage.session_id == session_id)
        total = self.db.scalar(total_stmt) or 0
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        messages = list(self.db.scalars(stmt).all())
        return messages, total
