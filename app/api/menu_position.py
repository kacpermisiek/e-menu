from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import create_mail_pool_position, update_table
from app.models.menu import Menu, MenuPosition
from app.schemas.menu import (
    MenuPositionCreateSchema,
    MenuPositionPatchSchema,
    MenuPositionSchema,
    MenuPositionUpdateSchema,
)
from app.utils.enums import UpdateMethod

admin = APIRouter(dependencies=[Depends(OAuth2PasswordBearer(tokenUrl="token"))])


@admin.post("/", response_model=MenuPositionSchema, status_code=HTTPStatus.CREATED)
def create_menu_position(
    menu_position: MenuPositionCreateSchema, db: Session = Depends(get_db())
):

    if menu_position.menus is not None:
        menus = db.query(Menu).filter(Menu.id.in_(menu_position.menus)).all()
    else:
        menus = []

    position = MenuPosition(
        name=menu_position.name,
        price=menu_position.price,
        description=menu_position.description,
        preparation_time=menu_position.preparation_time,
        is_vegan=menu_position.is_vegan,
        menus=menus,
    )
    try:
        db.add(position)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Position already exists")

    create_mail_pool_position(
        db,
        position.id,
        updated=False,
    )
    return position


@admin.get("/", response_model=List[MenuPositionSchema])
def get_menu_positions(db: Session = Depends(get_db())):
    return db.query(MenuPosition).all()


@admin.get("/{menu_position_id}", response_model=MenuPositionSchema)
def get_menu_position(menu_position_id: int, db: Session = Depends(get_db())):
    menu_position = db.get(MenuPosition, menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    return menu_position


@admin.patch("/{menu_position_id}", response_model=MenuPositionSchema)
def patch_menu_position(
    menu_position_id: int,
    menu_position_update: MenuPositionPatchSchema,
    db: Session = Depends(get_db()),
):
    if menu_position_update.menus is not None:
        menus = db.query(Menu).filter(Menu.id.in_(menu_position_update.menus)).all()
    else:
        menus = None

    model = MenuPositionPatchSchema(
        name=menu_position_update.name,
        price=menu_position_update.price,
        description=menu_position_update.description,
        preparation_time=menu_position_update.preparation_time,
        is_vegan=menu_position_update.is_vegan,
        menus=menus,
    )

    create_mail_pool_position(
        db,
        menu_position_id,
        updated=False,
    )

    return update_table(
        db=db,
        row_identifier=menu_position_id,
        update_model=model,
        schema=MenuPosition,
        return_schema=MenuPositionSchema,
        method=UpdateMethod.PATCH,
    )


@admin.put("/{menu_position_id}", response_model=MenuPositionSchema)
def update_menu_position(
    menu_position_id: int,
    menu_position_update: MenuPositionUpdateSchema,
    db: Session = Depends(get_db()),
):
    model = MenuPositionUpdateSchema(
        name=menu_position_update.name,
        price=menu_position_update.price,
        description=menu_position_update.description,
        preparation_time=menu_position_update.preparation_time,
        is_vegan=menu_position_update.is_vegan,
        menus=db.query(Menu).filter(Menu.id.in_(menu_position_update.menus)).all(),
    )

    create_mail_pool_position(
        db,
        menu_position_id,
        updated=False,
    )

    return update_table(
        db=db,
        row_identifier=menu_position_id,
        update_model=model,
        schema=MenuPosition,
        return_schema=MenuPositionSchema,
        method=UpdateMethod.PUT,
    )


@admin.delete("/{menu_position_id}", response_model=MenuPositionSchema)
def delete_menu_position(menu_position_id: int, db: Session = Depends(get_db())):
    menu_position = db.get(MenuPosition, menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    for menu in menu_position.menus:
        menu.positions.remove(menu_position)

    db.delete(menu_position)
    db.commit()

    return menu_position
