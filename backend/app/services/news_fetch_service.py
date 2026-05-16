import feedparser
from sqlalchemy.orm import Session

from app.core.news_sources import NEWS_SOURCES
from app.models.news_model import News
from app.models.user_model import User
from app.models.news_notification_model import NewsNotification

from app.services.news_normlizer import normalize_rss_item
from app.services.news_filter_service import (
    is_clothing_related,
    is_commerce_related
)
from app.services.news_scraping_service import (
    scrape_ticaret_bakanligi
)


class NewsFetchService:

    def fetch_and_store_news(self, db: Session, category: str):
        if category not in NEWS_SOURCES:
            raise ValueError("Geçersiz haber kategorisi.")

        created_news = 0
        skipped_news = 0
        created_notifications = 0

        sources = NEWS_SOURCES[category]

        for source in sources:

            if source["type"] == "rss":
                feed = feedparser.parse(source["url"])

                for item in feed.entries:
                    normalized_news = normalize_rss_item(
                        item=item,
                        source_name=source["name"],
                        category=category
                    )

                    result = self._store_single_news(
                        db=db,
                        normalized_news=normalized_news,
                        category=category
                    )

                    if result["created"]:
                        created_news += 1
                        created_notifications += result["notifications"]
                    else:
                        skipped_news += 1

            elif source["type"] == "scraping":
                scraped_news = self._scrape_source(source)

                for normalized_news in scraped_news:
                    result = self._store_single_news(
                        db=db,
                        normalized_news=normalized_news,
                        category=category
                    )

                    if result["created"]:
                        created_news += 1
                        created_notifications += result["notifications"]
                    else:
                        skipped_news += 1

        db.commit()

        return {
            "message": "Haberler başarıyla çekildi.",
            "category": category,
            "created_news": created_news,
            "skipped_news": skipped_news,
            "created_notifications": created_notifications
        }

    def _store_single_news(
        self,
        db: Session,
        normalized_news: dict | None,
        category: str
    ):
        if normalized_news is None:
            return {"created": False, "notifications": 0}

        if not normalized_news.get("url"):
            return {"created": False, "notifications": 0}

        if not self._is_valid_news(
            normalized_news=normalized_news,
            category=category
        ):
            return {"created": False, "notifications": 0}

        if self._news_exists(db, normalized_news["url"]):
            return {"created": False, "notifications": 0}

        news = News(**normalized_news)

        db.add(news)
        db.flush()

        notification_count = self._create_notifications_for_news(
            db=db,
            news=news
        )

        return {
            "created": True,
            "notifications": notification_count
        }

    def _create_notifications_for_news(
        self,
        db: Session,
        news: News
    ) -> int:
        news_date = news.published_at or news.created_at

        if not news_date:
            return 0

        users = (
            db.query(User)
            .filter(User.created_at <= news_date)
            .all()
        )

        count = 0

        for user in users:
            existing_notification = (
                db.query(NewsNotification)
                .filter(
                    NewsNotification.user_id == user.id,
                    NewsNotification.news_id == news.id
                )
                .first()
            )

            if existing_notification:
                continue

            notification = NewsNotification(
                user_id=user.id,
                news_id=news.id,
                is_read=False
            )

            db.add(notification)
            count += 1

        return count

    def _scrape_source(self, source: dict):
        if source["name"] == "Ticaret Bakanlığı Duyurular":
            return scrape_ticaret_bakanligi()

        return []

    def _is_valid_news(self, normalized_news: dict, category: str) -> bool:
        if category == "fashion":
            return is_clothing_related(
                normalized_news["title"],
                normalized_news["description"]
            )

        if category == "commerce_finance":
            return is_commerce_related(
                normalized_news["title"],
                normalized_news["description"]
            )

        return True

    def _news_exists(self, db: Session, url: str) -> bool:
        return (
            db.query(News)
            .filter(News.url == url)
            .first()
            is not None
        )