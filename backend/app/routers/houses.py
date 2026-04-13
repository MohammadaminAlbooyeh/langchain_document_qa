
from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.config import settings
from app.core.deps import get_db
from app.models.house import House
from app.schemas.house import HouseOut
from app.services.external_listings import fetch_external_listings
from app.services.apify_listings import fetch_apify_actor_items
from app.services.manual_listings import load_manual_listings
from app.services.scraper_immobiliare import scrape_immobiliare
from app.services.scraper_idealista import scrape_idealista
from app.services.scraper_immobiliare_selenium import scrape_immobiliare as scrape_immobiliare_selenium
from app.services.scraper_idealista_selenium import scrape_idealista as scrape_idealista_selenium

router = APIRouter()

CITY_SLUGS = {
    "Milan": "milano",
    "Rome": "roma",
    "Turin": "torino",
    "Naples": "napoli",
    "Florence": "firenze",
    "Venice": "venezia",
    "Bologna": "bologna",
    "Genoa": "genova",
    "Palermo": "palermo",
    "Bari": "bari",
    "Catania": "catania",
    "Verona": "verona",
    "Messina": "messina",
    "Padua": "padova",
    "Trieste": "trieste",
    "Taranto": "taranto",
    "Brescia": "brescia",
    "Prato": "prato",
    "Parma": "parma",
    "Modena": "modena",
    "Reggio Calabria": "reggio-calabria",
}

CITY_DISTRICTS = {
    "Milan": ["Navigli", "Brera", "Porta Romana", "Isola"],
    "Rome": ["Centro Storico", "Trastevere", "Prati", "Monti"],
    "Turin": ["Centro", "Crocetta", "San Salvario", "Lingotto"],
    "Florence": ["Duomo", "Santa Maria Novella", "Oltrarno", "San Lorenzo"],
    "Venice": ["San Marco", "Cannaregio", "Dorsoduro", "Castello"],
    "Bologna": ["Centro Storico", "Porto", "Santo Stefano", "Bolognina"],
}


def _city_to_slug(city: Optional[str]) -> str:
    if not city:
        return "milano"
    return CITY_SLUGS.get(city, city.strip().lower().replace(" ", "-"))


