"""Added preciounidad

Revision ID: 8ba15da9c804
Revises: 
Create Date: 2017-10-20 17:14:55.403351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ba15da9c804'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('producto', sa.Column('preciounidad', sa.String(8)))


def downgrade():
    op.drop_column('producto', 'preciounidad')
