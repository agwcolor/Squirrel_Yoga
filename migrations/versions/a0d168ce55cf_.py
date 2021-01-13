"""empty message

Revision ID: a0d168ce55cf
Revises: 1a0a98eca7f9
Create Date: 2021-01-12 00:13:15.075624

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a0d168ce55cf'
down_revision = '1a0a98eca7f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Event', 'tree')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Event', sa.Column('tree', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
