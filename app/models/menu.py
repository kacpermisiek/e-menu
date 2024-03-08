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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

menu_menu_position = Table(
    "menu_menu_position",
    Base.metadata,
    Column("menu_id", UUID, ForeignKey("menu.id")),
    Column("menu_position_id", UUID, ForeignKey("menu_position.id")),
)


class MenuPosition(Base):
    __tablename__ = "menu_position"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    preparation_time = Column(Integer, nullable=False)
    is_vegan = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    menus = relationship(
        "Menu", secondary=menu_menu_position, back_populates="positions"
    )


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = (UniqueConstraint("name", name="uq_menu_name"),)

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    positions = relationship(
        "MenuPosition", secondary=menu_menu_position, back_populates="menus"
    )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
