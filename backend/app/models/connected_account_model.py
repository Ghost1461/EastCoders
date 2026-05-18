from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime
from app.core.database import Base



class ConnectedAccount(Base):
    __tablename__ = "connected_accounts"

    id = Column(Integer, primary_key=True, index=True)

    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    platform = Column(String, nullable=False, index=True)
    source_user_id = Column(String, nullable=False, index=True)

    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="connected_accounts")

    last_synced_at = Column(
    DateTime(timezone=True),
    nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "owner_user_id",
            "platform",
            "source_user_id",
            name="uq_user_platform_source"
        ),
    )