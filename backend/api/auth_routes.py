from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import secrets
import hashlib
from datetime import datetime, UTC, timedelta
from backend.api.dependencies import get_db_session
from backend.models.api_key import APIKey
from backend.utils.config import get_settings
from backend.utils.sanitizer import InputSanitizer
from backend.utils.logger import get_logger

auth_router = APIRouter()
logger = get_logger()
settings = get_settings()


def generate_api_key() -> str:
    prefix = settings.api_key_prefix
    return f"{prefix}{secrets.token_hex(32)}"


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    expires_at: str | None = None


class APIKeyResponse(BaseModel):
    api_key: str
    message: str


class APIKeyListResponse(BaseModel):
    key: str
    name: str | None
    created_at: str
    is_active: bool


@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    """Login with email/password and get API key"""
    # Validate inputs
    email = InputSanitizer.sanitize_email(request.email)
    if not email or not request.password:
        logger.warning(f"Login attempt with invalid credentials")
        raise HTTPException(status_code=400, detail="Valid email and password required")

    # Hash email to generate consistent user_id
    user_id = hashlib.sha256(email.encode()).hexdigest()[:16]

    # Generate and store API key
    api_key = generate_api_key()
    expires_at = datetime.now(UTC) + timedelta(days=90)

    db_key = APIKey(
        key=api_key,
        user_id=user_id,
        name=f"Login at {datetime.now(UTC).isoformat()}",
        expires_at=expires_at,
        is_active=True,
    )
    db.add(db_key)
    await db.commit()

    logger.info(f"API key generated for user {user_id}")

    return LoginResponse(
        token=api_key, user_id=user_id, expires_at=expires_at.isoformat()
    )


@auth_router.post("/verify")
async def verify_key(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db_session)):
    """Verify API key and return user_id"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    # Query database for valid key
    result = await db.execute(select(APIKey).where(APIKey.key == x_api_key))
    api_key = result.scalar_one_or_none()

    if not api_key or not api_key.is_active:
        logger.warning(f"Invalid API key verification attempt: {x_api_key[:10]}...")
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Check expiration
    if api_key.expires_at and datetime.now(UTC) > api_key.expires_at:
        logger.warning(f"Expired API key: {api_key.key[:10]}...")
        raise HTTPException(status_code=401, detail="API key expired")

    # Update last used timestamp
    api_key.last_used = datetime.now(UTC)
    await db.commit()

    return {
        "valid": True,
        "user_id": api_key.user_id,
        "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
    }


@auth_router.get("/keys")
async def list_keys(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db_session)):
    """List all API keys for the authenticated user"""
    # Verify caller
    result = await db.execute(select(APIKey).where(APIKey.key == x_api_key))
    caller_key = result.scalar_one_or_none()

    if not caller_key or not caller_key.is_active:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Get all keys for this user
    result = await db.execute(select(APIKey).where(APIKey.user_id == caller_key.user_id))
    keys = result.scalars().all()

    return {
        "keys": [
            APIKeyListResponse(
                key=k.key[:20] + "...",  # Hide full key
                name=k.name,
                created_at=k.created_at.isoformat(),
                is_active=k.is_active,
            )
            for k in keys
        ]
    }


@auth_router.post("/revoke")
async def revoke_key(
    x_api_key: str = Header(...), db: AsyncSession = Depends(get_db_session)
):
    """Revoke the current API key"""
    result = await db.execute(select(APIKey).where(APIKey.key == x_api_key))
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    api_key.is_active = False
    await db.commit()

    logger.info(f"API key revoked: {api_key.key[:10]}...")
    return {"message": "API key revoked successfully"}
