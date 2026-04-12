from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from urllib.request import Request, urlopen

from app.core.config import settings


def _build_url(base_url: str, filters: Dict[str, Any]) -> str:
    parsed_url = urlparse(base_url)
    query_params = dict(parse_qsl(parsed_url.query))

    for key, value in filters.items():
        if value is None or value == "":
            continue
        query_params[key] = str(value)

    return urlunparse(parsed_url._replace(query=urlencode(query_params)))


def _unwrap_payload(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in ("results", "data", "items", "listings", "properties"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_value(record: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, ""):
            return value
    return default


def _stable_external_id(record: Dict[str, Any], index: int) -> int:
    fingerprint = "|".join(
        [
            str(record.get("id") or record.get("external_id") or ""),
            str(record.get("title") or record.get("name") or ""),
            str(record.get("location") or record.get("city") or ""),
            str(record.get("price") or record.get("amount") or ""),
            str(index),
        ]
    )
    digest = hashlib.sha1(fingerprint.encode("utf-8")).hexdigest()[:10]
    return int(digest, 16)


def normalize_external_listing(record: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
    title = _first_value(record, ["title", "name", "headline", "property_title"], "External listing")
    location = _first_value(record, ["location", "city", "address", "area"], "Unknown location")
    description = _first_value(record, ["description", "summary", "excerpt", "details"])

    return {
        "id": _stable_external_id(record, index),
        "title": str(title),
        "description": str(description) if description is not None else None,
        "price": _as_float(_first_value(record, ["price", "amount", "cost", "monthly_rent"], 0)),
        "location": str(location),
        "bedrooms": _as_int(_first_value(record, ["bedrooms", "rooms", "room_count"], 0)),
        "bathrooms": _as_int(_first_value(record, ["bathrooms", "bathrooms_count"], 0)),
        "area_sqft": _as_float(_first_value(record, ["area_sqft", "area", "surface", "size"], 0)),
        "property_type": str(_first_value(record, ["property_type", "type", "category"], "apartment")),
        "owner_id": 0,
        "created_at": datetime.now(timezone.utc),
    }


def fetch_external_listings(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not settings.LISTINGS_API_URL:
        return []

    request_url = _build_url(settings.LISTINGS_API_URL, filters)
    request_headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; HouseFinderBot/1.0)",
    }
    if settings.LISTINGS_API_TOKEN:
        request_headers["Authorization"] = f"Bearer {settings.LISTINGS_API_TOKEN}"

    request = Request(request_url, headers=request_headers)

    try:
        with urlopen(request, timeout=settings.LISTINGS_API_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} from external listings API") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach external listings API: {exc.reason}") from exc

    return [normalize_external_listing(record, index) for index, record in enumerate(_unwrap_payload(payload))]