from fastapi import APIRouter, Depends

from config.config import main_settings
from core.auth.auth_logic import get_current_user
from core.database.dislikes import get_all_own_dislikes_db, dislike_post_db, remove_dislike_db
from core.schemas.dislikes.common import DisLikeCreateOut, DisLikeRemoveOut, ListDisLikedPosts
from resources.users.models import User

settings = main_settings()

dislike_router = APIRouter(prefix=settings.API_PATH_V1 + "dislike",
                           tags=["Dislike"])


@dislike_router.get("")
async def get_all_own_dislikes(user: User = Depends(get_current_user)) -> list[ListDisLikedPosts]:
    return await get_all_own_dislikes_db(user)


@dislike_router.post("/{id}")
async def dislike_post(id: int, user: User = Depends(get_current_user)) -> DisLikeCreateOut:
    return await dislike_post_db(id, user)


@dislike_router.delete("/{id}")
async def remove_dislike(id: int, user: User = Depends(get_current_user)) -> DisLikeRemoveOut:
    return await remove_dislike_db(id, user)
