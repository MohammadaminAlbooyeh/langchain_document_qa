import sys
from loguru import logger
from backend.utils.config import get_settings

settings = get_settings()

logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
logger.add(
    "logs/langchain_qa.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
)


def get_logger():
    return logger
