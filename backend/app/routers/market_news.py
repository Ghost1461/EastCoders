from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import MarketNews
from app.services.news_api_service import fetch_and_store_market_news

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

@router.get("/")
def dashboard_home():
    return {"message": "news çalışıyor"}

@router.post("/fetch")
def fetch_market_news(db: Session = Depends(get_db)):
    return fetch_and_store_market_news(db)


@router.get("/display_market_news")
def get_market_news(db: Session = Depends(get_db)):
    return db.query(MarketNews).order_by(
        MarketNews.published_at.desc()
    ).all()