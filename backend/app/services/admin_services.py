from app.models.user_model import User
from app.models.connected_account_model import ConnectedAccount
from app.models.ai_report_cache_model import AiReportCache
from app.models.product_listing_model import ProductListing
from app.models.user_model import User
from app.services.report_service import get_dashboard_report_service
from app.models.product_model import Product
from app.models.product_listing_model import ProductListing
from app.models.user_model import User

def get_all_users_service(db):
    users = db.query(User).all()

    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
                "profile_image_url": user.profile_image_url
            }
            for user in users
        ]
    }


def get_user_detail_service(user_id: int, db):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {"message": "Kullanıcı bulunamadı."}

    connected_accounts = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == user.id
    ).all()

    ai_cache_count = db.query(AiReportCache).filter(
        AiReportCache.user_id == user.id
    ).count()

    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "profile_image_url": user.profile_image_url
        },
        "connected_accounts": [
            {
                "id": account.id,
                "owner_user_id": account.owner_user_id,
                "platform": account.platform,
                "source_user_id": account.source_user_id,
                "is_active": account.is_active
            }
            for account in connected_accounts
        ],
        "ai_cache_count": ai_cache_count
    }



def get_ai_cache_records_service(db):
    records = db.query(AiReportCache).all()

    return {
        "count": len(records),
        "records": [
            {
                "id": record.id,
                "user_id": record.user_id,
                "report_type": record.report_type,
                "ai_response": record.ai_response,
                "input_hash": record.input_hash,
                "created_at": record.created_at
            }
            for record in records
        ]
    }


def delete_ai_cache_record_service(cache_id: int, db):
    record = db.query(AiReportCache).filter(
        AiReportCache.id == cache_id
    ).first()

    if not record:
        return {"message": "Cache kaydı bulunamadı."}

    db.delete(record)
    db.commit()

    return {
        "message": "AI cache kaydı silindi.",
        "cache_id": cache_id
    }


def get_admin_summary_service(db):
    return {
        "total_users": db.query(User).count(),
        "total_connected_accounts": db.query(ConnectedAccount).count(),
        "total_ai_cache_records": db.query(AiReportCache).count(),
    }


def delete_user_ai_cache_service(user_id: int, db):
    deleted_count = db.query(AiReportCache).filter(
        AiReportCache.user_id == user_id
    ).delete()

    db.commit()

    return {
        "message": "Kullanıcının AI cache kayıtları silindi.",
        "user_id": user_id,
        "deleted_count": deleted_count
    }


def get_all_connected_accounts_service(db, platform: str | None = None):

    SUPPORTED_PLATFORMS = [
        "amazon",
        "trendyol",
        "hepsiburada",
    ]

    query = db.query(ConnectedAccount)

    if platform:
        platform = platform.lower()

        if platform not in SUPPORTED_PLATFORMS:
            return {
                "message": f"Desteklenmeyen platform: {platform}",
                "supported_platforms": SUPPORTED_PLATFORMS
            }

        query = query.filter(
            ConnectedAccount.platform == platform
        )

    accounts = query.all()

    return {
        "count": len(accounts),
        "supported_platforms": SUPPORTED_PLATFORMS,
        "accounts": [
            {
                "id": account.id,
                "owner_user_id": account.owner_user_id,
                "platform": account.platform,
                "source_user_id": account.source_user_id,
                "is_active": account.is_active
            }
            for account in accounts
        ]
    }


# Sistemdeki tüm product listing kayıtlarını döner
def get_all_product_listings_service(db):
    listings = db.query(ProductListing).all()

    return {
        "count": len(listings),
        "listings": [
            {
                "listing_id": listing.listing_id,
                "internal_product_id": listing.internal_product_id,
                "user_id": listing.user_id,
                "source_user_id": listing.source_user_id,
                "platform": listing.platform,
                "external_product_id": listing.external_product_id,
                "seller_sku": listing.seller_sku,
                "price": listing.price,
                "stock": listing.stock,
                "commission_rate": listing.commission_rate,
                "rating": listing.rating,
                "review_count": listing.review_count,
                "status": listing.status
            }
            for listing in listings
        ]
    }



def get_user_dashboard_report_admin_service(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "Kullanıcı bulunamadı."}

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        },
        "report": get_dashboard_report_service(
            db=db,
            current_user=user
        )
    }


def search_user_dashboard_report_admin_service(db, email: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "Kullanıcı bulunamadı."}

    return get_user_dashboard_report_admin_service(
        db=db,
        user_id=user.id
    )



def get_user_nested_products_admin_service(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {
            "message": "Kullanıcı bulunamadı."
        }

    products = db.query(Product).all()

    result = []

    for product in products:
        listings = db.query(ProductListing).filter(
            ProductListing.internal_product_id == product.id,
            ProductListing.user_id == user_id
        ).all()

        if not listings:
            continue

        result.append({
            "internal_product_id": product.id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "gender": product.gender,
            "color": product.color,
            "size": product.size,
            "tags": product.tags,
            "image_url": product.image_url,
            "last_updated": product.last_updated,
            "listings": [
                {
                    "listing_id": listing.listing_id,
                    "platform": listing.platform,
                    "external_product_id": listing.external_product_id,
                    "seller_sku": listing.seller_sku,
                    "price": listing.price,
                    "stock": listing.stock,
                    "commission_rate": listing.commission_rate,
                    "rating": listing.rating,
                    "review_count": listing.review_count,
                    "status": listing.status,
                    "source_user_id": listing.source_user_id,
                    "user_id": listing.user_id
                }
                for listing in listings
            ]
        })

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "count": len(result),
        "products": result
    }