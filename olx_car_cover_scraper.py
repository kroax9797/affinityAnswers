import requests
from bs4 import BeautifulSoup
import csv
import time

# URL for car cover search
BASE_URL = "https://www.olx.in/items/q-car-cover"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def get_listings(page=1):
    url = f"{BASE_URL}?page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []

    for item in soup.select("li.EIR5N"):
        title_tag = item.select_one("span._2tW1I")
        price_tag = item.select_one("span._89yzn")
        location_tag = item.select_one("span._2tW1I._1MIBT")
        link_tag = item.find("a", href=True)

        title = title_tag.text.strip() if title_tag else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"
        location = location_tag.text.strip() if location_tag else "N/A"
        link = "https://www.olx.in" + link_tag['href'] if link_tag else "N/A"

        listings.append({
            "title": title,
            "price": price,
            "location": location,
            "link": link
        })

    return listings

def scrape_all_pages(pages=3):
    all_listings = []
    for i in range(1, pages + 1):
        print(f"Scraping page {i}")
        listings = get_listings(page=i)
        all_listings.extend(listings)
        time.sleep(1)  # Be nice to OLX servers
    return all_listings

def save_to_csv(data, filename="car_covers_olx.csv"):
    keys = ["title", "price", "location", "link"]
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} listings to {filename}")

if __name__ == "__main__":
    listings = scrape_all_pages(pages=3)
    save_to_csv(listings)
