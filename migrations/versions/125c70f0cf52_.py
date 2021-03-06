"""empty message

Revision ID: 125c70f0cf52
Revises: 59c1474da284
Create Date: 2017-09-19 19:57:37.307000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '125c70f0cf52'
down_revision = '59c1474da284'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('sort', sa.Integer(), nullable=True),
    sa.Column('route', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('action', sa.String(length=250), nullable=True),
    sa.Column('hex', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('create_user', sa.String(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_user', sa.String(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('create_user', sa.Integer(), nullable=True),
    sa.Column('modify_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('start_time', sa.Date(), nullable=True),
    sa.Column('end_time', sa.Date(), nullable=True),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('course_url', sa.String(), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('create_user', sa.String(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_user', sa.String(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menus_permissions',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], )
    )
    op.create_table('roles_menus',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], )
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('wx', sa.String(), nullable=True),
    sa.Column('wx_name', sa.String(), nullable=True),
    sa.Column('qq', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('base', sa.Boolean(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('card_image_front', sa.String(), nullable=True),
    sa.Column('card_image_back', sa.String(), nullable=True),
    sa.Column('pay_image', sa.String(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('update_user', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.drop_table('roles_users')
    op.drop_table('roles_menus')
    op.drop_table('menus_permissions')
    op.drop_table('course')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('menu')
    # ### end Alembic commands ###
