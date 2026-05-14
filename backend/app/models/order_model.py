from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)

    user_id = Column(String, nullable=True)
    platform = Column(String, nullable=False)
    external_order_id = Column(String, nullable=False, index=True)

    customer_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    order_date = Column(String, nullable=False)

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(String, primary_key=True, index=True)

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    listing_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")