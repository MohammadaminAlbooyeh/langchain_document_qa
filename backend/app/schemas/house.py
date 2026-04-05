from pydantic import BaseModel
from typing import Optional


class HouseBase(BaseModel):
    title: Optional[str]
    price: Optional[int]
    currency: Optional[str]
    city: Optional[str]
    neighborhood: Optional[str]
    area_m2: Optional[float]
    rooms: Optional[int]
    url: Optional[str]


class HouseCreate(HouseBase):
    pass


class HouseOut(HouseBase):
    id: int

    class Config:
        orm_mode = True
