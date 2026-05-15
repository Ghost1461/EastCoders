from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )
    listing_id = Column(String)
    internal_product_id = Column(String)

    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="items")