from fastapi import HTTPException

from app.models.connected_account_model import ConnectedAccount


def connect_platform_account_service(
    db,
    current_user,
    platform: str,
    source_user_id: str
):
    platform = platform.lower()

    #aktif hesap kontrolü sağlanıyor
    active_account = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id,
        ConnectedAccount.platform == platform,
        ConnectedAccount.is_active == True
    ).first()

    #aynı key tekrar bağlanırsa hata değil mesaj dönüyor
    if active_account:
        if active_account.source_user_id == source_user_id:
            return {
                "message": "Bu platform hesabı zaten kullanıcı hesabına bağlı.",
                "platform": platform,
                "source_user_id": source_user_id,
                "is_active": active_account.is_active
            }

        #farklı key bağlamayı engelleme
        raise HTTPException(
            status_code=400,
            detail=(
                f"Zaten bağlı aktif bir {platform} hesabınız (keyiniz) var. "
                f"Yeni bir key bağlamadan önce eskisini devre dışı bırakın."
            )
        )

    existing_account = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id,
        ConnectedAccount.platform == platform,
        ConnectedAccount.source_user_id == source_user_id
    ).first()

    #eski deactivate edilmiş hesabı tekrar aktif etme
    if existing_account:
        existing_account.is_active = True

        db.commit()
        db.refresh(existing_account)

        return {
            "message": "Platform hesabı yeniden etkinleştirildi.",
            "platform": platform,
            "source_user_id": source_user_id,
            "is_active": existing_account.is_active
        }

    new_account = ConnectedAccount(
        owner_user_id=current_user.id,
        platform=platform,
        source_user_id=source_user_id,
        is_active=True
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "message": "Platform hesabı başarıyla bağlandı.",
        "platform": platform,
        "source_user_id": source_user_id,
        "is_active": new_account.is_active
    }


def get_connected_accounts_service(db, current_user):
    accounts = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id
    ).all()

    return {
        "count": len(accounts),
        "accounts": [
            {
                "id": account.id,
                "platform": account.platform,
                "source_user_id": account.source_user_id,
                "is_active": account.is_active
            }
            for account in accounts
        ]
    }


def deactivate_connected_account_service(
    db,
    current_user,
    platform: str,
    source_user_id: str
):
    platform = platform.lower()

    account = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id,
        ConnectedAccount.platform == platform,
        ConnectedAccount.source_user_id == source_user_id,
        ConnectedAccount.is_active == True
    ).first()

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Aktif olarak bağlı hesap bulunamadı."
        )

    account.is_active = False

    db.commit()

    return {
        "message": "Bağlı hesap devre dışı bırakıldı.",
        "platform": platform,
        "source_user_id": source_user_id
    }


def validate_connected_account(
    db,
    current_user,
    platform: str,
    source_user_id: str
):
    platform = platform.lower()

    account = db.query(ConnectedAccount).filter(
        ConnectedAccount.owner_user_id == current_user.id,
        ConnectedAccount.platform == platform,
        ConnectedAccount.source_user_id == source_user_id,
        ConnectedAccount.is_active == True
    ).first()

    if not account:
        raise HTTPException(
            status_code=403,
            detail="!Uyarı, bu platform hesabı mevcut kullanıcıyla bağlantılı değil."
        )

    return account