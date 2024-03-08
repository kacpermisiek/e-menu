from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MenuPositionSchema(BaseModel):
    name: str
    price: float
    description: str
    preparation_time: int
    is_vegan: bool = False

    created_at: datetime
    updated_at: datetime


class MenuSchema(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    positions: list[MenuPositionSchema]

    created_at: datetime
    updated_at: datetime
