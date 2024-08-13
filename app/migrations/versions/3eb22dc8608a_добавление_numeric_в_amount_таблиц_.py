"""Добавление numeric в amount таблиц банка расходов и доходов

Revision ID: 3eb22dc8608a
Revises: 5beeee0f76da
Create Date: 2024-08-13 15:33:04.339436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eb22dc8608a'
down_revision: Union[str, None] = '5beeee0f76da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('incomes_bank', 'amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.alter_column('spendings_bank', 'amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('spendings_bank', 'amount',
               existing_type=sa.Numeric(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    op.alter_column('incomes_bank', 'amount',
               existing_type=sa.Numeric(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    # ### end Alembic commands ###
