from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base

MenuMenuPosition = Table(
    "menu_menu_position",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menu.id", ondelete="CASCADE")),
    Column(
        "menu_position_id", Integer, ForeignKey("menu_position.id", ondelete="CASCADE")
    ),
)


class MenuPosition(Base):
    __tablename__ = "menu_position"
    __table_args__ = (UniqueConstraint("name", name="uq_menu_position_name"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    preparation_time = Column(Integer, nullable=False)
    is_vegan = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    menus = relationship(
        "Menu",
        secondary=MenuMenuPosition,
        back_populates="positions",
        cascade="all, delete",
    )


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = (UniqueConstraint("name", name="uq_menu_name"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    positions = relationship(
        "MenuPosition",
        secondary=MenuMenuPosition,
        back_populates="menus",
        cascade="all, delete",
    )
