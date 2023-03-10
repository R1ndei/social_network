"""empty message

Revision ID: 3_photo_model
Revises: 2_posts_model
Create Date: 2023-01-13 11:19:53.091206

"""
from alembic import op
import sqlalchemy as sa



revision = '3_photo_model'
down_revision = '2_posts_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('uploader', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], name='fk_photos_posts_id_post', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uploader'], ['users.id'], name='fk_photos_users_id_uploader', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('photos')
