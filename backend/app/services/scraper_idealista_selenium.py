from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def scrape_idealista(city="torino", page=1, headless=True):
    url = f"https://www.idealista.it/ricerca.html?city={city}&tipo=vendita&page={page}"
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1200,800")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(4)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    results = []
    cards = soup.select("article, .item, .listing-item")
    for card in cards:
        title_el = card.select_one("a[itemprop='url'] h2, h2, .item-link, .title")
        price_el = card.select_one(".price, .item-price")
        location_el = card.select_one(".address, .item-location, .district")
        link_el = card.select_one("a")

        title = title_el.get_text(strip=True) if title_el else None
        price = price_el.get_text(strip=True) if price_el else None
        location = location_el.get_text(strip=True) if location_el else None
        link = link_el["href"] if link_el and link_el.has_attr("href") else None
        if link and link.startswith("/"):
            link = "https://www.idealista.it" + link

        if not (title or price or location):
            continue

        results.append({
            "title": title,
            "price": price,
            "location": location,
            "url": link,
        })

    return results


if __name__ == "__main__":
    data = scrape_idealista("torino", 1, headless=True)
    for item in data[:10]:
        print(item)
