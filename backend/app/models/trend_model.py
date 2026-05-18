from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime

from app.core.database import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)

    trend_key = Column(String, index=True, nullable=False)
    trend_name = Column(String, nullable=False)

    trend_type = Column(String, nullable=False)
    source = Column(String, nullable=False)

    category = Column(String, nullable=True)
    platform = Column(String, nullable=True)

    marketplace_signal = Column(Float, default=0)
    sales_growth = Column(Float, default=0)
    review_growth = Column(Float, default=0)
    rating_signal = Column(Float, default=0)
    stock_signal = Column(Float, default=0)
    news_signal = Column(Float, default=0)

    trend_score = Column(Float, default=0)

    image_url = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)

    explanation = Column(String, nullable=True)
  #  suggestion = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)