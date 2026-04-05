from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.house import House


def search_houses(db: Session, filters: Dict[str, Any], skip: int = 0, limit: int = 50):
    q = db.query(House)
    if "city" in filters:
        q = q.filter(House.city == filters["city"])
    return q.offset(skip).limit(limit).all()
