from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.core.limiter import limiter
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting RAG Chat Storage Service", extra={"environment": settings.ENVIRONMENT})
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables checked/created")
    yield
    logger.info("Stopping RAG Chat Storage Service")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend microservice for securely storing RAG chatbot sessions, messages, and retrieved context.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning("Application error", extra={"path": request.url.path, "error": exc.message})
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning("Rate limit exceeded", extra={"path": request.url.path})
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Please try again later."})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router, prefix=settings.API_PREFIX)
