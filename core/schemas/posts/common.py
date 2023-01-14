import datetime
from typing import Optional

from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    head: str
    main_text: str


class PostUpdate(BaseModel):
    head: Optional[str]
    main_text: Optional[str]


class PostOutBase(BaseModel):
    status: int
    detail: str


class PostCreateOut(PostOutBase):
    pass


class PostUpdateOut(PostOutBase):
    pass


class PostDeleteOut(PostOutBase):
    pass


class AllPostPhotoOut(BaseModel):
    id: int
    name: str


class AllPostCreatorOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class AllPostsOut(BaseModel):
    id: int
    head: str
    main_text: str
    likes: int
    dislikes: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    post_photo: list[AllPostPhotoOut]
    creator: AllPostCreatorOut


class CurrentPostLikes(BaseModel):
    id: int
    created_at: datetime.datetime
    user: AllPostCreatorOut


class CurrentPostDislikes(BaseModel):
    id: int
    created_at: datetime.datetime
    user: AllPostCreatorOut


class CurrenPostOut(AllPostsOut):
    post_like: list[CurrentPostLikes]
    post_dislike: list[CurrentPostDislikes]
