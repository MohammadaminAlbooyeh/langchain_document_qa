from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.api.routes import router
from backend.middleware.error_handler import setup_error_handlers
from backend.middleware.request_id import RequestIDMiddleware
from backend.middleware.timing import TimingMiddleware
from backend.models.database import init_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="LangChain Document QA API",
    description="REST API for document question-answering system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

setup_error_handlers(app)
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "langchain-document-qa"}
