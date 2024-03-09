"""Init

Revision ID: 0001
Revises: 
Create Date: 2024-03-08 15:03:42.718113

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "menu_position",
        sa.Column("id", UUID, primary_key=True, index=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("preparation_time", sa.Integer, nullable=False),
        sa.Column("is_vegan", sa.Boolean, server_default="false"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "menu",
        sa.Column("id", UUID, primary_key=True, index=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("name", name="uq_menu_name"),
    )

    op.create_table(
        "menu_menu_position",
        sa.Column("menu_id", UUID, sa.ForeignKey("menu.id"), nullable=False),
        sa.Column(
            "menu_position_id", UUID, sa.ForeignKey("menu_position.id"), nullable=False
        ),
        sa.PrimaryKeyConstraint("menu_id", "menu_position_id"),
    )


def downgrade() -> None:
    op.drop_table("menu")
    op.drop_table("menu_position")
