from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.connected_account_model import ConnectedAccount
from app.models.review_model import Review

#sürekli aynı şeyi tekrar etmemek için
def serialize_review(review: Review):
    return {
        "id": review.id,
        "review_id": review.review_id,
        "owner_user_id": review.owner_user_id,
        "source_user_id": review.source_user_id,
        "platform": review.platform,
        "external_order_id": review.external_order_id,
        "customer_id": review.customer_id,
        "external_product_id": review.external_product_id,
        "listing_id": review.listing_id,
        "rating": review.rating,
        "comment": review.comment,
        "sentiment": review.sentiment,
        "topic": review.topic,
        "created_at": review.created_at
    }


def base_review_query(db: Session, current_user):
    return (
        db.query(Review)
        .join(
            ConnectedAccount,
            and_(
                ConnectedAccount.owner_user_id == Review.owner_user_id,
                ConnectedAccount.platform == Review.platform,
                ConnectedAccount.source_user_id == Review.source_user_id,
                ConnectedAccount.is_active == True
            )
        )
        .filter(Review.owner_user_id == current_user.id)
    )


def get_all_reviews_service(db: Session, current_user):
    reviews = (
        base_review_query(db, current_user)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_platform_service(platform_key: str, db: Session, current_user):
    platform_key = platform_key.lower()

    reviews = (
        base_review_query(db, current_user)
        .filter(Review.platform == platform_key)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "platform": platform_key,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_customer_service(customer_id: str, db: Session, current_user):
    reviews = (
        base_review_query(db, current_user)
        .filter(Review.customer_id == customer_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "customer_id": customer_id,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_listing_service(listing_id: str, db: Session, current_user):
    reviews = (
        base_review_query(db, current_user)
        .filter(Review.listing_id == listing_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "listing_id": listing_id,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_product_service(
    external_product_id: str,
    db: Session,
    current_user
):
    reviews = (
        base_review_query(db, current_user)
        .filter(Review.external_product_id == external_product_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "external_product_id": external_product_id,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_rating_service(rating: int, db: Session, current_user):
    reviews = (
        base_review_query(db, current_user)
        .filter(Review.rating == rating)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "rating": rating,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_sentiment_service(sentiment: str, db: Session, current_user):
    sentiment = sentiment.lower()

    reviews = (
        base_review_query(db, current_user)
        .filter(func.lower(Review.sentiment) == sentiment)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "sentiment": sentiment,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_reviews_by_topic_service(topic: str, db: Session, current_user):
    topic = topic.lower()

    reviews = (
        base_review_query(db, current_user)
        .filter(func.lower(Review.topic) == topic)
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "topic": topic,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def search_reviews_by_comment_service(q: str, db: Session, current_user):
    reviews = (
        base_review_query(db, current_user)
        .filter(Review.comment.ilike(f"%{q}%"))
        .order_by(Review.created_at.desc())
        .all()
    )

    return {
        "query": q,
        "total": len(reviews),
        "reviews": [serialize_review(review) for review in reviews]
    }


def get_review_summary_service(db: Session, current_user):
    base_query = base_review_query(db, current_user)

    total_reviews = base_query.count()

    average_rating = (
        base_query.with_entities(
            func.coalesce(func.avg(Review.rating), 0)
        )
        .scalar()
    )

    positive_count = base_query.filter(
        func.lower(Review.sentiment) == "positive"
    ).count()

    negative_count = base_query.filter(
        func.lower(Review.sentiment) == "negative"
    ).count()

    mixed_count = base_query.filter(
        func.lower(Review.sentiment) == "mixed"
    ).count()

    topic_results = (
        base_query.with_entities(
            Review.topic,
            func.count(Review.id).label("count")
        )
        .filter(Review.topic.isnot(None))
        .group_by(Review.topic)
        .order_by(func.count(Review.id).desc())
        .limit(5)
        .all()
    )

    most_common_topics = [
        {
            "topic": topic,
            "count": count
        }
        for topic, count in topic_results
    ]

    return {
        "total_reviews": total_reviews,
        "average_rating": round(float(average_rating), 2),
        "positive_count": positive_count,
        "negative_count": negative_count,
        "mixed_count": mixed_count,
        "most_common_topics": most_common_topics
    }


def get_rating_distribution_service(db: Session, current_user):
    results = (
        base_review_query(db, current_user)
        .with_entities(
            Review.rating,
            func.count(Review.id).label("count")
        )
        .group_by(Review.rating)
        .order_by(Review.rating.desc())
        .all()
    )

    distribution_map = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    for rating, count in results:
        distribution_map[rating] = count

    return {
        "rating_distribution": [
            {
                "rating": rating,
                "count": count
            }
            for rating, count in distribution_map.items()
        ]
    }


def get_topic_summary_service(db: Session, current_user):
    results = (
        base_review_query(db, current_user)
        .with_entities(
            Review.topic,
            func.count(Review.id).label("review_count"),
            func.coalesce(func.avg(Review.rating), 0).label("average_rating")
        )
        .filter(Review.topic.isnot(None))
        .group_by(Review.topic)
        .order_by(func.count(Review.id).desc())
        .all()
    )

    return {
        "total_topics": len(results),
        "topics": [
            {
                "topic": topic,
                "review_count": review_count,
                "average_rating": round(float(average_rating), 2)
            }
            for topic, review_count, average_rating in results
        ]
    }