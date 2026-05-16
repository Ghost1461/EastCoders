from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.models.news_notification_model import NewsNotification


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/unread-count")
def get_unread_notification_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = (
        db.query(NewsNotification)
        .filter(
            NewsNotification.user_id == current_user.id,
            NewsNotification.is_read == False
        )
        .count()
    )

    return {
        "unread_count": count,
        "has_unread": count > 0
    }


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = (
        db.query(NewsNotification)
        .options(joinedload(NewsNotification.news))
        .filter(NewsNotification.user_id == current_user.id)
        .order_by(NewsNotification.created_at.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "notification_id": item.id,
            "news_id": item.news.id,
            "title": item.news.title,
            "source": item.news.source,
            "category": item.news.category,
            "image_url": item.news.image_url,
            "url": item.news.url,
            "is_read": item.is_read,
            "created_at": item.created_at,
            "published_at": item.news.published_at
        }
        for item in notifications
    ]


@router.post("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = (
        db.query(NewsNotification)
        .filter(
            NewsNotification.id == notification_id,
            NewsNotification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Bildirim bulunamadı.")

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return {
        "message": "Bildirim okundu olarak işaretlendi.",
        "notification_id": notification.id,
        "is_read": notification.is_read
    }