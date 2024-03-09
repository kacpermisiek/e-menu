import uuid

import pytest

from app.models.menu import MenuPosition, Menu


@pytest.fixture
def hundred_menu_positions(db_api, json_basic_menu_position):
    for i in range(100):
        json_basic_menu_position["name"] = json_basic_menu_position["name"] + str(i)
        db_api.add(MenuPosition(**json_basic_menu_position))
    db_api.commit()


@pytest.fixture
def hundred_menus(db_api, json_basic_menu):
    for i in range(100):
        json_basic_menu["name"] = json_basic_menu["name"] + str(i)
        db_api.add(Menu(**json_basic_menu))
    db_api.commit()
