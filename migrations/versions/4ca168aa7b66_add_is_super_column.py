"""Add is_super column

Revision ID: 4ca168aa7b66
Revises: 5feaef0f4863
Create Date: 2024-11-27 15:58:16.729184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ca168aa7b66'
down_revision: Union[str, None] = '5feaef0f4863'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('title', sa.String(), nullable=False))
    op.add_column('pictures', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('pictures', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'pictures', ['user_id'])
    op.create_foreign_key(None, 'pictures', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('is_super', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_super')
    op.drop_constraint(None, 'pictures', type_='foreignkey')
    op.drop_constraint(None, 'pictures', type_='unique')
    op.drop_column('pictures', 'is_active')
    op.drop_column('pictures', 'user_id')
    op.drop_column('pictures', 'title')
    # ### end Alembic commands ###
