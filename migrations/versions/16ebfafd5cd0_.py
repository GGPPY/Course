"""empty message

Revision ID: 16ebfafd5cd0
Revises: 972a0e50bdd5
Create Date: 2017-08-25 10:36:59.232000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16ebfafd5cd0'
down_revision = '972a0e50bdd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('action', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menus_permissions',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], )
    )
    op.drop_column(u'menu', 'action')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'menu', sa.Column('action', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.drop_table('menus_permissions')
    op.drop_table('permission')
    # ### end Alembic commands ###