import httpx
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime

TICARET_LOGO_URL = "https://ticaret.gov.tr/v2/images/logo-e.png?v=1"


def parse_ticaret_date(title: str):
    try:
        date_part = title.split("-")[-1].strip()
        return parser.parse(date_part, dayfirst=True).replace(tzinfo=None)
    except Exception:
        return None


def parse_turkish_date_from_header(header):
    if not header:
        return None

    months = [
        "ocak", "şubat", "mart", "nisan",
        "mayıs", "haziran", "temmuz",
        "ağustos", "eylül", "ekim",
        "kasım", "aralık"
    ]

    spans = header.find_all("span")

    for span in spans:
        text = span.get_text(" ", strip=True)

        if any(month in text.lower() for month in months):
            try:
               return parse_turkish_date_text(text)
            except Exception:
                return None

    return None


def scrape_ticaret_detail(url: str):
    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True,
            verify=False,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        header = soup.select_one("div.__header")
        content = soup.select_one("div.__content")

        title = None
        published_at = None
        description = None

        if header:
            h2 = header.find("h2")
            if h2:
                title = h2.get_text(" ", strip=True)

            published_at = parse_turkish_date_from_header(header)

        if content:
            description = content.get_text(" ", strip=True)

        return {
            "title": title,
            "description": description,
            "published_at": published_at
        }

    except Exception as e:
        print("TICARET DETAIL SCRAPE ERROR:", e)
        return {
            "title": None,
            "description": None,
            "published_at": None
        }


def scrape_ticaret_bakanligi():
    news_list = []

    try:
        response = httpx.get(
            "https://ticaret.gov.tr/duyurular",
            timeout=10,
            follow_redirects=True,
            verify=False,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        seen_urls = set()

        for link in links:
            href = link.get("href")

            if not href:
                continue

            if "/duyurular/" not in href:
                continue

            title_element = link.find("h5")
            if title_element:
                title = title_element.get_text(" ", strip=True)
            else:
                title = link.get_text(" ", strip=True)

            if not title:
                continue

            if href.startswith("http"):
                url = href
            else:
                url = f"https://ticaret.gov.tr{href}"

            if url in seen_urls:
                continue

            seen_urls.add(url)

            detail = scrape_ticaret_detail(url)

            news_list.append({
                "title": detail["title"] or title,
                "description": detail["description"] or title,
                "image_url": TICARET_LOGO_URL,
                "source": "Ticaret Bakanlığı Duyurular",
                "url": url,
                "category": "commerce_finance",
                "published_at": detail["published_at"] or parse_ticaret_date(title)
            })

    except Exception as e:
        print("TICARET SCRAPE ERROR:", e)

    return news_list

def parse_turkish_date_text(text: str):
    if not text:
        return None

    months = {
        "ocak": 1,
        "şubat": 2,
        "subat": 2,
        "mart": 3,
        "nisan": 4,
        "mayıs": 5,
        "mayis": 5,
        "haziran": 6,
        "temmuz": 7,
        "ağustos": 8,
        "agustos": 8,
        "eylül": 9,
        "eylul": 9,
        "ekim": 10,
        "kasım": 11,
        "kasim": 11,
        "aralık": 12,
        "aralik": 12,
    }

    parts = text.strip().lower().split()

    if len(parts) < 3:
        return None

    try:
        day = int(parts[0])
        month = months.get(parts[1])
        year = int(parts[2])

        if not month:
            return None

        return datetime(year, month, day)

    except Exception:
        return None