import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session

from app.models import Order, OrderItem
from app.services.order_normalizer import normalize_order


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

ORDER_FILES = {
    "hepsiburada": DATA_DIR / "mock_sources" / "hepsiburada_orders.json",
    "trendyol": DATA_DIR / "mock_sources" / "trendyol_orders.json",
    "amazon": DATA_DIR / "mock_sources" / "amazon_orders.json",
}


def generate_order_id() -> str:
    return f"O-{uuid.uuid4().hex[:8].upper()}"


def generate_order_item_id() -> str:
    return f"OI-{uuid.uuid4().hex[:8].upper()}"


def import_orders_by_platform(db: Session, platform_key: str):
    file_path = ORDER_FILES.get(platform_key)

    if not file_path:
        raise ValueError(f"Unsupported platform: {platform_key}")

    with open(file_path, "r", encoding="utf-8") as file:
        raw_orders = json.load(file)

    created_orders = 0
    updated_orders = 0
    created_items = 0

    for raw_item in raw_orders:
        item = normalize_order(platform_key, raw_item)

        order_id = item.get("order_id") or generate_order_id()

        order = db.query(Order).filter(
            Order.platform == item.get("platform"),
            Order.external_order_id == item.get("external_order_id")
        ).first()

        if order:
            order.user_id = item.get("user_id")
            order.customer_id = item.get("customer_id")
            order.status = item.get("status", "pending")
            order.order_date = item.get("order_date")

            db.query(OrderItem).filter(
                OrderItem.order_id == order.order_id
            ).delete()

            updated_orders += 1

        else:
            order = Order(
                order_id=order_id,
                user_id=item.get("user_id"),
                platform=item.get("platform"),
                external_order_id=item.get("external_order_id"),
                customer_id=item.get("customer_id"),
                status=item.get("status", "pending"),
                order_date=item.get("order_date"),
            )

            db.add(order)
            db.flush()
            created_orders += 1

        for order_item in item.get("items", []):
            db_order_item = OrderItem(
                order_item_id=generate_order_item_id(),
                order_id=order.order_id,
                listing_id=order_item.get("listing_id"),
                quantity=order_item.get("quantity", 0),
                unit_price=order_item.get("unit_price", 0),
            )

            db.add(db_order_item)
            created_items += 1

    db.commit()

    return {
        "platform": platform_key,
        "message": f"{platform_key} siparişleri başarıyla aktarıldı",
        "created_orders": created_orders,
        "updated_orders": updated_orders,
        "created_items": created_items,
    }


def import_all_orders(db: Session):
    results = []

    for platform_key in ORDER_FILES.keys():
        result = import_orders_by_platform(db, platform_key)
        results.append(result)

    return {
        "message": "Tüm platform siparişleri başarıyla aktarıldı",
        "results": results,
    }