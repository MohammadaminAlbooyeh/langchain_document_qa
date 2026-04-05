from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.house import House
from app.schemas.house import HouseOut

router = APIRouter()


@router.get("/", response_model=List[HouseOut])
def list_houses(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(House).offset(skip).limit(limit).all()


@router.get("/{house_id}", response_model=HouseOut)
def get_house(house_id: int, db: Session = Depends(get_db)):
    obj = db.query(House).filter(House.id == house_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="House not found")
    return obj
