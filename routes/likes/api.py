from fastapi import APIRouter, Depends

from config.config import main_settings
from core.auth.auth_logic import get_current_user
from core.database.likes import like_post_db, get_all_own_likes_db, remove_like_db
from core.schemas.likes.common import LikeCreateOut, ListLikedPosts, LikeRemoveOut
from resources.users.models import User

settings = main_settings()

like_router = APIRouter(prefix=settings.API_PATH_V1 + "like",
                        tags=["Like"])


@like_router.get("")
async def get_all_own_likes(user: User = Depends(get_current_user)) -> list[ListLikedPosts]:
    return await get_all_own_likes_db(user)


@like_router.post("/{id}")
async def like_post(id: int, user: User = Depends(get_current_user)) -> LikeCreateOut:
    return await like_post_db(id, user)


@like_router.delete("/{id}")
async def remove_like(id: int, user: User = Depends(get_current_user)) -> LikeRemoveOut:
    return await remove_like_db(id, user)
