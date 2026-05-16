import json
from pathlib import Path

from app.models.review_model import Review
from app.models.order_model import Order
from app.models.order_item import OrderItem

from app.services.review_normalizer import normalize_review
from app.services.connected_account_service import validate_connected_account


def import_reviews_service(
    platform_key: str,
    source_user_id: str,
    db,
    current_user
):
    platform_key = platform_key.lower()

    created_reviews = 0
    skipped_reviews = 0
    skipped_wrong_source_user = 0
    skipped_not_owned_order = 0
    skipped_listing_not_in_order = 0

    try:
        validate_connected_account(
            db=db,
            current_user=current_user,
            platform=platform_key,
            source_user_id=source_user_id
        )

        BASE_DIR = Path(__file__).resolve().parents[2]
        DATA_DIR = BASE_DIR / "data"

        REVIEW_FILES = {
            "hepsiburada": DATA_DIR / "mock_sources" / "hepsiburada_reviews.json",
            "trendyol": DATA_DIR / "mock_sources" / "trendyol_reviews.json",
            "amazon": DATA_DIR / "mock_sources" / "amazon_reviews.json",
        }

        json_path = REVIEW_FILES.get(platform_key)

        if json_path is None:
            return {
                "error": f"Desteklenmeyen platform: {platform_key}"
            }

        if not json_path.exists():
            return {
                "error": f"No review file found for platform: {platform_key}",
                "expected_path": str(json_path)
            }

        with open(json_path, "r", encoding="utf-8") as file:
            reviews_data = json.load(file)

        for raw_review in reviews_data:
            review_data = normalize_review(platform_key, raw_review)

            if str(review_data.get("source_user_id")) != str(source_user_id):
                skipped_wrong_source_user += 1  #JSON’daki user_id, endpointteki source_user_id ile eşleşmiyor
                continue

            #Review, external_order_id + customer_id ile doğru order’a ait mi?
            order = db.query(Order).filter(
                Order.owner_user_id == current_user.id,
                Order.platform == platform_key,
                Order.source_user_id == source_user_id,
                Order.external_order_id == review_data["external_order_id"],
                Order.customer_id == review_data["customer_id"]
            ).first()

            if not order:
                skipped_not_owned_order += 1#bu order o kullanıcının değil
                continue

            #Review, listing_id o order’ın itemları içinde var mı?
            order_item = db.query(OrderItem).filter(
                OrderItem.order_id == order.id,
                OrderItem.listing_id == review_data["listing_id"]
            ).first()

            if not order_item:
                skipped_listing_not_in_order += 1#order doğru kullanıcının ama öyle bir listingi yok
                continue

            #Daha önce bu review eklendi mi kontrolü
            existing_review = db.query(Review).filter(
                Review.owner_user_id == current_user.id,
                Review.platform == platform_key,
                Review.source_user_id == source_user_id,
                Review.review_id == review_data["review_id"]
            ).first()

            if existing_review:
                skipped_reviews += 1#bu review daha önce eklendi
                continue

            new_review = Review(
                review_id=review_data["review_id"],

                owner_user_id=current_user.id,
                source_user_id=source_user_id,
                platform=platform_key,

                external_order_id=review_data["external_order_id"],
                customer_id=review_data["customer_id"],

                internal_product_id=review_data.get("internal_product_id"),
                listing_id=review_data["listing_id"],

                rating=review_data["rating"],
                comment=review_data.get("comment"),
                sentiment=review_data.get("sentiment"),
                topic=review_data.get("topic"),
                created_at=review_data["created_at"]
            )

            db.add(new_review)
            created_reviews += 1#yeni eklenen review

        db.commit()

        return {
            "message": f"{platform_key} reviews imported successfully.",
            "platform": platform_key,
            "source_user_id": source_user_id,
            "created_reviews": created_reviews,
            "skipped_reviews": skipped_reviews,
            "skipped_wrong_source_user": skipped_wrong_source_user,
            "skipped_not_owned_order": skipped_not_owned_order,
            "skipped_listing_not_in_order": skipped_listing_not_in_order
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }