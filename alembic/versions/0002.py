"""Add user table

Revision ID: 0002
Revises: 0001
Create Date: 2024-03-08 15:24:30.232272

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True, index=True, nullable=False),
        sa.Column("login", sa.String(255), nullable=False),
        sa.Column("password", sa.String(1024), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("login", name="uq_login"),
    )


def downgrade() -> None:
    op.drop_table("user")
