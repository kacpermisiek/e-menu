from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.utils.vars import MAX_INT_64


class MenuPositionSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0, le=MAX_INT_64)
    description: str
    preparation_time: int = Field(..., gt=0, le=MAX_INT_64)
    is_vegan: bool = False

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        from_orm = True


class MenuPositionCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: int = Field(..., gt=0, le=MAX_INT_64)
    is_vegan: bool = Field(False)


class MenuPositionUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: int = Field(..., gt=0, le=MAX_INT_64)
    is_vegan: bool = Field(...)


class MenuPositionPatchSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: Optional[int] = Field(None, gt=0, le=MAX_INT_64)
    is_vegan: Optional[bool] = Field(None)


class MenuPositionResponseSchema(BaseModel):
    id: int
    name: str
    price: float
    description: str
    preparation_time: int
    is_vegan: bool = False

    created_at: datetime
    updated_at: datetime


class MenuSchema(BaseModel):
    id: int
    name: str
    positions: list[MenuPositionSchema]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        from_orm = True


class MenuCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    positions: Optional[list[MenuPositionSchema]] = []
