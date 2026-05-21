from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.limiter import limiter
from app.core.security import verify_api_key
from app.schemas.message import MessageCreate, MessageResponse, PaginatedMessagesResponse
from app.schemas.session import SessionCreate, SessionFavoriteUpdate, SessionRename, SessionResponse
from app.services.chat_service import ChatService

router = APIRouter(dependencies=[Depends(verify_api_key)])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(db)


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_WRITE)
def create_session(request: Request, payload: SessionCreate, service: ChatService = Depends(get_chat_service)):
    return service.create_session(payload)


@router.get("", response_model=list[SessionResponse])
def list_sessions(
    user_id: str = Query(..., min_length=1),
    favorite_only: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ChatService = Depends(get_chat_service),
):
    return service.list_sessions(user_id=user_id, limit=limit, offset=offset, favorite_only=favorite_only)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, service: ChatService = Depends(get_chat_service)):
    return service.get_session(session_id)


@router.patch("/{session_id}/rename", response_model=SessionResponse)
@limiter.limit(settings.RATE_LIMIT_WRITE)
def rename_session(request: Request, session_id: str, payload: SessionRename, service: ChatService = Depends(get_chat_service)):
    return service.rename_session(session_id=session_id, title=payload.title)


@router.patch("/{session_id}/favorite", response_model=SessionResponse)
@limiter.limit(settings.RATE_LIMIT_WRITE)
def update_favorite(request: Request, session_id: str, payload: SessionFavoriteUpdate, service: ChatService = Depends(get_chat_service)):
    return service.update_favorite(session_id=session_id, is_favorite=payload.is_favorite)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.RATE_LIMIT_WRITE)
def delete_session(request: Request, session_id: str, service: ChatService = Depends(get_chat_service)):
    service.delete_session(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{session_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_WRITE)
def add_message(request: Request, session_id: str, payload: MessageCreate, service: ChatService = Depends(get_chat_service)):
    return service.add_message(session_id=session_id, payload=payload)


@router.get("/{session_id}/messages", response_model=PaginatedMessagesResponse)
def list_messages(
    session_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ChatService = Depends(get_chat_service),
):
    messages, total = service.list_messages(session_id=session_id, limit=limit, offset=offset)
    return PaginatedMessagesResponse(items=messages, total=total, limit=limit, offset=offset)
