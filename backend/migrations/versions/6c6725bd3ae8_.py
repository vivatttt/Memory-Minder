"""empty message

Revision ID: 6c6725bd3ae8
Revises: 
Create Date: 2025-01-16 20:44:09.201572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6c6725bd3ae8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('key', sa.TEXT(), nullable=False),
    sa.Column('name_image', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__images'))
    )
    op.create_table('names_memory_stats',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('played_at', sa.DATE(), nullable=False),
    sa.Column('correct_answers', sa.INTEGER(), nullable=False),
    sa.Column('wrong_answers', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__names_memory_stats'))
    )
    op.create_table('users',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), nullable=True),
    sa.Column('username', sa.TEXT(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users'))
    )
    op.create_table('viewed_images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('image_id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__viewed_images'))
    )
    op.create_table('false_state_stats',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('played_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('won', sa.BOOLEAN(), nullable=True),
    sa.Column('level', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__false_state_stats__user_id__users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__false_state_stats'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('false_state_stats')
    op.drop_table('viewed_images')
    op.drop_table('users')
    op.drop_table('names_memory_stats')
    op.drop_table('images')
    # ### end Alembic commands ###