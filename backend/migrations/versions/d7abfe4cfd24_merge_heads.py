"""Merge heads

Revision ID: d7abfe4cfd24
Revises: 378f199289d0, 9755a19c4228
Create Date: 2025-01-12 22:55:21.030072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7abfe4cfd24'
down_revision: Union[str, None] = ('378f199289d0', '9755a19c4228')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
