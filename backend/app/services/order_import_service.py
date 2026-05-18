import json
from pathlib import Path

from app.models.order_model import Order
from app.models.order_item import OrderItem
from app.services.order_normalizer import normalize_order
from app.services.connected_account_service import validate_connected_account

def import_orders_service(
    platform_key: str,
    source_user_id: str,
    db,
    current_user
    ):
    
    #Bu user bu platform hesabını bağlamış mı
    validate_connected_account(
    db=db,
    current_user=current_user,
    platform=platform_key,
    source_user_id=source_user_id
    )
    
    def has_changes(obj, values: dict) -> bool:
        return any(
            getattr(obj, key) != value
            for key, value in values.items()
        )

    created_orders = 0
    updated_orders = 0
    created_items = 0

    platform_key = platform_key.lower()

    try:
        BASE_DIR = Path(__file__).resolve().parents[2]
        DATA_DIR = BASE_DIR / "data"

        ORDER_FILES = {
            "hepsiburada": DATA_DIR / "mock_sources" / "hepsiburada_orders.json",
            "trendyol": DATA_DIR / "mock_sources" / "trendyol_orders.json",
            "amazon": DATA_DIR / "mock_sources" / "amazon_orders.json",
        }

        json_path = ORDER_FILES.get(platform_key)

        if json_path is None:
            return {
                "error": f"Desteklenmeyen platform: {platform_key}"
            }

        if not json_path.exists():
            return {
                "error": f"No order file found for platform: {platform_key}",
                "expected_path": str(json_path)
            }

        with open(json_path, "r", encoding="utf-8") as file:
            orders_data = json.load(file)

        for order_data in orders_data:
            normalized_order = normalize_order(platform_key, order_data)

            #Sadece o login olan kullanıcının orderlarını import et(connected account bağlansa bile yanlış seller’ın orderı import edilmez)
            if normalized_order.get("user_id") != source_user_id:
                continue

            existing_order = db.query(Order).filter(
                Order.owner_user_id == current_user.id,
                Order.platform == platform_key,
                Order.source_user_id == source_user_id,
                Order.external_order_id == normalized_order["external_order_id"]
            ).first()

            if existing_order:
                order_values = {
                    "customer_id": normalized_order.get("customer_id"),
                    "status": normalized_order["status"],
                    "order_date": normalized_order["order_date"]
                }

                item_values = [
                    {
                        "listing_id": item["listing_id"],
                        "external_product_id": item["external_product_id"],
                        "quantity": item["quantity"],
                        "unit_price": item["unit_price"]
                    }
                    for item in normalized_order.get("items", [])
                ]

                existing_items = db.query(OrderItem).filter(
                    OrderItem.order_id == existing_order.id
                ).all()

                existing_item_values = [
                    {
                        "listing_id": item.listing_id,
                        "external_product_id": item.external_product_id,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price
                    }
                    for item in existing_items
                ]

                #sıralı vermez isek sıra değişince de updated_order artabilir, risk almaya gerek yok
                item_values = sorted(
                    item_values,
                    key=lambda x: x["listing_id"]
                )

                existing_item_values = sorted(
                    existing_item_values,
                    key=lambda x: x["listing_id"]
)

                order_changed = has_changes(existing_order, order_values)

                items_changed = existing_item_values != item_values

                if order_changed or items_changed:

                    for key, value in order_values.items():
                        setattr(existing_order, key, value)

                    db.query(OrderItem).filter(
                        OrderItem.order_id == existing_order.id
                    ).delete()

                    for order_item in normalized_order.get("items", []):
                        new_item = OrderItem(
                            order_id=existing_order.id,
                            listing_id=order_item["listing_id"],
                            external_product_id=order_item["external_product_id"],
                            quantity=order_item["quantity"],
                            unit_price=order_item["unit_price"]
                        )

                        db.add(new_item)
                        created_items += 1

                    updated_orders += 1

                continue

            new_order = Order(
                order_id=normalized_order["order_id"],
                owner_user_id=current_user.id,
                source_user_id=source_user_id,
                platform=platform_key,
                external_order_id=normalized_order["external_order_id"],
                customer_id=normalized_order.get("customer_id"),
                status=normalized_order["status"],
                order_date=normalized_order["order_date"]
            )

            db.add(new_order)
            db.flush()

            for order_item  in normalized_order.get("items", []):
                new_item = OrderItem(
                    order_id=new_order.id,
                    listing_id=order_item ["listing_id"],
                    external_product_id=order_item ["external_product_id"],
                    quantity=order_item ["quantity"],
                    unit_price=order_item ["unit_price"]
                )

                db.add(new_item)
                created_items += 1

            created_orders += 1

        db.commit()

        return {
            "message": f"{platform_key} siparişler başarıyla içe aktarıldı.",
            "platform": platform_key,
            "source_user_id": source_user_id,
            "created_orders": created_orders,
            "updated_orders": updated_orders,
            "created_items": created_items
        }
    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }