from http import HTTPStatus

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import update_table
from app.models.menu import Menu, MenuPosition
from app.schemas.menu import (
    MenuPositionCreateSchema,
    MenuPositionPatchSchema,
    MenuPositionSchema,
    MenuPositionUpdateSchema,
    MenuSchema,
    MenuCreateSchema,
)
from app.utils.enums import UpdateMethod

admin = APIRouter()
public = APIRouter()


@admin.post(
    "/menu_position", response_model=MenuPositionSchema, status_code=HTTPStatus.CREATED
)
def create_menu_position(
    menu_position: MenuPositionCreateSchema, db: Session = Depends(get_db())
):
    db_menu_position = MenuPosition(**menu_position.dict() | {"id": uuid.uuid4()})
    db.add(db_menu_position)
    db.commit()
    return db_menu_position


@admin.get("/menu_position", response_model=List[MenuPositionSchema])
def get_menu_positions(db: Session = Depends(get_db())):
    return db.query(MenuPosition).all()


@admin.get("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def get_menu_position(menu_position_id: uuid.UUID, db: Session = Depends(get_db())):
    menu_position = db.query(MenuPosition).get(menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    return menu_position


@admin.patch("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def patch_menu_position(
    menu_position_id: uuid.UUID,
    menu_position_update: MenuPositionPatchSchema,
    db: Session = Depends(get_db()),
):
    return update_table(
        db=db,
        row_identifier=menu_position_id,
        update_model=menu_position_update,
        schema=MenuPosition,
        return_schema=MenuPositionSchema,
        method=UpdateMethod.PATCH,
    )


@admin.put("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def update_menu_position(
    menu_position_id: uuid.UUID,
    menu_position_update: MenuPositionUpdateSchema,
    db: Session = Depends(get_db()),
):
    return update_table(
        db=db,
        row_identifier=menu_position_id,
        update_model=menu_position_update,
        schema=MenuPosition,
        return_schema=MenuPositionSchema,
        method=UpdateMethod.PUT,
    )


@admin.delete("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def delete_menu_position(menu_position_id: uuid.UUID, db: Session = Depends(get_db())):
    menu_position = db.query(MenuPosition).get(menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    db.delete(menu_position)
    db.commit()
    return menu_position


@public.get("/", response_model=List[MenuSchema])
def get_menus(db: Session = Depends(get_db())):
    return db.query(Menu).all()


@public.get("/{menu_id}", response_model=MenuSchema)
def get_menu(menu_id: uuid.UUID, db: Session = Depends(get_db())):
    menu = db.query(Menu).get(menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    return menu


@admin.post("/", response_model=MenuSchema, status_code=HTTPStatus.CREATED)
def create_menu(menu: MenuCreateSchema, db: Session = Depends(get_db())):
    db_menu = Menu(**menu.dict() | {"id": uuid.uuid4()})
    db.add(db_menu)
    db.commit()
    return db_menu


@admin.patch("/{menu_id}", response_model=MenuSchema)
def patch_menu(
    menu_id: uuid.UUID,
    menu_update: MenuCreateSchema,
    db: Session = Depends(get_db()),
):
    return update_table(
        db=db,
        row_identifier=menu_id,
        update_model=menu_update,
        schema=Menu,
        return_schema=MenuSchema,
        method=UpdateMethod.PATCH,
    )


@admin.put("/{menu_id}", response_model=MenuSchema)
def update_menu(
    menu_id: uuid.UUID,
    menu_update: MenuCreateSchema,
    db: Session = Depends(get_db()),
):
    return update_table(
        db=db,
        row_identifier=menu_id,
        update_model=menu_update,
        schema=Menu,
        return_schema=MenuSchema,
        method=UpdateMethod.PUT,
    )


@admin.delete("/{menu_id}", response_model=MenuSchema)
def delete_menu(menu_id: uuid.UUID, db: Session = Depends(get_db())):
    menu = db.query(Menu).get(menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(menu)
    db.commit()
    return menu
