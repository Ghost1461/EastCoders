from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.schemas.trend_schema import (
    MarketTrendResponse,
    RawTrendResponse,
    PersonalizedTrendResponse
)

from app.schemas.trend_ai_schema import (
    TrendAISummaryResponse,
)

from app.services.trend_service import (
    generate_market_trends_for_system,
    get_all_trends,
    get_market_trends,
    get_personalized_market_trends,
    get_raw_trends
)

from app.services.trend_ai_service import (
    generate_trends_ai_summary
)


router = APIRouter(
    prefix="/trends",
    tags=["Trends"]
)


@router.post("/generate/market")
async def generate_market_trends_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await generate_market_trends_for_system(
        db=db
    )


@router.get("/raw", response_model=list[RawTrendResponse])
def list_raw_trends(
    limit: int = Query(default=40, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_raw_trends(
        db=db,
        limit=limit
    )


@router.get("/", response_model=list[MarketTrendResponse])
def list_all_trends(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_trends(
        db=db,
        limit=limit
    )


@router.get("/market", response_model=list[MarketTrendResponse])
def list_market_trends(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_market_trends(
        db=db,
        limit=limit
    )

@router.get("/personalized", response_model=list[PersonalizedTrendResponse])
def list_personalized_market_trends(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_personalized_market_trends(
        db=db,
        limit=limit
    )

@router.post("/ai-summary", response_model=TrendAISummaryResponse)
def generate_trends_ai_summary_route(
    limit: int = Query(default=20, ge=1, le=50),
    force_refresh: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return generate_trends_ai_summary(
        db=db,
        current_user=current_user,
        limit=limit,
        force_refresh=force_refresh
    )