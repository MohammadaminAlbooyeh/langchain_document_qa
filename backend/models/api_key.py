from datetime import datetime, UTC
from sqlalchemy import Column, String, DateTime, Boolean
from backend.models.document import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    key = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    last_used = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
