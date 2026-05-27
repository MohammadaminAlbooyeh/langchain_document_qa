from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from backend.models.document import Base


class QAPair(Base):
    __tablename__ = "qa_pairs"

    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence = Column(Integer, default=0)
    sources = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
