from datetime import datetime
from enum import Enum
from typing import Any, Optional

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from app.models.menu import Menu, MenuPosition
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


def validate_menus_type(menus: list[Any]) -> list[int] | list[Menu]:
    if not all([isinstance(menu, int) or isinstance(menu, Menu) for menu in menus]):
        raise ValueError("Invalid type for menus. Should be list of integers(ids)")
    return menus


class MenuPositionCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: int = Field(..., gt=0, le=MAX_INT_64)
    is_vegan: bool = Field(False)
    menus: list[Any] = Field([])

    @field_validator("menus")
    def validate_menus_type(cls, value: list[Any]) -> list[int] | list[Menu]:
        return validate_menus_type(menus=value)


class MenuPositionUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: int = Field(..., gt=0, le=MAX_INT_64)
    is_vegan: bool = Field(...)
    menus: list[Any] = Field(...)

    @field_validator("menus")
    def validate_menus_type(cls, value: list[Any]) -> list[int] | list[Menu]:
        return validate_menus_type(menus=value)


class MenuPositionPatchSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0, le=MAX_INT_64)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    preparation_time: Optional[int] = Field(None, gt=0, le=MAX_INT_64)
    is_vegan: Optional[bool] = Field(None)
    menus: Optional[list[Any]] = Field(None)

    @field_validator("menus")
    def validate_menus_type(cls, value: Optional[list[Any]]) -> list[int] | list[Menu]:
        return value if value is None else validate_menus_type(menus=value)


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


def validate_menu_positions_type(
    positions: list[Any],
) -> list[int] | list[MenuPosition]:
    if not all(
        [
            isinstance(position, int) or isinstance(position, MenuPosition)
            for position in positions
        ]
    ):
        raise ValueError("Invalid type for positions. Should be list of integers(ids)")
    return positions


class MenuCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    positions: Optional[list[Any]] = []

    @field_validator("positions")
    def validate_positions_type(
        cls, value: Optional[list[Any]]
    ) -> list[int] | list[Menu]:
        return value if value is None else validate_menu_positions_type(positions=value)


class MenuPatchSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    positions: Optional[list[Any]] = []

    @field_validator("positions")
    def validate_positions_type(
        cls, value: Optional[list[Any]]
    ) -> list[int] | list[Menu]:
        return value if value is None else validate_menu_positions_type(positions=value)


class MenuUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    positions: list[Any]

    @field_validator("positions")
    def validate_positions_type(cls, value: list[Any]) -> list[int] | list[Menu]:
        return validate_menu_positions_type(positions=value)


class SortParameter(str, Enum):
    NAME = "name"
    POSITIONS_COUNT = "positions_count"


class MenusQuerySchema(BaseModel):
    sortby: SortParameter = Query(
        SortParameter.NAME,
        description="Available sort parameters: 'name', 'positions_count'",
    )
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=255,
        description="Menu name filter, for example: 'basic_menu'",
    )
    created_before: Optional[datetime] = Query(
        None, description="Created before some date, for example: '2022-01-01T00:00:00'"
    )
    created_after: Optional[datetime] = Query(
        None, description="Created after some date, for example: '2022-01-01T00:00:00'"
    )
    updated_before: Optional[datetime] = Query(
        None, description="Updated before some date, for example: '2022-01-01T00:00:00'"
    )
    updated_after: Optional[datetime] = Query(
        None, description="Updated after some date, for example: '2022-01-01T00:00:00'"
    )
