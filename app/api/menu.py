from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.api.utils import get_menu_and_position, menu_contains_position, update_table
from app.models.menu import Menu, MenuPosition
from app.schemas.menu import (
    MenuCreateSchema,
    MenuPositionCreateSchema,
    MenuPositionPatchSchema,
    MenuPositionSchema,
    MenuPositionUpdateSchema,
    MenuSchema,
    MenusQuerySchema,
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
    db_menu_position = MenuPosition(**menu_position.dict())
    db.add(db_menu_position)
    db.commit()
    return db_menu_position


@admin.get("/menu_position", response_model=List[MenuPositionSchema])
def get_menu_positions(db: Session = Depends(get_db())):
    return db.query(MenuPosition).all()


@admin.get("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def get_menu_position(menu_position_id: int, db: Session = Depends(get_db())):
    menu_position = db.get(MenuPosition, menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    return menu_position


@admin.patch("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
def patch_menu_position(
    menu_position_id: int,
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
    menu_position_id: int,
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
def delete_menu_position(menu_position_id: int, db: Session = Depends(get_db())):
    menu_position = db.get(MenuPosition, menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")

    for menu in menu_position.menus:
        menu.positions.remove(menu_position)

    db.delete(menu_position)
    db.commit()
    return menu_position


@public.get("/", response_model=List[MenuSchema])
def get_menus(query: MenusQuerySchema = Depends(), db: Session = Depends(get_db())):
    results = db.query(Menu).order_by(query.sortby)
    if query.name:
        results = results.filter(func.lower(Menu.name).like(f"%{query.name.lower()}%"))

    if query.created_before:
        results = results.filter(Menu.created_at <= query.created_before)

    if query.created_after:
        results = results.filter(Menu.created_at >= query.created_after)

    if query.updated_before:
        results = results.filter(Menu.updated_at <= query.updated_before)

    if query.updated_after:
        results = results.filter(Menu.updated_at >= query.updated_after)

    return results.order_by(query.sortby).all()


@public.get("/{menu_id}", response_model=MenuSchema)
def get_menu(menu_id: int, db: Session = Depends(get_db())):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    return menu


@admin.post("/", response_model=MenuSchema, status_code=HTTPStatus.CREATED)
def create_menu(menu: MenuCreateSchema, db: Session = Depends(get_db())):
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    return db_menu


@admin.patch("/{menu_id}", response_model=MenuSchema)
def patch_menu(
    menu_id: int,
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
    menu_id: int,
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
def delete_menu(menu_id: int, db: Session = Depends(get_db())):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(menu)
    db.commit()
    return menu


@admin.post("/{menu_id}/add_position/{menu_position_id}", response_model=MenuSchema)
def add_position_to_menu(
    menu_id: int,
    menu_position_id: int,
    db: Session = Depends(get_db()),
):
    menu, menu_position = get_menu_and_position(db, menu_id, menu_position_id)

    if menu_contains_position(db, menu_id, menu_position_id):
        raise HTTPException(
            status_code=400, detail="Menu and position connection already exists"
        )

    menu.positions.append(menu_position)
    db.commit()
    return menu


@admin.post("/{menu_id}/remove_position/{menu_position_id}", response_model=MenuSchema)
def remove_position_from_menu(
    menu_id: int,
    menu_position_id: int,
    db: Session = Depends(get_db()),
):
    menu, menu_position = get_menu_and_position(db, menu_id, menu_position_id)

    if not menu_contains_position(db, menu_id, menu_position_id):
        raise HTTPException(
            status_code=400, detail="Menu and position connection does not exist"
        )

    menu.positions.remove(menu_position)
    db.commit()
    return menu
