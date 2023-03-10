"""empty message

Revision ID: 1_users_model
Revises: 
Create Date: 2023-01-13 11:18:15.421675

"""
from alembic import op
import sqlalchemy as sa



revision = '1_users_model'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('mid_name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_super_user', sa.Boolean(), nullable=False),
    sa.Column('is_verified_email', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )


def downgrade() -> None:
    op.drop_table('users')
