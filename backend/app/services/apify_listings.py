from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

from app.core.config import settings


APIFY_BASE = "https://api.apify.com/v2"


def _first(record: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, ""):
            return value
    return default


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        if isinstance(value, str):
            digits = "".join(ch for ch in value if ch.isdigit() or ch == ".")
            return float(digits) if digits else default
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def normalize_apify_listing(record: Dict[str, Any], idx: int, source_name: str) -> Dict[str, Any]:
    title = _first(record, ["title", "name", "headline"], f"Listing {idx + 1}")
    location = _first(record, ["location", "city", "address", "district"], "Unknown")
    url = _first(record, ["url", "link", "listingUrl"])
    description = _first(record, ["description", "summary", "excerpt"])

    source_tag = f"Source: {source_name}"
    if url:
        source_tag = f"{source_tag} | {url}"

    return {
        "id": 2_000_000 + idx,
        "title": str(title),
        "description": (str(description) + "\n" + source_tag) if description else source_tag,
        "price": _to_float(_first(record, ["price", "amount", "cost", "monthly_rent"], 0)),
        "location": str(location),
        "bedrooms": _to_int(_first(record, ["bedrooms", "rooms", "room_count"], 0)),
        "bathrooms": _to_int(_first(record, ["bathrooms", "bathrooms_count"], 0)),
        "area_sqft": _to_float(_first(record, ["area_sqft", "area", "surface", "size"], 0.0)),
        "property_type": str(_first(record, ["property_type", "type", "category"], "apartment")),
        "owner_id": 0,
        "created_at": datetime.now(timezone.utc),
    }


def fetch_apify_actor_items(actor_id: str, source_name: str, city: str | None, limit: int) -> List[Dict[str, Any]]:
    if not settings.APIFY_TOKEN or not actor_id:
        return []

    endpoint = f"{APIFY_BASE}/acts/{actor_id}/run-sync-get-dataset-items"
    params = {
        "token": settings.APIFY_TOKEN,
        "timeout": 120,
        "memory": 1024,
    }

    payload: Dict[str, Any] = {
        "maxItems": limit,
    }
    if city:
        payload.update({
            "city": city,
            "location": city,
            "search": city,
            "query": city,
        })

    response = requests.post(endpoint, params=params, json=payload, timeout=150)
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        return []

    return [
        normalize_apify_listing(item, idx, source_name)
        for idx, item in enumerate(data)
        if isinstance(item, dict)
    ]
