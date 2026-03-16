import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Do not use this url extensively in testing, less we get marked as a bot.
# For simple tests, use a random url
SEARCH_URL = "https://www.amazon.com/s?k=laptops"
TARGET_COUNT = 5  # Number of laptop listings to return


def _build_driver() -> webdriver.Chrome:
    # Configure Chrome for reliable headless mode
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Set a realistic browser User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _check_blocked(driver: webdriver.Chrome) -> None:
    # TODO: This has not been tested
    title = driver.title.lower()
    if "robot" in title or "captcha" in title or "sorry" in title:
        raise RuntimeError(
            f"Amazon blocked the request (page title: '{driver.title}'). "
            "Try again later or use a different IP."
        )


def _extract_text(card, css: str):
    elements = card.find_elements(By.CSS_SELECTOR, css)
    return elements[0].get_attribute("textContent").strip() if elements else None


def _extract_url(card):
    # There's exactly one anchor wrapping an h2 per card that contains the URL
    elements = card.find_elements(By.CSS_SELECTOR, "a:has(h2)")
    if not elements:
        return None
    href = elements[0].get_attribute("href") or ""
    if href.startswith("http"):
        return href
    return "https://www.amazon.com" + href


def scrape_laptops():
    driver = _build_driver()
    try:
        driver.get(SEARCH_URL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
            )
        except TimeoutException:
            _check_blocked(driver)
            raise RuntimeError(
                f"No search results found on page (title: '{driver.title}'). "
                "The URL may be wrong or Amazon's page structure has changed."
            )

        cards = driver.find_elements(
            By.CSS_SELECTOR, "[data-component-type='s-search-result']"
        )

        results = []
        for card in cards:
            if len(results) >= TARGET_COUNT:
                break

            title = _extract_text(card, "h2 span")
            # If no title, skip this card
            if not title:
                continue

            # .a-offscreen is Amazon's visually-hidden span containing the clean price string (e.g. "$499.99")
            price = _extract_text(card, ".a-price .a-offscreen")
            # .a-icon-alt is the screen-reader text inside the star icon, e.g. "4.5 out of 5 stars"
            rating_el = card.find_elements(By.CSS_SELECTOR, ".a-icon-alt")
            rating = rating_el[0].get_attribute("textContent").strip() if rating_el else None
            url = _extract_url(card)

            results.append({
                "title": title,
                "price": price,
                "rating": rating,
                "url": url,
            })

        return results
    finally:
        driver.quit()
