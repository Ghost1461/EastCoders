from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime, timedelta, timezone

from app.core.database import Base


TR_TIMEZONE = timezone(timedelta(hours=3))


def now_tr():
    return datetime.now(TR_TIMEZONE)


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    platform = Column(String, nullable=False)

    source_user_id = Column(String, nullable=False)

    sync_type = Column(String, nullable=False)
    # manual / auto

    status = Column(String, nullable=False)
    # success / partial / failed

    created_products = Column(Integer, default=0)
    created_listings = Column(Integer, default=0)
    updated_listings = Column(Integer, default=0)

    created_orders = Column(Integer, default=0)
    created_items = Column(Integer, default=0)
    updated_orders= Column(Integer, default=0)

    created_reviews = Column(Integer, default=0)
    skipped_reviews = Column(Integer, default=0)

    synced_at = Column(
    DateTime(timezone=True),
    default=now_tr
)