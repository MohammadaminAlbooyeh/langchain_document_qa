from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from backend.utils.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


async def init_db():
    """Initialize database with all models"""
    from backend.models.document import Base
    # Import all models to register them
    from backend.models.api_key import APIKey
    from backend.models.audit_log import AuditLog
    from backend.models.conversation import Conversation
    from backend.models.qa_pair import QAPair
    from backend.models.embedding import Embedding

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
