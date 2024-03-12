from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import (
    add_row_to_table,
    get_menu_and_position,
    menu_contains_position,
    update_table,
)
from app.models.menu import Menu, MenuPosition
from app.schemas.menu import (
    MenuCreateSchema,
    MenuPatchSchema,
    MenuSchema,
    MenusQuerySchema,
    MenuUpdateSchema,
)
from app.utils.enums import UpdateMethod

admin = APIRouter(dependencies=[Depends(OAuth2PasswordBearer(tokenUrl="token"))])
public = APIRouter()


@public.get("/", response_model=List[MenuSchema])
async def get_menus(
    query: MenusQuerySchema = Depends(), db: Session = Depends(get_db())
):
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
async def get_menu(menu_id: int, db: Session = Depends(get_db())):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    return menu


@admin.post("/", response_model=MenuSchema, status_code=HTTPStatus.CREATED)
async def create_menu(menu: MenuCreateSchema, db: Session = Depends(get_db())):
    if menu.positions is not None:
        positions = (
            db.query(MenuPosition).filter(MenuPosition.id.in_(menu.positions)).all()
        )
    else:
        positions = []

    return add_row_to_table(db, Menu(name=menu.name, positions=positions))


@admin.patch("/{menu_id}", response_model=MenuSchema)
async def patch_menu(
    menu_id: int,
    menu_update: MenuPatchSchema,
    db: Session = Depends(get_db()),
):
    if menu_update.positions is not None:
        positions = (
            db.query(MenuPosition)
            .filter(MenuPosition.id.in_(menu_update.positions))
            .all()
        )
    else:
        positions = None
    model = MenuUpdateSchema(
        name=menu_update.name,
        positions=positions,
    )
    return update_table(
        db=db,
        row_identifier=menu_id,
        update_model=model,
        schema=Menu,
        return_schema=MenuSchema,
        method=UpdateMethod.PATCH,
    )


@admin.put("/{menu_id}", response_model=MenuSchema)
async def update_menu(
    menu_id: int,
    menu_update: MenuUpdateSchema,
    db: Session = Depends(get_db()),
):
    model = MenuPatchSchema(
        name=menu_update.name,
        positions=db.query(MenuPosition)
        .filter(MenuPosition.id.in_(menu_update.positions))
        .all(),
    )
    return update_table(
        db=db,
        row_identifier=menu_id,
        update_model=model,
        schema=Menu,
        return_schema=MenuSchema,
        method=UpdateMethod.PUT,
    )


@admin.delete("/{menu_id}", response_model=MenuSchema)
async def delete_menu(menu_id: int, db: Session = Depends(get_db())):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(menu)
    db.commit()
    return menu


@admin.post("/{menu_id}/add_position/{menu_position_id}", response_model=MenuSchema)
async def add_position_to_menu(
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
async def remove_position_from_menu(
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
