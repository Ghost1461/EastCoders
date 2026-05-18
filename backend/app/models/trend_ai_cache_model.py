from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime

from app.core.database import Base


class TrendAISummaryCache(Base):
    __tablename__ = "trend_ai_summary_cache"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    summary_type = Column(String, default="trend_page")
    summary = Column(String, nullable=False)
    cache_date = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "summary_type",
            "cache_date",
            name="uq_user_daily_trend_summary"
        ),
    )