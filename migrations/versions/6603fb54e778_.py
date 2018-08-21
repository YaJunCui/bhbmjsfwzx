"""empty message

Revision ID: 6603fb54e778
Revises: 765531343d2a
Create Date: 2018-08-21 06:42:46.174424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6603fb54e778'
down_revision = '765531343d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserve_infos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department', sa.String(length=64), nullable=True),
    sa.Column('approver', sa.String(length=64), nullable=True),
    sa.Column('sender', sa.String(length=64), nullable=True),
    sa.Column('telephone', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('time_interval', sa.String(length=64), nullable=True),
    sa.Column('remarks', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reserve_infos_department'), 'reserve_infos', ['department'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reserve_infos_department'), table_name='reserve_infos')
    op.drop_table('reserve_infos')
    # ### end Alembic commands ###