from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship

TR_TIMEZONE = timezone(timedelta(hours=3))


def now_tr():
    return datetime.now(TR_TIMEZONE)

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="seller")

    created_at = Column(
    DateTime(timezone=True),
    default=now_tr
    )

    profile_image_url = Column(String, nullable=True)

    listings = relationship("ProductListing", back_populates="user")
    orders = relationship("Order", back_populates="user")
    connected_accounts = relationship(
    "ConnectedAccount",
    back_populates="user",
    cascade="all, delete-orphan"

)