import json
from scraper.amazon_scraper import scrape_laptops

if __name__ == "__main__":
    laptops = scrape_laptops()
    print(json.dumps(laptops, indent=2))
