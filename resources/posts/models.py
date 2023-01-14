import datetime

import ormar

from config.db_config import MainMetaDB
from core.utils import moscow_time
from resources.users.models import User


class Post(ormar.Model):
    class Meta(MainMetaDB):
        tablename = "posts"

    id: int = ormar.Integer(primary_key=True, nullable=False)
    head: str = ormar.String(max_length=100)
    main_text: str = ormar.Text()
    creator: User = ormar.ForeignKey(
        User,
        nullable=False,
        related_name="user_post",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    likes: int = ormar.Integer(default=0)
    dislikes: int = ormar.Integer(default=0)
    created_at: datetime = ormar.DateTime(default=moscow_time)
    updated_at: datetime = ormar.DateTime(default=moscow_time)


class Photo(ormar.Model):
    class Meta(MainMetaDB):
        tablename = "photos"

    id: int = ormar.Integer(primary_key=True, nullable=False)
    name: str = ormar.String(max_length=250)
    uploader: User = ormar.ForeignKey(
        User,
        nullable=False,
        related_name="user_photo",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    post: Post = ormar.ForeignKey(
        Post,
        nullable=False,
        related_name="post_photo",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    uploaded_at: datetime = ormar.DateTime(default=moscow_time)


class Like(ormar.Model):
    class Meta(MainMetaDB):
        tablename = "likes"

    id: int = ormar.Integer(primary_key=True, nullable=False)
    user: User = ormar.ForeignKey(
        User,
        nullable=False,
        related_name="user_like",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    post: Post = ormar.ForeignKey(
        Post,
        nullable=False,
        related_name="post_like",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    created_at: datetime = ormar.DateTime(default=moscow_time)


class DisLike(ormar.Model):
    class Meta(MainMetaDB):
        tablename = "dislikes"

    id: int = ormar.Integer(primary_key=True, nullable=False)
    user: User = ormar.ForeignKey(
        User,
        nullable=False,
        related_name="user_dislike",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    post: Post = ormar.ForeignKey(
        Post,
        nullable=False,
        related_name="post_dislike",
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    created_at: datetime = ormar.DateTime(default=moscow_time)
