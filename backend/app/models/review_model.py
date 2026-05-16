from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    review_id = Column(String, nullable=False, index=True)

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    source_user_id = Column(String, nullable=False, index=True)

    platform = Column(String, nullable=False, index=True)

    external_order_id = Column(String, nullable=False, index=True)

    customer_id = Column(String, nullable=True)

    internal_product_id = Column(String, nullable=True)

    #review'de listing doğrulamasını DB relationship ile değil, service içinde OrderItem kontrolüyle sağlanıyor
    listing_id = Column(String, nullable=False, index=True)

    rating = Column(Integer, nullable=False)

    comment = Column(String, nullable=True)

    sentiment = Column(String, nullable=True)

    topic = Column(String, nullable=True)

    created_at = Column(String, nullable=False)
