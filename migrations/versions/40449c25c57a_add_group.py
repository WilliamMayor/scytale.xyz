"""Add group

Revision ID: 40449c25c57a
Revises:
Create Date: 2016-01-02 17:00:45.926927

"""

# revision identifiers, used by Alembic.
revision = '40449c25c57a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # commands auto generated by Alembic - please adjust!
    op.create_table(
        'group',
        sa.Column('gid', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('password', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('gid'),
        sa.UniqueConstraint('name'))
    # end Alembic commands


def downgrade():
    # commands auto generated by Alembic - please adjust! ###
    op.drop_table('group')
    # end Alembic commands ###
