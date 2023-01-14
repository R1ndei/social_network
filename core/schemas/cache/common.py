import datetime

from pydantic import BaseModel


class SaveUserInCache(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class SaveLikeOrDislikeInCache(BaseModel):
    id: int
    created_at: datetime.datetime
    user: SaveUserInCache
