"""phase_2_google_platform_meta

Revision ID: a3f2b1c4e5d6
Revises: f883ccb34a09
Create Date: 2026-09-06 22:15:00.000000+00:00

"""

from typing import Union
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3f2b1c4e5d6"
down_revision: Union[str, Sequence[str], None] = "f883ccb34a09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("platform_connections") as batch_op:
        batch_op.add_column(sa.Column("platform_meta", sa.JSON(), nullable=False, server_default="{}"))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("platform_connections") as batch_op:
        batch_op.drop_column("platform_meta")
