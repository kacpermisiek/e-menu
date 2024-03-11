from sqlalchemy import Column, DateTime, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("login", name="uq_login"),)

    id = Column(UUID, primary_key=True, index=True)
    login = Column(String(255), nullable=False)
    password = Column(String(1024), nullable=False)
    email = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
