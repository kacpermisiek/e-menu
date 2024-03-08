import requests
from sqlalchemy.orm import Session

from tests.utils import given_menus


def test_list_menu_items(db_api: Session):
    given_menus(db_api)
