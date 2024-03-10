from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app.api import menu
from app.settings import settings
from app.utils.logger import get_logger, setup_logger
from app.utils.mail_utils import just_clear_mail_pool, send_mail

setup_logger(settings.log_level)
logger = get_logger("main")
logger.info("Starting application")

app = FastAPI(
    title="eMenu",
    version=settings.version,
)

app.include_router(menu.public, prefix="/api/menu", tags=["Menu"])
app.include_router(menu.admin, prefix="/api/admin/menu", tags=["Menu"])


async def send_daily_mail():
    if settings.smtp_enabled:
        logger.info("Creating daily mail")
        send_mail()
    else:
        just_clear_mail_pool()


scheduler = AsyncIOScheduler()

scheduler.add_job(send_daily_mail, "interval", seconds=5)
scheduler.start()
