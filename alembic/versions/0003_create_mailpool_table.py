"""Create MailPool table

Revision ID: 0003
Revises: 0002
Create Date: 2024-03-10 12:29:18.929531

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "mail_pool",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "position_id",
            sa.Integer(),
            sa.ForeignKey("menu_position.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("date", sa.Date(), nullable=False, index=True),
        sa.Column("updated", sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("position_id", "date", name="uq_menu_position_id"),
    )


def downgrade() -> None:
    op.drop_table("mail_pool")
