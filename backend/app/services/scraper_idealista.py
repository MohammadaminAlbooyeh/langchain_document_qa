import requests
from bs4 import BeautifulSoup


def scrape_idealista(city="torino", page=1):
    # Build a simple search URL for Idealista (may vary by site structure)
    url = f"https://www.idealista.it/ricerca.html?city={city}&tipo=vendita&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    from app.core.config import settings
    proxies = {"http": settings.PROXY_URL, "https": settings.PROXY_URL} if getattr(settings, "PROXY_URL", None) else None
    resp = requests.get(url, headers=headers, timeout=15, proxies=proxies)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # Try a few common listing container selectors
    cards = soup.select(".item, .listing-item, .nd-list__item, article")
    for card in cards:
        # title
        title_el = card.select_one(".item-link, .title, .in-card__title, h2, a")
        price_el = card.select_one(".price, .item-price, .in-card__price")
        location_el = card.select_one(".district, .location, .item-location, .in-card__address")
        link_el = card.select_one("a")

        title = title_el.get_text(strip=True) if title_el else None
        price = price_el.get_text(strip=True) if price_el else None
        location = location_el.get_text(strip=True) if location_el else None
        link = link_el["href"] if link_el and link_el.has_attr("href") else None

        if not title and not price and not location:
            continue

        # Normalize relative links
        if link and link.startswith("/"):
            link = "https://www.idealista.it" + link

        results.append({
            "title": title,
            "price": price,
            "location": location,
            "url": link,
        })

    return results


if __name__ == "__main__":
    data = scrape_idealista("torino", 1)
    for item in data[:10]:
        print(item)
