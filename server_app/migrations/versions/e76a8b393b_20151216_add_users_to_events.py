"""Add users to events

Revision ID: e76a8b393b
Revises: 174869c6926
Create Date: 2015-12-16 17:43:42.696568

"""

# revision identifiers, used by Alembic.
revision = 'e76a8b393b'
down_revision = '174869c6926'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_users',
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events_users')
    ### end Alembic commands ###
