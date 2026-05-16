from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.routers import router
from app.core.database import (
    Base,
    engine,
    SessionLocal
)

from app import models

from app.services.news_fetch_service import NewsFetchService


app = FastAPI(
    title="EastCoders API",
    version="1.0.0"
)

app.include_router(router)

Base.metadata.create_all(bind=engine)


scheduler = BackgroundScheduler()


def fetch_news_job():
    db = SessionLocal()

    try:
        service = NewsFetchService()

        service.fetch_and_store_news(
            db=db,
            category="fashion"
        )

        service.fetch_and_store_news(
            db=db,
            category="commerce_finance"
        )

        print("AUTO NEWS FETCH COMPLETED")

    except Exception as e:
        print("AUTO NEWS FETCH ERROR:", e)

    finally:
        db.close()


@app.on_event("startup")
def start_scheduler():

    scheduler.add_job(
        fetch_news_job,
        "interval",
        hours=3
    )

    scheduler.start()

    print("NEWS SCHEDULER STARTED")


@app.get("/")
def home():
    return {"message": "API çalışıyor"}