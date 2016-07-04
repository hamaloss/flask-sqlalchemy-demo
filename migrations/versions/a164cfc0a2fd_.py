"""empty message

Revision ID: a164cfc0a2fd
Revises: 14e30b58c2b7
Create Date: 2016-07-04 16:50:29.082740

"""

# revision identifiers, used by Alembic.
revision = 'a164cfc0a2fd'
down_revision = '14e30b58c2b7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('items', 'productId', existing_type=sa.Integer(), type_=sa.String(100))


def downgrade():
    op.alter_column('items', 'productId', existing_type=sa.String(100), type_=sa.Integer())
