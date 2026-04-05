from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict

from app.core.deps import get_db
from app.services.search_service import search_houses

router = APIRouter()


@router.post("/", response_model=list)
def search(filters: Dict[str, Any], skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return search_houses(db, filters, skip=skip, limit=limit)
