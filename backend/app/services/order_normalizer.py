def normalize_amazon_order(item: dict) -> dict:
    return {
        "order_id": item.get("order_id"),
        "user_id": item.get("user_id"),
        "platform": item.get("platform", "amazon").lower(),
        "external_order_id": item.get("external_order_id"),
        "customer_id": item.get("customer_id"),
        "items": item.get("items", []),
        "status": item.get("status", "pending"),
        "order_date": item.get("order_date"),
    }


def normalize_trendyol_order(item: dict) -> dict:
    return {
        "order_id": item.get("order_id"),
        "user_id": item.get("user_id"),
        "platform": item.get("platform", "trendyol").lower(),
        "external_order_id": item.get("external_order_id"),
        "customer_id": item.get("customer_id"),
        "items": item.get("items", []),
        "status": item.get("status", "pending"),
        "order_date": item.get("order_date"),
    }


def normalize_hepsiburada_order(item: dict) -> dict:
    return {
        "order_id": item.get("order_id"),
        "user_id": item.get("user_id"),
        "platform": item.get("platform", "hepsiburada").lower(),
        "external_order_id": item.get("external_order_id"),
        "customer_id": item.get("customer_id"),
        "items": item.get("items", []),
        "status": item.get("status", "pending"),
        "order_date": item.get("order_date"),
    }


NORMALIZERS = {
    "amazon": normalize_amazon_order,
    "trendyol": normalize_trendyol_order,
    "hepsiburada": normalize_hepsiburada_order,
}


def normalize_order(platform_key: str, item: dict) -> dict:
    normalizer = NORMALIZERS.get(platform_key)

    if not normalizer:
        raise ValueError(f"Unsupported platform: {platform_key}")

    return normalizer(item)