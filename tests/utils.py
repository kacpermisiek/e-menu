from sqlalchemy.orm import Session

from app.models.menu import Menu, MenuPosition


def given_menus(db_api: Session):
    menu_position = MenuPosition(
        name="Test Menu Position",
        description="Test Menu Position Description",
        price=10.0,
        preparation_time=10,
    )

    menu = Menu(
        name="Test Menu",
        description="Test Menu Description",
        price=10.0,
    )
