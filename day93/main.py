import json
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.audible.com/search?keywords=book&node=18573211011"
BASE_DIR = Path(__file__).parent
OUTPUT_FILE = BASE_DIR / "audible_books.json"
WAIT_SECONDS = 20


def get_text_or_none(parent, by, selector):
    try:
        return parent.find_element(by, selector).text.strip()
    except NoSuchElementException:
        return None


def click_if_visible(driver, by, selector):
    try:
        button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((by, selector))
        )
        button.click()
        return True
    except TimeoutException:
        return False


def dismiss_cookie_popup(driver):
    # Audible can show different cookie banners depending on region/AB test.
    selectors = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.CSS_SELECTOR, "button[aria-label='Accept Cookies']"),
        (By.CSS_SELECTOR, "button[data-purpose='accept-all-cookies-button']"),
    ]
    for by, selector in selectors:
        if click_if_visible(driver, by, selector):
            break


def scrape_results(driver):
    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.productListItem"))
    )
    cards = driver.find_elements(By.CSS_SELECTOR, "li.productListItem")
    books = []

    for card in cards:
        title = get_text_or_none(card, By.CSS_SELECTOR, "h3.bc-heading a")
        link = None
        try:
            link = card.find_element(By.CSS_SELECTOR, "h3.bc-heading a").get_attribute(
                "href"
            )
        except NoSuchElementException:
            pass

        author = get_text_or_none(card, By.CSS_SELECTOR, "li.authorLabel span a")
        narrator = get_text_or_none(card, By.CSS_SELECTOR, "li.narratorLabel span a")
        length = get_text_or_none(card, By.CSS_SELECTOR, "li.runtimeLabel span")
        language = get_text_or_none(card, By.CSS_SELECTOR, "li.languageLabel span")
        rating = get_text_or_none(card, By.CSS_SELECTOR, "li.ratingsLabel span")

        books.append(
            {
                "title": title,
                "author": author,
                "narrator": narrator,
                "length": length,
                "language": language,
                "rating": rating,
                "url": link,
            }
        )

    return books


def save_json(items, output_file):
    payload = {
        "source_url": URL,
        "scraped_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_items": len(items),
        "items": items,
    }
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def main():
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    driver = webdriver.Firefox(options=firefox_options)
    try:
        driver.get(URL)
        dismiss_cookie_popup(driver)
        books = scrape_results(driver)
        save_json(books, OUTPUT_FILE)
        print(f"Saved {len(books)} items to {OUTPUT_FILE}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
