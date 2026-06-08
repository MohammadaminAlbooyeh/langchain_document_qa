from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, UTC
from backend.models.api_key import APIKey
from backend.models.database import async_session


PUBLIC_PATHS = {
    "/health",
    "/api/v1/auth/login",
    "/api/v1/auth/verify",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/") and request.url.path not in PUBLIC_PATHS:
            api_key = request.headers.get("X-API-Key")

            if not api_key:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "API key required"},
                )

            # Verify API key from database
            is_valid = await self._verify_api_key(api_key)
            if not is_valid:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired API key"},
                )

            # Store user_id in request state for use in handlers
            async with async_session() as db:
                result = await db.execute(select(APIKey).where(APIKey.key == api_key))
                key_obj = result.scalar_one_or_none()
                if key_obj:
                    request.state.user_id = key_obj.user_id

        return await call_next(request)

    @staticmethod
    async def _verify_api_key(api_key: str) -> bool:
        """Verify API key exists, is active, and not expired"""
        try:
            async with async_session() as db:
                result = await db.execute(
                    select(APIKey).where(APIKey.key == api_key)
                )
                key_obj = result.scalar_one_or_none()

                if not key_obj or not key_obj.is_active:
                    return False

                if key_obj.expires_at and datetime.now(UTC) > key_obj.expires_at:
                    return False

                return True
        except Exception:
            return False
