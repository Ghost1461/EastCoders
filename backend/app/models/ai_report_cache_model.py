from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint

from app.core.database import Base



TR_TIMEZONE = timezone(timedelta(hours=3))


def now_tr():
    return datetime.now(TR_TIMEZONE)



class AiReportCache(Base):
    __tablename__ = "ai_report_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, nullable=False)
    report_type = Column(String, nullable=False)
    input_hash = Column(String, nullable=False)

    ai_response = Column(Text, nullable=False)

    created_at = Column(
    DateTime(timezone=True),
    default=now_tr
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "report_type",
            "input_hash",
            name="uq_ai_report_cache_user_type_hash"
        ),
    )