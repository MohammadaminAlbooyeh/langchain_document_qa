import requests
from bs4 import BeautifulSoup

def scrape_immobiliare(city="milano", page=1):
    url = f"https://www.immobiliare.it/en/vendita-case/{city}/?pag={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for card in soup.select(".nd-list__item"):
        title = card.select_one(".in-card__title")
        price = card.select_one(".in-card__price")
        location = card.select_one(".in-card__address")
        link = card.select_one("a")
        if not (title and price and location and link):
            continue
        results.append({
            "title": title.get_text(strip=True),
            "price": price.get_text(strip=True),
            "location": location.get_text(strip=True),
            "url": link["href"] if link.has_attr("href") else None
        })
    return results

if __name__ == "__main__":
    data = scrape_immobiliare("milano", 1)
    for item in data[:5]:
        print(item)
