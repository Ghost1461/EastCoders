import re

from playwright.async_api import async_playwright

from app.services.trend_normalizer_service import (
    normalize_product_name,
    normalize_category
)


TRENDYOL_BEST_SELLERS_URL = "https://www.trendyol.com/cok-satanlar"


def guess_category_from_name(product_name: str) -> str:
    name = product_name.lower()

    if any(word in name for word in ["pantolon", "jean", "tayt", "şort"]):
        return "Pantolon"

    if any(word in name for word in ["gömlek", "bluz", "tişört", "tshirt", "crop", "body", "atlet"]):
        return "Üst Giyim"

    if any(word in name for word in ["elbise", "abiye", "tulum"]):
        return "Elbise"

    if any(word in name for word in ["ceket", "mont", "kaban", "blazer", "trençkot"]):
        return "Dış Giyim"

    if any(word in name for word in ["etek"]):
        return "Etek"

    if any(word in name for word in ["sweatshirt", "hoodie", "kazak", "hırka"]):
        return "Sweatshirt/Kazak"

    if any(word in name for word in ["ayakkabı", "sneaker", "bot", "sandalet", "terlik"]):
        return "Ayakkabı"

    if any(word in name for word in ["çanta", "cüzdan"]):
        return "Çanta"

    return "Giyim"


def parse_trendyol_number(text: str):
    if not text:
        return None

    text = text.strip().lower()
    matches = re.findall(r"(\d+(?:[.,]\d+)?)(\s*[bm])?\+?", text)

    if not matches:
        return None

    selected_number = None
    selected_suffix = ""

    for number_text, suffix in matches:
        suffix = suffix.strip() if suffix else ""

        if suffix in ["b", "m"]:
            selected_number = number_text
            selected_suffix = suffix
            break

    if selected_number is None:
        selected_number, selected_suffix = matches[-1]
        selected_suffix = selected_suffix.strip() if selected_suffix else ""

    number = float(selected_number.replace(",", "."))

    if selected_suffix == "b":
        number *= 1000

    elif selected_suffix == "m":
        number *= 1_000_000

    return int(number)


def parse_price(text: str):
    if not text:
        return None

    clean = (
        text.replace("TL", "")
        .replace("₺", "")
        .replace("\n", " ")
        .replace("\xa0", " ")
        .strip()
    )

    match = re.search(
        r"\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+(?:,\d+)?",
        clean
    )

    if not match:
        return None

    number_text = (
        match.group()
        .replace(".", "")
        .replace(",", ".")
    )

    try:
        return float(number_text)
    except ValueError:
        return None


def calculate_social_signal(order_count, favorite_count, view_count):
    order_score = min((order_count or 0) / 2000, 1)
    favorite_score = min((favorite_count or 0) / 500000, 1)
    view_score = min((view_count or 0) / 100000, 1)

    return round(
        order_score * 0.45
        + favorite_score * 0.30
        + view_score * 0.25,
        2
    )


async def get_first_text(locator, selectors):
    for selector in selectors:
        el = locator.locator(selector)

        if await el.count() > 0:
            try:
                text = (await el.first.inner_text()).strip()

                if text:
                    return text
            except Exception:
                pass

    return None


async def fetch_trendyol_best_sellers(limit: int = 40):
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="tr-TR"
        )

        await page.goto(
            TRENDYOL_BEST_SELLERS_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        await page.wait_for_timeout(3000)

        cookie_button = page.locator(
            "button:has-text('Kabul Et'), "
            "button:has-text('Tümünü Kabul Et'), "
            "button:has-text('Accept')"
        )

        if await cookie_button.count() > 0:
            try:
                await cookie_button.first.click()
                await page.wait_for_timeout(1000)
            except Exception:
                pass

        giyim_button = page.locator("button.category-pill:has-text('Giyim')")

        if await giyim_button.count() == 0:
            print("Giyim button bulunamadı.")
            await browser.close()
            return []

        await giyim_button.first.click()
        await page.wait_for_timeout(4000)

        cards = page.locator("a.product-card-link")

        for _ in range(8):
            card_count = await cards.count()

            if card_count >= limit:
                break

            await page.mouse.wheel(0, 2500)
            await page.wait_for_timeout(1200)

        card_count = await cards.count()
        print("Trendyol product card count:", card_count)

        seen_names = set()

        for i in range(min(card_count, limit)):
            card = cards.nth(i)

            container = card.locator(
                "xpath=ancestor::div[contains(@class, 'product-card-wrapper')][1]"
            )

            search_area = (
                container
                if await container.count() > 0
                else card
            )

            image_el = search_area.locator("img[data-testid='product-image']")
            brand_el = search_area.locator("span.product-brand-name")
            rating_el = search_area.locator("span.rating-score")
            review_el = search_area.locator("span.p-total-rating-count")

            if await image_el.count() == 0:
                continue

            product_name = await image_el.first.get_attribute("alt")
            image_url = await image_el.first.get_attribute("src")

            if not product_name:
                continue

            clean_name = product_name.strip()

            if clean_name in seen_names:
                continue

            seen_names.add(clean_name)

            brand = None
            rating_text = None
            review_count_text = None

            if await brand_el.count() > 0:
                brand = (await brand_el.first.inner_text()).strip()

            price_text = await get_first_text(
                search_area,
                [
                    "div.ty-plus-discounted-price span",
                    "div.basket-price-discounted span",
                    "div.current-price__current",
                    "div.current-price__price-current",
                    "div.basket-price-original span"
                ]
            )

            if await rating_el.count() > 0:
                rating_text = (await rating_el.first.inner_text()).strip()

            if await review_el.count() > 0:
                review_count_text = (await review_el.first.inner_text()).strip()

            order_count_text = None
            favorite_count_text = None
            view_count_text = None

            social_items = search_area.locator("div.social-proof-item")
            social_count = await social_items.count()

            for j in range(social_count):
                social_item = social_items.nth(j)
                icon = social_item.locator("img.social-proof-item-icon")

                if await icon.count() == 0:
                    continue

                alt = await icon.first.get_attribute("alt")
                text = (await social_item.inner_text()).strip()

                if alt == "social-order-count":
                    order_count_text = text

                elif alt == "social-favorite-count":
                    favorite_count_text = text

                elif alt == "social-page-view-count":
                    view_count_text = text

            order_count = parse_trendyol_number(order_count_text)
            favorite_count = parse_trendyol_number(favorite_count_text)
            view_count = parse_trendyol_number(view_count_text)

            social_signal = calculate_social_signal(
                order_count=order_count,
                favorite_count=favorite_count,
                view_count=view_count
            )

            category = guess_category_from_name(clean_name)

            products.append({
                "trend_key": normalize_product_name(clean_name),
                "trend_name": clean_name,
                "brand": brand,
                "price_text": price_text,
                "price": parse_price(price_text),
                "rating_text": rating_text,
                "rating": float(rating_text.replace(",", ".")) if rating_text else None,
                "review_count_text": review_count_text,
                "review_count": parse_trendyol_number(review_count_text),
                "order_count_text": order_count_text,
                "order_count": order_count,
                "favorite_count_text": favorite_count_text,
                "favorite_count": favorite_count,
                "view_count_text": view_count_text,
                "view_count": view_count,
                "social_signal": social_signal,
                "image_url": image_url,
                "category": normalize_category(category),
                "platform": "trendyol",
                "source": "trendyol_cok_satanlar_giyim",
                "marketplace_signal": 1.0,
                "rank": len(products) + 1
            })

        await browser.close()

    return products