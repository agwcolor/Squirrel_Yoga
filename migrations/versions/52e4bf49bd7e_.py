"""empty message

Revision ID: 52e4bf49bd7e
Revises: 
Create Date: 2021-01-13 18:21:30.751223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52e4bf49bd7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Event', sa.Column('tree_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Event', 'Tree', ['tree_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Event', type_='foreignkey')
    op.drop_column('Event', 'tree_id')
    # ### end Alembic commands ###
