from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.api.routes import router
from backend.api.auth_routes import auth_router
from backend.middleware.error_handler import setup_error_handlers
from backend.middleware.request_id import RequestIDMiddleware
from backend.middleware.timing import TimingMiddleware
from backend.middleware.auth import AuthMiddleware
from backend.middleware.rate_limiter import RateLimiterMiddleware
from backend.models.database import init_db
from backend.utils.config import get_settings
from backend.utils.logger import get_logger

settings = get_settings()
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="LangChain Document QA API",
    description="REST API for document question-answering system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)

setup_error_handlers(app)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "langchain-document-qa"}
