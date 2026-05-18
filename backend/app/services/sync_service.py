from app.services.product_import_service import import_products_by_platform
from app.services.order_import_service import import_orders_service
from app.services.review_import_service import import_reviews_service
from datetime import datetime, timedelta, timezone
from app.models.sync_log_model import SyncLog
from app.models.connected_account_model import ConnectedAccount

#Frontend sayaç kullanıcı site açıkken çalışır, sekme kapanırsa durur. Bunun için zaman bazlı import sync frontendde(kullanıcı görsün değişiklikleri aktifken.)

#Backend scheduler kullanıcı siteyi kapatsa bile çalışır. Bunun için news sync backendde(değişiklikler kullanıcı görmeden de yapılsın, ona notification'u gitsin.)


TR_TIMEZONE = timezone(timedelta(hours=3))


def now_tr():
    return datetime.now(TR_TIMEZONE)


def sync_platform_service(
    platform_key: str,
    source_user_id: str,
    db,
    current_user
):
    platform_key = platform_key.lower()

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

    synced_at = now_tr()

    connected_account = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id,
        ConnectedAccount.platform == platform_key,
        ConnectedAccount.source_user_id == source_user_id
    ).first()

    if connected_account:
        connected_account.last_synced_at = synced_at

    sync_log = SyncLog(
        owner_user_id=current_user.id,
        platform=platform_key,
        source_user_id=source_user_id,

        sync_type="manual",
        status="success",

        created_products=product_result.get("new_products", 0),
        created_listings=product_result.get("created_listings", 0),
        updated_listings=product_result.get("updated_listings", 0),

        created_orders=order_result.get("created_orders", 0),
        updated_orders=order_result.get("updated_orders", 0),
        created_items=order_result.get("created_items", 0),

        created_reviews=review_result.get("created_reviews", 0),
        skipped_reviews=review_result.get("skipped_reviews", 0),
    )

    db.add(sync_log)
    db.commit()
    db.refresh(sync_log)

    return {
        "message": "Senkronizasyon başarıyla tamamlandı.",
        "platform": platform_key,
        "source_user_id": source_user_id,
        "last_synced_at": synced_at.isoformat(),
        "sync_log_id": sync_log.id,
        "results": {
            "products": product_result,
            "orders": order_result,
            "reviews": review_result
        }
    }