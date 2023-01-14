"""empty message

Revision ID: 2_posts_model
Revises: 1_users_model
Create Date: 2023-01-13 11:19:23.898091

"""
from alembic import op
import sqlalchemy as sa



revision = '2_posts_model'
down_revision = '1_users_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('head', sa.String(length=100), nullable=False),
    sa.Column('main_text', sa.Text(), nullable=False),
    sa.Column('creator', sa.Integer(), nullable=False),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('dislikes', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator'], ['users.id'], name='fk_posts_users_id_creator', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('posts')
