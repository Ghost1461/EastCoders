from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from datetime import datetime

from app.core.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)

    source = Column(String(100), nullable=True)
    url = Column(Text, nullable=False, unique=True)

    category = Column(String(50), nullable=False)
    # fashion veya commerce_finance

    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("url", name="uq_news_url"),
    )
