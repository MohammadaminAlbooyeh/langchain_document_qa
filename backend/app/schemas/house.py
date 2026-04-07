from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HouseBase(BaseModel):
    title: str
    description: Optional[str]
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    area_sqft: float
    property_type: str


class HouseCreate(HouseBase):
    pass


class HouseOut(HouseBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
