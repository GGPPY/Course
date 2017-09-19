"""empty message

Revision ID: b3b2b3faa8d4
Revises: 8d1ee027e6cf
Create Date: 2017-09-19 20:17:30.898000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b2b3faa8d4'
down_revision = '8d1ee027e6cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('subject_id', sa.Integer(), nullable=False))
    op.drop_constraint(u'course_type_id_fkey', 'course', type_='foreignkey')
    op.create_foreign_key(None, 'course', 'subject', ['subject_id'], ['id'])
    op.drop_column('course', 'course_url')
    op.drop_column('course', 'image_path')
    op.drop_column('course', 'type_id')
    op.add_column('subject', sa.Column('image_path', sa.String(), nullable=True))
    op.add_column('subject', sa.Column('subject_url', sa.String(), nullable=True))
    op.drop_column('subject', 'subject_image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subject', sa.Column('subject_image', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('subject', 'subject_url')
    op.drop_column('subject', 'image_path')
    op.add_column('course', sa.Column('type_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('course', sa.Column('image_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('course_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.create_foreign_key(u'course_type_id_fkey', 'course', 'subject', ['type_id'], ['id'])
    op.drop_column('course', 'subject_id')
    # ### end Alembic commands ###
