from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time


def scrape_immobiliare(city="milano", page=1, headless=True):
    url = f"https://www.immobiliare.it/en/vendita-case/{city}/?pag={page}"
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
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
    data = scrape_immobiliare("milano", 1, headless=True)
    for item in data[:5]:
        print(item)
