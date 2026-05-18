from app.services.product_import_service import import_products_by_platform
from app.services.order_import_service import import_orders_service
from app.services.review_import_service import import_reviews_service

#Frontend sayaç kullanıcı site açıkken çalışır, sekme kapanırsa durur. Bunun için zaman bazlı import sync frontendde(kullanıcı görsün değişiklikleri aktifken.)

#Backend scheduler kullanıcı siteyi kapatsa bile çalışır. Bunun için news sync backendde(değişiklikler kullanıcı görmeden de yapılsın, ona notification'u gitsin.)

def sync_platform_service(
    platform_key: str,
    source_user_id: str,
    db,
    current_user
):
    product_result = import_products_by_platform(
        db=db,
        platform_key=platform_key,
        current_user=current_user,
        source_user_id=source_user_id
    )

    order_result = import_orders_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )

    review_result = import_reviews_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )

    return {
        "message": "Sync completed successfully.",
        "platform": platform_key,
        "source_user_id": source_user_id,
        "results": {
            "products": product_result,
            "orders": order_result,
            "reviews": review_result
        }
    }