from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


PUBLIC_PATHS = {"/health", "/api/v1/auth/login", "/api/v1/auth/verify", "/docs", "/openapi.json", "/redoc"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/") and request.url.path not in PUBLIC_PATHS:
            api_key = request.headers.get("X-API-Key")
            if not api_key:
                from backend.api.auth_routes import API_KEYS
                if not API_KEYS:
                    return await call_next(request)
                return JSONResponse(
                    status_code=401,
                    content={"detail": "API key required"},
                )
        return await call_next(request)
