def normalize_hepsiburada_product(item: dict) -> dict:
    return {
        "platform": "Hepsiburada",
        "external_product_id": item["hb_product_id"],
        "seller_sku": item["merchant_sku"],
        "name": item["product_name"],
        "brand": item.get("brand"),
        "category": item.get("category_name"),
        "color": item.get("color"),
        "size": item.get("size"),
        "price": item["sale_price"],
        "stock": item["available_stock"],
        "commission_rate": item.get("commission_rate"),
        "rating": item.get("rating"),
        "review_count": item.get("review_count", 0),
        "status": item.get("status", "active")
    }


def normalize_trendyol_product(item: dict) -> dict:
    return {
        "platform": "Trendyol",
        "external_product_id": item["id"],
        "seller_sku": item["stockCode"],
        "name": item["title"],
        "brand": item.get("brand"),
        "category": item.get("categoryName"),
        "color": item.get("color"),
        "size": item.get("size"),
        "price": item["salePrice"],
        "stock": item["quantity"],
        "commission_rate": item.get("commissionRate"),
        "rating": item.get("ratingScore"),
        "review_count": item.get("reviewCount", 0),
        "status": "active" if item.get("approved", True) else "passive"
    }


def normalize_amazon_product(item: dict) -> dict:
    return {
        "platform": "Amazon",
        "external_product_id": item["asin"],
        "seller_sku": item["seller_sku"],
        "name": item["item_name"],
        "brand": item.get("brand"),
        "category": item.get("category"),
        "color": item.get("color"),
        "size": item.get("size"),
        "price": item["price"],
        "stock": item["quantity"],
        "commission_rate": item.get("commission_rate"),
        "rating": item.get("rating"),
        "review_count": item.get("review_count", 0),
        "status": item.get("status", "active")
    }


NORMALIZERS = {
    "hepsiburada": normalize_hepsiburada_product,
    "trendyol": normalize_trendyol_product,
    "amazon": normalize_amazon_product,
}


def normalize_product(platform_key: str, item: dict) -> dict:
    normalizer = NORMALIZERS.get(platform_key)

    if not normalizer:
        raise ValueError(f"Unsupported platform: {platform_key}")

    return normalizer(item)