from fastapi import APIRouter

from app.routers.products_import import router as products_import_router
from app.routers.trends import router as trends_router
from app.routers.reviews_import import router as reviews_import_router
from app.routers.review_display import router as review_display_router
from app.routers.reports import router as reports_router
from app.routers.alerts import router as alerts_router
from app.routers.integrations import router as integrations_router
from app.routers.authentication import router as authentication_router
from app.routers.market_news import market_news_router
from app.routers.news_notifications import router as news_notifications_router
from app.routers.product_display import router as products_display_router
from app.routers.order_import import router as order_import_router
from app.routers.order_display import router as order_display_router
from app.routers.connected_account import router as connected_account
from app.routers.profile import router as profile
from app.routers.sync import router as sync_router
from app.routers.admin import router as admin_router


from app.routers.trends import router as trends_router


router = APIRouter()

router.include_router(products_import_router)
router.include_router(trends_router)
router.include_router(reviews_import_router)
router.include_router(review_display_router)
router.include_router(reports_router)
router.include_router(alerts_router)
router.include_router(integrations_router)
router.include_router(authentication_router)
router.include_router(market_news_router)
router.include_router(products_display_router)
router.include_router(order_display_router)
router.include_router(order_import_router)
router.include_router(connected_account)
router.include_router(profile)
router.include_router(sync_router)
router.include_router(news_notifications_router)
router.include_router(trends_router)
router.include_router(admin_router)