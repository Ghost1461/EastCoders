from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime


class RawTrendResponse(BaseModel):
    id: int
    trend_name: str
    source: str
    category: Optional[str]
    platform: Optional[str]
    image_url: Optional[str]
    extra_data: Optional[Any]
    created_at: datetime
    updated_at: Optional[datetime]


class MarketTrendResponse(BaseModel):
    id: int
    trend_key: str
    trend_name: str
    trend_type: str
    source: str

    category: Optional[str]
    platform: Optional[str]

    marketplace_signal: float
    sales_growth: float
    review_growth: float
    rating_signal: float
    stock_signal: float
    news_signal: float
    trend_score: float

    image_url: Optional[str]
    extra_data: Optional[Any]

    explanation: Optional[str]

    created_at: datetime
    updated_at: Optional[datetime]


class MatchedProductResponse(BaseModel):
    listing_id: str
    product_id: int
    product_name: str

    brand: Optional[str]
    category: Optional[str]
    color: Optional[str]
    size: Optional[str]

    platform: Optional[str]
    seller_sku: Optional[str]

    price: Optional[float]
    stock: Optional[int]
    rating: Optional[float]
    review_count: Optional[int]
    status: Optional[str]


class PersonalizedTrendResponse(BaseModel):
    trend: MarketTrendResponse
    matched_products: List[MatchedProductResponse]