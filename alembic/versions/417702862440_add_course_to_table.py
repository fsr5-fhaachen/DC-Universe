"""add course to table

Revision ID: 417702862440
Revises: 0e38febe8725
Create Date: 2020-10-20 17:44:11.333951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '417702862440'
down_revision = '0e38febe8725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groupphase_users', sa.Column('course', sa.String(length=255), nullable=True))
    op.add_column('groups', sa.Column('course', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'course')
    op.drop_column('groupphase_users', 'course')
    # ### end Alembic commands ###
