from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProductListing(Base):
    __tablename__ = "product_listings"

    listing_id = Column(String, primary_key=True, index=True)

    internal_product_id = Column(
        String,
        ForeignKey("products.internal_product_id"),
        nullable=False
    )

    platform = Column(String, nullable=False)
    external_product_id = Column(String, nullable=False)

    seller_sku = Column(String, index=True, nullable=False)

    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    commission_rate = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)
    status = Column(String, default="active")

    product = relationship("Product", back_populates="listings")