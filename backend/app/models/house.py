from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.models import Base


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    currency = Column(String, default="EUR")
    city = Column(String, index=True)
    neighborhood = Column(String, nullable=True)
    area_m2 = Column(Float, nullable=True)
    rooms = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    posted_date = Column(DateTime, server_default=func.now())
