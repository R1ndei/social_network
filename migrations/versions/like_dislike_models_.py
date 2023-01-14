"""empty message

Revision ID: like_dislike_models
Revises: 3_photo_model
Create Date: 2023-01-13 18:38:02.119022

"""
from alembic import op
import sqlalchemy as sa



revision = 'like_dislike_models'
down_revision = '3_photo_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('dislikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], name='fk_dislikes_posts_id_post', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_dislikes_users_id_user', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], name='fk_likes_posts_id_post', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_likes_users_id_user', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('photos', sa.Column('uploaded_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('posts', 'likes',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('posts', 'dislikes',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('posts', 'dislikes',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('posts', 'likes',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    op.drop_column('photos', 'uploaded_at')
    op.drop_table('likes')
    op.drop_table('dislikes')
