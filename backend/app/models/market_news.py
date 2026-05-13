from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class MarketNews(Base):
    __tablename__ = "market_news"

    news_id = Column(String, primary_key=True, index=True)

    title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)

    summary = Column(String, nullable=True)
    source = Column(String, nullable=True)
    url = Column(String, nullable=True, unique=True)

    published_at = Column(DateTime, nullable=True)
    language = Column(String, default="tr")

    category = Column(String, nullable=True)
    related_tags = Column(JSON, default=[])

    impact_level = Column(String, default="medium")