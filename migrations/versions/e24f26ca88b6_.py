"""empty message

Revision ID: e24f26ca88b6
Revises: bcced4cef354
Create Date: 2021-09-12 00:11:35.392770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e24f26ca88b6'
down_revision = 'bcced4cef354'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('FCs', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('departure_point', sa.String(length=40), nullable=False),
    sa.Column('arrival_point', sa.String(length=40), nullable=False),
    sa.Column('order_type', sa.String(length=15), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('password_name', sa.VARCHAR(length=120), nullable=False),
    sa.Column('date_added', sa.DATETIME(), nullable=False),
    sa.Column('password_content', sa.VARCHAR(length=120), nullable=False),
    sa.Column('creator', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['creator'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('password_name')
    )
    op.drop_table('order')
    # ### end Alembic commands ###
