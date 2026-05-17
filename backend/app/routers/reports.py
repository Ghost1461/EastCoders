from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.report_service import (
    get_dashboard_report_service,
    get_ai_report_summary_service,
    get_ai_recommendations_service,
    get_ai_stock_analysis_service,
    get_ai_review_analysis_service,
    get_ai_period_summary_service
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/dashboard")
def get_dashboard_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_report_service(
        db=db,
        current_user=current_user
    )

#genel hesap summary'si
@router.get("/ai-summary")
def get_ai_report_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_report_summary_service(
        db=db,
        current_user=current_user
    )


@router.get("/ai-recommendations")
def get_ai_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_recommendations_service(
        db=db,
        current_user=current_user
    )


@router.get("/ai-stock-analysis")
def get_ai_stock_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_stock_analysis_service(
        db=db,
        current_user=current_user
    )


@router.get("/ai-review-analysis")
def get_ai_review_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_review_analysis_service(
        db=db,
        current_user=current_user
    )


#period bazlı hesap summary'si
@router.get("/ai/period-summary")
def ai_period_summary(
    period: str,
    value: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_period_summary_service(
        db=db,
        current_user=current_user,
        period=period,
        value=value
    )