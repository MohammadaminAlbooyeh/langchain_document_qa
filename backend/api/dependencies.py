from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.database import get_session


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


async def verify_api_key(x_api_key: str | None = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key required")
    return x_api_key


async def get_current_user(x_user_id: str | None = Header(None)):
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="User ID required")
    return x_user_id
