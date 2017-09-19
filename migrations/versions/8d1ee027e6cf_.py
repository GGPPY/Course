"""empty message

Revision ID: 8d1ee027e6cf
Revises: 125c70f0cf52
Create Date: 2017-09-19 20:04:27.962000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d1ee027e6cf'
down_revision = '125c70f0cf52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subject', sa.Column('subject_image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subject', 'subject_image')
    # ### end Alembic commands ###