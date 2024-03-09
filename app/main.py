from fastapi import FastAPI

from app.api import menu
from app.settings import settings
from app.utils.logger import get_logger, setup_logger

setup_logger(settings.log_level)
logger = get_logger("main")
logger.info("Starting application")

app = FastAPI(
    title="eMenu",
    version=settings.version,
)


app.include_router(menu.public, prefix="/api/menu", tags=["Menu"])
app.include_router(menu.admin, prefix="/api/admin/menu", tags=["Menu"])
