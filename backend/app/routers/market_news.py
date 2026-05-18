from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.news_model import News
from app.schemas.news import NewsResponse, NewsDetailResponse
from app.services.news_fetch_service import NewsFetchService

market_news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@market_news_router.get("/", response_model=list[NewsResponse])
def get_news(
    category: str = Query(..., description="fashion veya commerce_finance"),
    db: Session = Depends(get_db)
):
    if category not in ["fashion", "commerce_finance"]:
        raise HTTPException(
            status_code=400,
            detail="category sadece 'fashion' veya 'commerce_finance' olabilir."
        )

    news = (
        db.query(News)
        .filter(News.category == category)
        .order_by(News.published_at.desc().nullslast())
        .all()
    )

    return news

@market_news_router.get("/fashion", response_model=list[NewsResponse])
def get_fashion_news(db: Session = Depends(get_db)):
    return (
        db.query(News)
        .filter(News.category == "fashion")
        .order_by(News.published_at.desc().nullslast())
        .all()
    )


@market_news_router.get("/commerce-finance", response_model=list[NewsResponse])
def get_commerce_finance_news(db: Session = Depends(get_db)):
    return (
        db.query(News)
        .filter(News.category == "commerce_finance")
        .order_by(News.published_at.desc().nullslast())
        .all()
    )

@market_news_router.get("/{news_id}", response_model=NewsDetailResponse)
def get_news_detail(
    news_id: int,
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="Haber bulunamadı.")

    return news

@market_news_router.post("/fashion/fetch")
def fetch_fashion_news(db: Session = Depends(get_db)):
    service = NewsFetchService()

    return service.fetch_and_store_news(
        db=db,
        category="fashion"
    )


@market_news_router.post("/commerce-finance/fetch")
def fetch_commerce_finance_news(db: Session = Depends(get_db)):
    service = NewsFetchService()

    return service.fetch_and_store_news(
        db=db,
        category="commerce_finance"
    )
