from datetime import datetime, timedelta
from http import HTTPStatus

import requests
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db import Base, get_session_constructor
from app.models.mail_pool import MailPool
from app.models.user import User
from app.settings import Settings
from app.utils.enums import LoggingLevel
from app.utils.logger import get_logger, setup_logger
from init_data.init_schemas import MENU_POSITIONS, MENUS, USERS

setup_logger(LoggingLevel.DEBUG)
logger = get_logger("main")


def generate_token() -> str:
    r = requests.post(
        "http://localhost:8000/token", data={"username": "admin", "password": "string"}
    )
    return r.json()["access_token"]


def get_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {generate_token()}"}


class InitDataSettings(Settings):
    change_pool_dates: bool = True


def create_object(endpoint: str, obj: BaseModel) -> None:
    r = requests.post(
        f"http://localhost:8000{endpoint}", json=obj.dict(), headers=get_headers()
    )
    if r.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
        logger.error(r.json())


def create_menu_positions() -> None:
    for position in MENU_POSITIONS:
        create_object("/api/admin/menu/menu_position", position)


def create_menus() -> None:
    for menu in MENUS:
        create_object("/api/admin/menu", menu)


def create_users(db: Session) -> None:
    for user in USERS:
        db.add(user)
    db.commit()


def create_dummy_data(db: Session) -> None:
    create_users(db)
    create_menu_positions()
    create_menus()


def change_few_pool_dates_to_yesterday(db: Session) -> None:
    yesterday = datetime.now() - timedelta(days=1)
    db.query(MailPool).filter(MailPool.id % 5 == 0).update({"date": yesterday})
    db.query(MailPool).filter(MailPool.id % 10 == 0).update(
        {"date": yesterday, "updated": True}
    )
    db.commit()


def clear_tables(database_dsn: str, db: Session) -> None:
    engine = create_engine(database_dsn)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db.query(User).delete()


if __name__ == "__main__":
    """
    This function creates dummy data for development purposes. It should be removed before production.
    """

    settings = InitDataSettings()
    session_maker = get_session_constructor(settings.database)
    with session_maker() as db:
        clear_tables(settings.database.get_secret_value(), db)
        create_dummy_data(db)
        if settings.change_pool_dates:
            change_few_pool_dates_to_yesterday(db)
