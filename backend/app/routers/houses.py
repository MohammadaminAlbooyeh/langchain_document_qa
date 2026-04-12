
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.config import settings
from app.core.deps import get_db
from app.models.house import House
from app.schemas.house import HouseOut
from app.services.external_listings import fetch_external_listings

router = APIRouter()

CITY_DISTRICTS = {
    "Milan": ["Navigli", "Brera", "Porta Romana", "Isola"],
    "Rome": ["Centro Storico", "Trastevere", "Prati", "Monti"],
    "Turin": ["Centro", "Crocetta", "San Salvario", "Lingotto"],
    "Florence": ["Duomo", "Santa Maria Novella", "Oltrarno", "San Lorenzo"],
    "Venice": ["San Marco", "Cannaregio", "Dorsoduro", "Castello"],
    "Bologna": ["Centro Storico", "Porto", "Santo Stefano", "Bolognina"],
}


@router.get("/", response_model=List[HouseOut])
def list_houses(
    skip: int = 0,
    limit: int = 50,
    source: Optional[str] = Query("auto"),
    city: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    rooms: Optional[int] = Query(None),
    district: Optional[str] = Query(None),
    mode: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    filters: Dict[str, Any] = {
        "city": city,
        "min_price": min_price,
        "max_price": max_price,
        "rooms": rooms,
        "district": district,
        "mode": mode,
        "skip": skip,
        "limit": limit,
    }

    normalized_source = (source or "auto").lower()
    if normalized_source == "external" or (
        normalized_source == "auto" and settings.LISTINGS_API_URL
    ):
        try:
            external_listings = fetch_external_listings(filters)
            if normalized_source == "external":
                return external_listings[:limit]
            if external_listings:
                return external_listings[:limit]
        except RuntimeError as exc:
            if normalized_source == "external":
                raise HTTPException(status_code=502, detail=str(exc)) from exc

    q = db.query(House)
    if city:
        q = q.filter(House.location.ilike(f"%{city}%"))
    if min_price is not None:
        q = q.filter(House.price >= min_price)
    if max_price is not None:
        q = q.filter(House.price <= max_price)
    # Treat `rooms` as a minimum number of bedrooms (e.g., rooms=1 => bedrooms >= 1)
    if rooms is not None:
        try:
            min_rooms = int(rooms)
            q = q.filter(House.bedrooms >= min_rooms)
        except (ValueError, TypeError):
            pass
    if district:
        q = q.filter(
            or_(
                House.title.ilike(f"%{district}%"),
                House.description.ilike(f"%{district}%"),
                House.location.ilike(f"%{district}%"),
            )
        )
    return q.offset(skip).limit(limit).all()


@router.get("/districts", response_model=List[str])
def list_districts(city: str = Query(...)):
    return CITY_DISTRICTS.get(city, [])


@router.get("/{house_id}", response_model=HouseOut)
def get_house(house_id: int, db: Session = Depends(get_db)):
    obj = db.query(House).filter(House.id == house_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="House not found")
    return obj
