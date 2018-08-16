"""empty message

Revision ID: 1613b73ff48e
Revises: 0ce12b3ded68
Create Date: 2018-08-16 22:50:15.498645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1613b73ff48e'
down_revision = '0ce12b3ded68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
