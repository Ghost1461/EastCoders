from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.review_display_service import (
    get_all_reviews_service,
    get_reviews_by_platform_service,
    get_reviews_by_customer_service,
    get_reviews_by_listing_service,
    get_reviews_by_product_service,
    get_reviews_by_rating_service,
    get_reviews_by_sentiment_service,
    get_reviews_by_topic_service,
    search_reviews_by_comment_service,
    get_review_summary_service,
    get_rating_distribution_service,
    get_topic_summary_service,
)


router = APIRouter(
    prefix="/review_display",
    tags=["Review_Display"]
)


@router.get("/")
def dashboard_home():
    return {"message": "review çalışıyor"}


#Tüm reviewlarları çek
@router.get("/all")
def get_all_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_reviews_service(
        db=db,
        current_user=current_user
    )

#Platforma göre reviewları çek
@router.get("/platform/{platform_key}")
def get_reviews_by_platform(
    platform_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_platform_service(
        platform_key=platform_key,
        db=db,
        current_user=current_user
    )

#Bir customer'ın reviewlarını çek
@router.get("/customer/{customer_id}")
def get_reviews_by_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_customer_service(
        customer_id=customer_id,
        db=db,
        current_user=current_user
    )

#Bir listing için reviewlar.
@router.get("/listing/{listing_id}")
def get_reviews_by_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_listing_service(
        listing_id=listing_id,
        db=db,
        current_user=current_user
    )

#Bir ürün için reviewlar.
@router.get("/product/{internal_product_id}")
def get_reviews_by_product(
    internal_product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_product_service(
        internal_product_id=internal_product_id,
        db=db,
        current_user=current_user
    )

#1-5 rating’e göre filtre.
@router.get("/rating/{rating}")
def get_reviews_by_rating(
    rating: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_rating_service(
        rating=rating,
        db=db,
        current_user=current_user
    )

#positive, negative, mixed gibi sentiment verisine göre filtrele
@router.get("/sentiment/{sentiment}")
def get_reviews_by_sentiment(
    sentiment: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_sentiment_service(
        sentiment=sentiment,
        db=db,
        current_user=current_user
    )

#quality, color, shipping, price gibi konuya göre filtreleme
@router.get("/topic/{topic}")
def get_reviews_by_topic(
    topic: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_reviews_by_topic_service(
        topic=topic,
        db=db,
        current_user=current_user
    )

#Comment içinde arama.
@router.get("/search/comment")
def search_reviews_by_comment(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_reviews_by_comment_service(
        q=q,
        db=db,
        current_user=current_user
    )

#Rapor için: total_reviews, average_rating, positive_count, negative_count, mixed_count, most_common_topics gibi summary
@router.get("/summary")
def get_review_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_review_summary_service(
        db=db,
        current_user=current_user
    )

#5 yıldız kaç tane, 4 yıldız kaç tane gibi chart verisi.
@router.get("/rating-distribution")
def get_rating_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_rating_distribution_service(
        db=db,
        current_user=current_user
    )

#Topic bazlı adet + average rating.
@router.get("/topic-summary")
def get_topic_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_topic_summary_service(
        db=db,
        current_user=current_user
    )