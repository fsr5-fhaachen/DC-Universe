"""create speechlist table

Revision ID: b9daf1607bde
Revises: 0e38febe8725
Create Date: 2020-10-24 14:57:33.763676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9daf1607bde'
down_revision = '0e38febe8725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('speechlists',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.BigInteger(), nullable=False),
    sa.Column('member_id', sa.BigInteger(), nullable=False),
    sa.Column('member_name', sa.String(length=255), nullable=True),
    sa.Column('prio', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('speechlists')
    # ### end Alembic commands ###
