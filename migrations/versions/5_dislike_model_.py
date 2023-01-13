"""empty message

Revision ID: 5_dislike_model
Revises: 4_like_model
Create Date: 2023-01-13 11:21:09.698029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5_dislike_model'
down_revision = '4_like_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dislikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], name='fk_dislikes_posts_id_post', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['posts.id'], name='fk_dislikes_posts_id_user', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dislikes')
    # ### end Alembic commands ###
