"""empty message

Revision ID: 72db2240bf5d
Revises: b809df36a5b3
Create Date: 2021-02-25 23:44:29.017073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72db2240bf5d'
down_revision = 'b809df36a5b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('People')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('People',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"People_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('catchphrase', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='People_pkey')
    )
    # ### end Alembic commands ###