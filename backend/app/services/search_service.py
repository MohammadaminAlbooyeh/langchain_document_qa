from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.house import House


def search_houses(db: Session, filters: Dict[str, Any], skip: int = 0, limit: int = 50):
    q = db.query(House)
    if "city" in filters:
        q = q.filter(House.city == filters["city"])
    # Filter by minimum number of bedrooms when `rooms` provided.
    # Treat the value as a minimum (e.g., rooms=1 means bedrooms >= 1).
    if "rooms" in filters and filters["rooms"] is not None:
        try:
            min_rooms = int(filters["rooms"])
            q = q.filter(House.bedrooms >= min_rooms)
        except (ValueError, TypeError):
            pass
    return q.offset(skip).limit(limit).all()
