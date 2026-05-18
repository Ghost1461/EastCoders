from dateutil import parser
from bs4 import BeautifulSoup
import httpx

def parse_date(date_value):
    if not date_value:
        return None

    try:
        return parser.parse(date_value).replace(tzinfo=None)
    except Exception:
        return None


def clean_html(value):
    if not value:
        return None

    soup = BeautifulSoup(value, "html.parser")
    return soup.get_text(" ", strip=True)


def extract_image_url(item, description=None):
    if "media_content" in item and item["media_content"]:
        return item["media_content"][0].get("url")

    if "media_thumbnail" in item and item["media_thumbnail"]:
        return item["media_thumbnail"][0].get("url")

    if "enclosures" in item and item["enclosures"]:
        for enclosure in item["enclosures"]:
            href = enclosure.get("href")
            enclosure_type = enclosure.get("type", "")

            if href and (
                enclosure_type.startswith("image")
                or href.endswith((".jpg", ".jpeg", ".png", ".webp"))
            ):
                return href

    if description:
        soup = BeautifulSoup(description, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img.get("src")

    return None


def normalize_rss_item(item, source_name: str, category: str):
    title = item.get("title")
    description = item.get("summary") or item.get("description")
    url = item.get("link")

    if not description and url:
     description = fetch_description_from_article(url)
    
    if not title or not url:
        return None

    image_url = extract_image_url(item, description)
    if not image_url and url:
     image_url = fetch_image_from_article(url)

    published_at = None
    if item.get("published"):
        published_at = parse_date(item.get("published"))
    elif item.get("updated"):
        published_at = parse_date(item.get("updated"))

    return {
        "title": clean_html(title),
        "description": clean_html(description),
        "image_url": image_url,
        "source": source_name,
        "url": url,
        "category": category,
        "published_at": published_at
    }
    
def fetch_image_from_article(url: str) -> str | None:
    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        )

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # og:image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image.get("content")

        # twitter:image
        twitter_image = soup.find(
            "meta",
            attrs={"name": "twitter:image"}
        )

        if twitter_image and twitter_image.get("content"):
            return twitter_image.get("content")

        # Gazete Moda featured image
        featured_image = soup.find(
            "img",
            class_="attachment-newsever-featured"
        )

        if featured_image and featured_image.get("src"):
            return featured_image.get("src")

        # article içindeki ilk görsel
        article = soup.find("article")

        if article:
            images = article.find_all("img")

            for img in images:
                src = img.get("src")

                if (
                    src
                    and "logo" not in src.lower()
                    and "icon" not in src.lower()
                ):
                    return src

        return None

    except Exception:
        return None    
    
def fetch_description_from_article(url: str) -> str | None:
    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        )

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        summary = soup.find("p", class_="news-detail-summary")

        if summary:
            return summary.get_text(" ", strip=True)

        return None

    except Exception:
        return None    