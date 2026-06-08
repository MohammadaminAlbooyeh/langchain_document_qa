from datetime import datetime, UTC
from sqlalchemy import Column, String, DateTime, Text
from backend.models.document import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    action = Column(String(255), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC), index=True)
