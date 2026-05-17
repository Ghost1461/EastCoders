def normalize_review(platform_key: str, raw_review: dict):
    return {
        "source_user_id": raw_review.get("user_id"),

        "external_order_id": raw_review.get("external_order_id"),

        "review_id": raw_review.get("review_id"),

        "customer_id": raw_review.get("customer_id"),

        "external_product_id": raw_review.get("external_product_id"),

        "listing_id": raw_review.get("listing_id"),

        "platform": platform_key.lower(),

        "rating": raw_review.get("rating"),

        "comment": raw_review.get("comment"),

        "sentiment": raw_review.get("sentiment"),

        "topic": raw_review.get("topic"),

        "created_at": raw_review.get("created_at")
    }