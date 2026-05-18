from app.models.user_model import User
from app.models.connected_account_model import ConnectedAccount
from app.models.ai_report_cache_model import AiReportCache


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
    query = db.query(ConnectedAccount)

    if platform:
        query = query.filter(
            ConnectedAccount.platform == platform.lower()
        )

    accounts = query.all()

    return {
        "count": len(accounts),
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