from typing import Annotated

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api import menu, menu_position, user
from app.api.deps import get_db
from app.api.utils import authenticate_user, create_access_token
from app.schemas.other import Token
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
app.include_router(
    menu_position.admin, prefix="/api/admin/menu_position", tags=["Menu Position"]
)
app.include_router(user.admin, prefix="/api/admin/user", tags=["User"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/token", include_in_schema=False)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db()),
):
    user = authenticate_user(db, pwd_context, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.login})
    return Token(access_token=access_token, token_type="bearer")


async def send_daily_mail():
    if settings.smtp_enabled:
        logger.info("Creating daily mail")
        send_mail()
    else:
        logger.info("SMTP is disabled, clearing mail pool")
        just_clear_mail_pool()


scheduler = AsyncIOScheduler()
scheduler.configure(timezone=settings.scheduler_timezone)

scheduler.add_job(send_daily_mail, "cron", hour=10)
scheduler.start()
