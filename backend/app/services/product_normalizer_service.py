def normalize_trendyol_product(item: dict) -> dict:
    return {
        "platform": item.get("platform", "trendyol"),

        "external_product_id": item.get("external_product_id"),
        "seller_sku": item.get("seller_sku"),

        "source_user_id": item.get("user_id"),

        "name": item.get("name"),
        "brand": item.get("brand"),
        "category": item.get("category"),
        "gender": item.get("gender"),
        "color": item.get("color"),
        "size": item.get("size"),

        "price": item.get("price", 0),
        "stock": item.get("stock", 0),
        "commission_rate": item.get("commission_rate"),

        "rating": item.get("rating"),
        "review_count": item.get("review_count", 0),
        "status": item.get("status", "active"),

        "tags": item.get("tags", []),
        "image_url": item.get("image_url"),
        "last_updated": item.get("last_updated"),
    }


def normalize_hepsiburada_product(item: dict) -> dict:
    return {
        #"user_id": item.get("user_id"),

        "platform": item.get("platform", "hepsiburada"),

        "external_product_id": item.get("external_product_id"),
        "seller_sku": item.get("seller_sku"),

        "source_user_id": item.get("user_id"),

        "name": item.get("name"),
        "brand": item.get("brand"),
        "category": item.get("category"),
        "gender": item.get("gender"),
        "color": item.get("color"),
        "size": item.get("size"),

        "price": item.get("price", 0),
        "stock": item.get("stock", 0),
        "commission_rate": item.get("commission_rate"),

        "rating": item.get("rating"),
        "review_count": item.get("review_count", 0),
        "status": item.get("status", "active"),

        "tags": item.get("tags", []),
        "image_url": item.get("image_url"),
        "last_updated": item.get("last_updated"),
    }


def normalize_amazon_product(item: dict) -> dict:
    return {
        "platform": item.get("platform", "amazon"),

        "external_product_id": item.get("external_product_id"),
        "seller_sku": item.get("seller_sku"),

        "source_user_id": item.get("user_id"),

        "name": item.get("name"),
        "brand": item.get("brand"),
        "category": item.get("category"),
        "gender": item.get("gender"),
        "color": item.get("color"),
        "size": item.get("size"),

        "price": item.get("price", 0),
        "stock": item.get("stock", 0),
        "commission_rate": item.get("commission_rate"),

        "rating": item.get("rating"),
        "review_count": item.get("review_count", 0),
        "status": item.get("status", "active"),

        "tags": item.get("tags", []),
        "image_url": item.get("image_url"),
        "last_updated": item.get("last_updated"),
    }


NORMALIZERS = {
    "hepsiburada": normalize_hepsiburada_product,
    "trendyol": normalize_trendyol_product,
    "amazon": normalize_amazon_product,
}


def normalize_product(platform_key: str, item: dict) -> dict:
    normalizer = NORMALIZERS.get(platform_key)

    if not normalizer:
        raise ValueError(f"Desteklenmeyen platform: {platform_key}")

    return normalizer(item)