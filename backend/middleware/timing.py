import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from backend.utils.logger import get_logger

logger = get_logger()


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        response.headers["X-Response-Time"] = f"{elapsed:.3f}s"
        logger.info(f"{request.method} {request.url.path} - {elapsed:.3f}s")
        return response
