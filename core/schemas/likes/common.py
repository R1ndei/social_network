import datetime

from pydantic import BaseModel


class LikeOutBase(BaseModel):
    status: int
    detail: str


class LikeCreateOut(LikeOutBase):
    pass


class LikeRemoveOut(LikeOutBase):
    pass


class CreatorInLikeListOut(BaseModel):
    first_name: str
    last_name: str


class PostPhotoInLikeListOut(BaseModel):
    name: str


class PostInLikeListOut(BaseModel):
    id: int
    head: str
    main_text: str
    likes: int
    dislikes: int
    creator: CreatorInLikeListOut
    post_photo: list[PostPhotoInLikeListOut]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ListLikedPosts(BaseModel):
    id: int
    created_at: datetime.datetime
    post: PostInLikeListOut
