import uuid
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import Base
from app.utils.enums import UpdateMethod


def update_table(
    db: Session,
    row_identifier: int,
    update_model: BaseModel,
    schema: Base,
    return_schema: Base,
    method: str,
):
    row = db.query(schema).get(row_identifier)
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
