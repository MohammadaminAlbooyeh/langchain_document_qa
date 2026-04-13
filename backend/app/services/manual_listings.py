from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MANUAL_LISTINGS_PATH = Path("data/manual_listings.json")


def load_manual_listings() -> List[Dict[str, Any]]:
    if not MANUAL_LISTINGS_PATH.exists():
        return []

    try:
        payload = json.loads(MANUAL_LISTINGS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(payload, list):
        return []

    return [item for item in payload if isinstance(item, dict)]


def save_manual_listings(listings: List[Dict[str, Any]]) -> None:
    MANUAL_LISTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANUAL_LISTINGS_PATH.write_text(
        json.dumps(listings, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
