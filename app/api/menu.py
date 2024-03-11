from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import (
    add_row_to_table,
    create_mail_pool_position,
    get_menu_and_position,
    menu_contains_position,
    update_table,
)
from app.models.menu import Menu, MenuPosition
from app.schemas.menu import (
    MenuCreateSchema,
    MenuPatchSchema,
    MenuPositionCreateSchema,
    MenuPositionPatchSchema,
    MenuPositionSchema,
    MenuPositionUpdateSchema,
    MenuSchema,
    MenusQuerySchema,
    MenuUpdateSchema,
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


@admin.put("/menu_position/{menu_position_id}", response_model=MenuPositionSchema)
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
    if menu.positions is not None:
        positions = (
            db.query(MenuPosition).filter(MenuPosition.id.in_(menu.positions)).all()
        )
    else:
        positions = []

    return add_row_to_table(db, Menu(name=menu.name, positions=positions))


@admin.patch("/{menu_id}", response_model=MenuSchema)
def patch_menu(
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
def update_menu(
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
