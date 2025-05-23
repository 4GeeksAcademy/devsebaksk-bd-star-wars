"""empty message

Revision ID: 0b6a648591ba
Revises: c742cdf9cfe2
Create Date: 2025-03-31 15:47:02.592765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b6a648591ba'
down_revision = 'c742cdf9cfe2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_user', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'planets', ['favorites_user'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorites_user')

    # ### end Alembic commands ###
