"""empty message

Revision ID: 2f2182e74ca9
Revises: 6603fb54e778
Create Date: 2018-08-21 07:04:05.334588

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2f2182e74ca9'
down_revision = '6603fb54e778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reserve_infos', sa.Column('date_day', sa.String(length=64), nullable=True))
    op.add_column('reserve_infos', sa.Column('date_month', sa.String(length=64), nullable=True))
    op.add_column('reserve_infos', sa.Column('date_year', sa.String(length=64), nullable=True))
    op.drop_column('reserve_infos', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reserve_infos', sa.Column('date', mysql.VARCHAR(length=64), nullable=True))
    op.drop_column('reserve_infos', 'date_year')
    op.drop_column('reserve_infos', 'date_month')
    op.drop_column('reserve_infos', 'date_day')
    # ### end Alembic commands ###
