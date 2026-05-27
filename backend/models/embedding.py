from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float
from backend.models.document import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)
    dimension = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
