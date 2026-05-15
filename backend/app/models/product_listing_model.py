from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProductListing(Base):
    __tablename__ = "product_listings"

    listing_id = Column(String, primary_key=True, index=True)

    internal_product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)#kendi db'mizdeki user id
    source_user_id = Column(String, nullable=True)#Platformdan gelen, o platformun user id'i


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
    user = relationship("User", back_populates="listings")