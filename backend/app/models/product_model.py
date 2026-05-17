from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=True)
    gender= Column(String, nullable=True)
    color = Column(String, nullable=True)
    size = Column(String, nullable=True)

    tags = Column(JSON, default=[])

    listings = relationship("ProductListing", back_populates="product", cascade="all, delete-orphan")
    
    image_url=Column(String, nullable=True)
    last_updated=Column(String, nullable=True)