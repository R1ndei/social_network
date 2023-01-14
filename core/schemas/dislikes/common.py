import datetime

from pydantic import BaseModel


class DisLikeOutBase(BaseModel):
    status: int
    detail: str


class DisLikeCreateOut(DisLikeOutBase):
    pass


class DisLikeRemoveOut(DisLikeOutBase):
    pass


class CreatorInDisLikeListOut(BaseModel):
    first_name: str
    last_name: str


class PostPhotoInDisLikeListOut(BaseModel):
    name: str


class PostInDisLikeListOut(BaseModel):
    id: int
    head: str
    main_text: str
    likes: int
    dislikes: int
    creator: CreatorInDisLikeListOut
    post_photo: list[PostPhotoInDisLikeListOut]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ListDisLikedPosts(BaseModel):
    id: int
    created_at: datetime.datetime
    post: PostInDisLikeListOut
