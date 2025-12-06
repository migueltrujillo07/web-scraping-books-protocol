import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


BASE_URL = "https://books.toscrape.com/"
CATALOG_URL = BASE_URL + "catalogue/page-{}.html"

DATA_RAW_DIR = os.path.join("data", "raw")
DATA_PROCESSED_DIR = os.path.join("data", "processed")
OUTPUT_CSV = os.path.join(DATA_PROCESSED_DIR, "books_catalog.csv")


def ensure_directories():
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)


def get_soup(url: str) -> BeautifulSoup:
    """Send a GET request and return a BeautifulSoup object."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_book_card(article_tag):
    """Extract book data from an <article> HTML element."""
    # Title
    title_tag = article_tag.h3.a
    title = title_tag["title"].strip()

    # Price
    price_tag = article_tag.select_one(".price_color")
    price_text = price_tag.get_text(strip=True).replace("£", "")
    try:
        price = float(price_text)
    except ValueError:
        price = None

    # Rating (stored as a class, e.g. "star-rating Three")
    rating_tag = article_tag.select_one(".star-rating")
    rating = None
    if rating_tag is not None:
        classes = rating_tag.get("class", [])
        # classes example: ['star-rating', 'Three']
        rating_classes = [c for c in classes if c != "star-rating"]
        rating = rating_classes[0] if rating_classes else None

    # Availability
    availability_tag = article_tag.select_one(".availability")
    availability = availability_tag.get_text(strip=True) if availability_tag else None

    # Product page URL
    link_tag = article_tag.h3.a
    relative_url = link_tag["href"]
    # Some URLs may contain '../', so we normalize them
    product_page_url = BASE_URL + "catalogue/" + relative_url.replace("../../../", "").replace("../../", "")

    return {
        "title": title,
        "price_gbp": price,
        "rating": rating,
        "availability": availability,
        "product_page_url": product_page_url,
    }


def scrape_page(page_number: int):
    """Scrape a single catalog page and return a list of book dicts."""
    url = CATALOG_URL.format(page_number)
    soup = get_soup(url)

    # Save raw HTML (optional, useful for protocol demonstration)
    raw_path = os.path.join(DATA_RAW_DIR, f"books_page_{page_number}.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    article_tags = soup.select("article.product_pod")
    books_data = [parse_book_card(article) for article in article_tags]
    return books_data


def scrape_all_pages(max_pages: int = 5, delay_seconds: float = 1.0):
    """Scrape multiple pages with a delay between requests."""
    all_books = []

    for page in tqdm(range(1, max_pages + 1), desc="Scraping pages"):
        try:
            page_books = scrape_page(page)
            if not page_books:
                # If no books were found, we assume we reached the end
                print(f"No books found on page {page}. Stopping.")
                break
            all_books.extend(page_books)
            time.sleep(delay_seconds)  # Be polite, avoid sending too many requests quickly
        except requests.HTTPError as e:
            print(f"HTTP error on page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break

    return all_books


def main():
    print("Starting web scraping data acquisition protocol...")
    ensure_directories()

    books = scrape_all_pages(max_pages=5, delay_seconds=1.0)

    if not books:
        print("No data collected. Exiting.")
        return

    df = pd.DataFrame(books)

    # Basic validation
    print(f"Total books scraped: {len(df)}")
    print(df.head())

    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Dataset saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

