"""empty message

Revision ID: c49ade389f59
Revises: 9d90a2369720
Create Date: 2025-01-15 13:46:40.300151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c49ade389f59'
down_revision: Union[str, None] = '9d90a2369720'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('viewed_images', 'correct')
    op.drop_column('viewed_images', 'used_in_game')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('viewed_images', sa.Column('used_in_game', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('viewed_images', sa.Column('correct', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###