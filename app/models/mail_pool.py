from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, UniqueConstraint

from app.db import Base


class MailPool(Base):
    __tablename__ = "mail_pool"
    __table_args__ = (
        UniqueConstraint("position_id", "date", name="uq_menu_position_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_id = Column(
        Integer,
        ForeignKey("menu_position.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    date = Column(Date, nullable=False, index=True)
    updated = Column(Boolean, default=False, nullable=False)
