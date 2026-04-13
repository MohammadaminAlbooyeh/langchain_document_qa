from __future__ import annotations

import argparse
import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app.services.manual_listings import save_manual_listings


def _parse_price(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    digits = re.sub(r"[^\d]", "", str(value))
    return float(digits) if digits else 0.0


def _stable_id(source_name: str, title: str, location: str, idx: int) -> int:
    digest = hashlib.sha1(f"{source_name}|{title}|{location}|{idx}".encode("utf-8")).hexdigest()[:10]
    return 3_000_000 + int(digest, 16)


def _normalize(item: Dict[str, Any], idx: int, source_name: str) -> Dict[str, Any]:
    title = str(item.get("title") or f"Listing {idx + 1}")
    location = str(item.get("location") or "Unknown")
    url = item.get("url")
    desc = f"Source: {source_name}" + (f" | {url}" if url else "")

    return {
        "id": _stable_id(source_name, title, location, idx),
        "title": title,
        "description": desc,
        "price": _parse_price(item.get("price")),
        "location": location,
        "bedrooms": 0,
        "bathrooms": 0,
        "area_sqft": 0.0,
        "property_type": "apartment",
        "owner_id": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _open_browser() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


def _capture_immobiliare(city_slug: str, page: int) -> List[Dict[str, Any]]:
    url = f"https://www.immobiliare.it/en/vendita-case/{city_slug}/?pag={page}"
    driver = _open_browser()
    try:
        print(f"\nOpen in browser: {url}")
        print("Solve captcha / scroll if needed, then press ENTER in terminal.")
        driver.get(url)
        input("Press ENTER when listings are visible on screen...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()

    results: List[Dict[str, Any]] = []
    for card in soup.select(".nd-list__item"):
        title = card.select_one(".in-card__title")
        price = card.select_one(".in-card__price")
        location = card.select_one(".in-card__address")
        link = card.select_one("a")
        if not (title and price and location and link):
            continue
        results.append(
            {
                "title": title.get_text(strip=True),
                "price": price.get_text(strip=True),
                "location": location.get_text(strip=True),
                "url": link.get("href"),
            }
        )
    return results


def _capture_idealista(city_slug: str, page: int) -> List[Dict[str, Any]]:
    url = f"https://www.idealista.it/ricerca.html?city={city_slug}&tipo=vendita&page={page}"
    driver = _open_browser()
    try:
        print(f"\nOpen in browser: {url}")
        print("Solve captcha / scroll if needed, then press ENTER in terminal.")
        driver.get(url)
        input("Press ENTER when listings are visible on screen...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()

    results: List[Dict[str, Any]] = []
    cards = soup.select(".item, .listing-item, .nd-list__item, article")
    for card in cards:
        title_el = card.select_one(".item-link, .title, .in-card__title, h2, a")
        price_el = card.select_one(".price, .item-price, .in-card__price")
        location_el = card.select_one(".district, .location, .item-location, .in-card__address")
        link_el = card.select_one("a")

        title = title_el.get_text(strip=True) if title_el else None
        price = price_el.get_text(strip=True) if price_el else None
        location = location_el.get_text(strip=True) if location_el else None
        link = link_el.get("href") if link_el else None

        if not title and not price and not location:
            continue

        if link and link.startswith("/"):
            link = "https://www.idealista.it" + link

        results.append(
            {
                "title": title,
                "price": price,
                "location": location,
                "url": link,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual in-browser capture for real estate listings.")
    parser.add_argument("--city", default="torino", help="City slug used in target websites, e.g. torino, milano")
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    city_slug = args.city.strip().lower()
    page = args.page

    merged: List[Dict[str, Any]] = []

    immobiliare_rows = _capture_immobiliare(city_slug=city_slug, page=page)
    for idx, row in enumerate(immobiliare_rows):
        merged.append(_normalize(row, idx, "immobiliare.it (manual)"))

    idealista_rows = _capture_idealista(city_slug=city_slug, page=page)
    for idx, row in enumerate(idealista_rows):
        merged.append(_normalize(row, len(merged) + idx, "idealista.it (manual)"))

    save_manual_listings(merged)
    print(f"Saved {len(merged)} manual listings to data/manual_listings.json")


if __name__ == "__main__":
    main()
