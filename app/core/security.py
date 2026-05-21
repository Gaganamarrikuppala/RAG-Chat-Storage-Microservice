from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> None:
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
