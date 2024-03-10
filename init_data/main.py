from http import HTTPStatus

import requests

from app.utils.enums import LoggingLevel
from app.utils.logger import get_logger, setup_logger
from init_data.init_schemas import MENU_POSITIONS, MENUS

setup_logger(LoggingLevel.DEBUG)
logger = get_logger("main")


def create_object(endpoint, obj):
    r = requests.post(f"http://localhost:8000{endpoint}", json=obj.dict())
    if r.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
        logger.error(r.json())


def create_menu_positions():
    for position in MENU_POSITIONS:
        create_object("/api/admin/menu/menu_position", position)


def create_menus():
    for menu in MENUS:
        create_object("/api/admin/menu", menu)


def create_dummy_data() -> None:
    """This function creates dummy data for development purposes. It should be removed before production."""
    create_menu_positions()
    create_menus()


if __name__ == "__main__":
    create_dummy_data()
