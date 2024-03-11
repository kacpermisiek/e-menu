from app.schemas.menu import MenuCreateSchema, MenuPositionCreateSchema
from app.schemas.user import UserCreateSchema

"""
Paste here some emails for test of sending mails
"""
USERS = [
    UserCreateSchema(
        login="admin",
        email="elo.cotam@wp.pl",
        password="admin",
    ),
    UserCreateSchema(
        login="user",
        email="kacpermisiek1@gmail.com",
        password="user",
    ),
]

MENU_POSITIONS = [
    MenuPositionCreateSchema(
        name="Pizza",
        price=10.0,
        description="test_description",
        preparation_time=10,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Pasta",
        price=15.0,
        description="test_description",
        preparation_time=15,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Salad",
        price=5.0,
        description="test_description",
        preparation_time=5,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Soup",
        price=7.0,
        description="test_description",
        preparation_time=7,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Cake",
        price=20.0,
        description="test_description",
        preparation_time=20,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Coffee",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Tea",
        price=2.0,
        description="test_description",
        preparation_time=2,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Beer",
        price=4.0,
        description="test_description",
        preparation_time=4,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Wine",
        price=6.0,
        description="test_description",
        preparation_time=6,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Water",
        price=1.0,
        description="test_description",
        preparation_time=1,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Juice",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Milk",
        price=2.0,
        description="test_description",
        preparation_time=2,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Bread",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Butter",
        price=2.0,
        description="test_description",
        preparation_time=2,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Cheese",
        price=4.0,
        description="test_description",
        preparation_time=4,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Ham",
        price=5.0,
        description="test_description",
        preparation_time=5,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Eggs",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Bacon",
        price=4.0,
        description="test_description",
        preparation_time=4,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Sausage",
        price=5.0,
        description="test_description",
        preparation_time=5,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Chicken",
        price=6.0,
        description="test_description",
        preparation_time=6,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Beef",
        price=7.0,
        description="test_description",
        preparation_time=7,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Pork",
        price=8.0,
        description="test_description",
        preparation_time=8,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Fish",
        price=9.0,
        description="test_description",
        preparation_time=9,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Fries",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Rice",
        price=2.0,
        description="test_description",
        preparation_time=2,
        is_vegan=True,
    ),
    MenuPositionCreateSchema(
        name="Pancakes",
        price=5.0,
        description="test_description",
        preparation_time=5,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Waffles",
        price=6.0,
        description="test_description",
        preparation_time=6,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Ice Cream",
        price=4.0,
        description="test_description",
        preparation_time=4,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Yogurt",
        price=3.0,
        description="test_description",
        preparation_time=3,
        is_vegan=False,
    ),
    MenuPositionCreateSchema(
        name="Cereal",
        price=2.0,
        description="test_description",
        preparation_time=2,
        is_vegan=False,
    ),
]

MENUS = [
    MenuCreateSchema(
        name="Menu 1",
        positions=[x for x in range(1, len(MENU_POSITIONS), 2)],
    ),
    MenuCreateSchema(
        name="Menu 2",
        positions=[x for x in range(0, len(MENU_POSITIONS) - 1, 2)],
    ),
    MenuCreateSchema(
        name="Menu 3",
        positions=[0, len(MENU_POSITIONS) - 1],
    ),
]