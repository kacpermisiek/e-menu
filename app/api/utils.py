import datetime
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import Base
from app.models.mail_pool import MailPool
from app.models.menu import Menu, MenuPosition
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


def add_row_to_table(db: Session, row: Base) -> Base:
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Object already exists")
    return row


def create_mail_pool_position(db: Session, position_id: int, updated: bool) -> None:
    mail_pool = MailPool(
        position_id=position_id, date=datetime.date.today(), updated=updated
    )
    try:
        db.add(mail_pool)
        db.commit()
        print("\n\nMail pool position added\n\n")
    except IntegrityError as e:
        print("\n\nMail pool position already exists\n\n")
        print(str(e))
        db.rollback()
