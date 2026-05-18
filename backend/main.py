import asyncio

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.routers import router
from app.core.database import Base, engine, SessionLocal
from app import models
from fastapi.middleware.cors import CORSMiddleware

from app.services.trend_service import generate_market_trends_for_system


app = FastAPI(
    title="EastCoders API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()


def scheduled_market_trend_job():
    db = SessionLocal()

    try:
        asyncio.run(generate_market_trends_for_system(db=db))
        print("Daily market trend update completed.")
    except Exception as e:
        print("Daily market trend update failed:", e)
    finally:
        db.close()


@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(
        scheduled_market_trend_job,
        "interval",
        hours=24,
        id="daily_market_trend_update",
        replace_existing=True
    )

    scheduler.start()
    print("Trend scheduler started.")


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


@app.get("/")
def home():
    return {"message": "API çalışıyor"}