def _parse_price(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    digits = re.sub(r"[^\d]", "", str(value))
    return float(digits) if digits else 0.0


def _normalize_scraped_listing(item: Dict[str, Any], idx: int, source_name: str) -> Dict[str, Any]:
    title = str(item.get("title") or f"Listing {idx + 1}")
    url = item.get("url")
    description = f"Source: {source_name}" + (f" | {url}" if url else "")
    return {
        "id": 1_000_000 + idx,
        "title": title,
        "description": description,
        "price": _parse_price(item.get("price")),
        "location": str(item.get("location") or "Unknown"),
        "bedrooms": 0,
        "bathrooms": 0,
        "area_sqft": 0.0,
        "property_type": "apartment",
        "owner_id": 0,
        "created_at": datetime.now(timezone.utc),
    }


def _matches_filters(item: Dict[str, Any], city: Optional[str], district: Optional[str], min_price: Optional[float], max_price: Optional[float], rooms: Optional[int]) -> bool:
    location = str(item.get("location") or "").lower()
    title = str(item.get("title") or "").lower()

    if city and city.lower() not in location and city.lower() not in title:
        return False
    if district:
        district_l = district.lower()
        description = str(item.get("description") or "").lower()
        if district_l not in location and district_l not in title and district_l not in description:
            return False

    price = float(item.get("price") or 0.0)
    if min_price is not None and price < min_price:
        return False
    if max_price is not None and price > max_price:
        return False

    # Scraped sources do not expose room count reliably in current parser.
    if rooms is not None:
        bedrooms = int(item.get("bedrooms") or 0)
        if bedrooms and bedrooms < int(rooms):
            return False

    return True


def _fetch_scraped_listings(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    city = filters.get("city")
    district = filters.get("district")
    min_price = filters.get("min_price")
    max_price = filters.get("max_price")
    rooms = filters.get("rooms")
    page = 1
    city_slug = _city_to_slug(city)

    merged: List[Dict[str, Any]] = []

    # Try requests-based first
    try:
        imm = scrape_immobiliare(city=city_slug, page=page)
    except Exception:
        imm = []
    try:
        ide = scrape_idealista(city=city_slug, page=page)
    except Exception:
        ide = []

    if not imm:
        try:
            imm = scrape_immobiliare_selenium(city=city_slug, page=page, headless=True)
        except Exception:
            imm = []
    if not ide:
        try:
            ide = scrape_idealista_selenium(city=city_slug, page=page, headless=True)
        except Exception:
            ide = []

    for idx, row in enumerate(imm):
        merged.append(_normalize_scraped_listing(row, len(merged) + idx, "immobiliare.it"))
    for idx, row in enumerate(ide):
        merged.append(_normalize_scraped_listing(row, len(merged) + idx, "idealista.it"))

    return [
        item
        for item in merged
        if _matches_filters(item, city=city, district=district, min_price=min_price, max_price=max_price, rooms=rooms)
    ]


def _fetch_apify_listings(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    city = filters.get("city")
    district = filters.get("district")
    min_price = filters.get("min_price")
    max_price = filters.get("max_price")
    rooms = filters.get("rooms")
    limit = int(filters.get("limit") or 50)

    merged: List[Dict[str, Any]] = []

    # Requested order: 1) immobiliare 2) idealista
    try:
        merged.extend(
            fetch_apify_actor_items(
                actor_id=settings.APIFY_IMMOBILIARE_ACTOR_ID or "",
                source_name="immobiliare.it",
                city=city,
                limit=limit,
            )
        )
    except Exception:
        pass

    try:
        merged.extend(
            fetch_apify_actor_items(
                actor_id=settings.APIFY_IDEALISTA_ACTOR_ID or "",
                source_name="idealista.it",
                city=city,
                limit=limit,
            )
        )
    except Exception:
        pass

    return [
        item
        for item in merged
        if _matches_filters(item, city=city, district=district, min_price=min_price, max_price=max_price, rooms=rooms)
    ]


def _fetch_manual_cached_listings(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    city = filters.get("city")
    district = filters.get("district")
    min_price = filters.get("min_price")
    max_price = filters.get("max_price")
    rooms = filters.get("rooms")

    manual_rows = load_manual_listings()
    return [
        item
        for item in manual_rows
        if _matches_filters(item, city=city, district=district, min_price=min_price, max_price=max_price, rooms=rooms)
    ]


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

    if normalized_source in ("auto", "manual"):
        manual_listings = _fetch_manual_cached_listings(filters)
        if normalized_source == "manual":
            if manual_listings:
                return manual_listings[:limit]
            raise HTTPException(
                status_code=502,
                detail=(
                    "No manual-captured live listings found. Run manual capture first: "
                    "python -m app.services.manual_capture --city torino"
                ),
            )
        if manual_listings:
            return manual_listings[:limit]

    if normalized_source in ("auto", "apify"):
        apify_listings = _fetch_apify_listings(filters)
        if normalized_source == "apify":
            return apify_listings[:limit]
        if apify_listings:
            return apify_listings[:limit]

    if normalized_source in ("auto", "scrape"):
        scraped_listings = _fetch_scraped_listings(filters)
        if normalized_source == "scrape":
            if scraped_listings:
                return scraped_listings[:limit]
            raise HTTPException(
                status_code=502,
                detail=(
                    "Scraping blocked by target website anti-bot protection (DataDome/CAPTCHA). "
                    "Try source=auto for DB fallback or use an approved data provider."
                ),
            )
        if scraped_listings:
            return scraped_listings[:limit]

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

    # Live-first mode: do not silently fall back to seeded/local DB in auto mode.
    if normalized_source in ("auto", "manual", "scrape", "apify", "external"):
        raise HTTPException(
            status_code=502,
            detail=(
                "No live listings available right now. Target websites are blocking automated requests "
                "or external source returned no data."
            ),
        )

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
