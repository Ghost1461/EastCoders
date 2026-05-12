from fastapi import APIRouter

from app.routers.products import router as products_router
from app.routers.dashboard import router as dashboard_router
from app.routers.trends import router as trends_router
from app.routers.reviews import router as reviews_router
from app.routers.reports import router as reports_router
from app.routers.alerts import router as alerts_router
from app.routers.integrations import router as integrations_router
from app.routers.authentication import router as authentication_router
from app.routers.market_news import router as market_news_router

router = APIRouter()

router.include_router(products_router)
router.include_router(dashboard_router)
router.include_router(trends_router)
router.include_router(reviews_router)
router.include_router(reports_router)
router.include_router(alerts_router)
router.include_router(integrations_router)
router.include_router(authentication_router)
router.include_router(market_news_router)