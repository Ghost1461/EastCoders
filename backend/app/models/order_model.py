from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(String, index=True)

    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    source_user_id = Column(String, nullable=False, index=True)
    platform = Column(String, nullable=False)
    external_order_id = Column(String, nullable=False, index=True)

    customer_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    order_date = Column(String, nullable=False)

    user = relationship("User", back_populates="orders")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

