import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import Base
from app.models.menu import Menu, MenuMenuPosition, MenuPosition
from app.utils.enums import UpdateMethod


def update_table(
    db: Session,
    row_identifier: int,
    update_model: BaseModel,
    schema: Base,
    return_schema: Base,
    method: str,
):
    row = db.get(schema, row_identifier)
    if row is None:
        raise HTTPException(status_code=404, detail="Object not found")

    if method == UpdateMethod.PATCH:
        update_data = update_model.dict(exclude_unset=True, exclude_none=True)
    else:
        update_data = update_model.dict(exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(row, key):
            setattr(row, key, value)

    db.add(row)
    db.commit()
    return return_schema.from_orm(row)


def menu_contains_position(db: Session, menu_id: int, position_id: int):
    query = db.get(Menu, menu_id)

    for position in query.positions:
        if position.id == position_id:
            return True

    return False


def get_menu_and_position(db, menu_id, menu_position_id):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu_position = db.get(MenuPosition, menu_position_id)
    if menu_position is None:
        raise HTTPException(status_code=404, detail="Menu position not found")
    return menu, menu_position
