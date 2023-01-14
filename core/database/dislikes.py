from fastapi import HTTPException, status

from config.config import main_settings
from config.db_config import database
from core.database.cache import set_redis_cache, remove_key_from_redis
from core.database.posts import get_or_none_post_from_db_by_id, check_and_delete_existed_like_or_dislike
from core.schemas.dislikes.common import DisLikeCreateOut, DisLikeRemoveOut, ListDisLikedPosts
from core.utils import moscow_time_now
from resources.posts.models import Post, DisLike
from resources.users.models import User

settings = main_settings()


async def get_all_own_dislikes_db(user: User) -> list[ListDisLikedPosts]:
    return await DisLike.objects.filter(user=user.id).select_related(
        ["post__post_photo", "post__creator"]).all()


async def get_or_none_dislike_from_db_by_post_user_id(post_id: int, user_id: int) -> DisLike:
    return await DisLike.objects.get_or_none(post=post_id, user=user_id)


async def dislike_post_db(post_id: int, user: User) -> DisLikeCreateOut:
    async with database.transaction():
        existed_dislike: DisLike = await get_or_none_dislike_from_db_by_post_user_id(post_id=post_id, user_id=user.id)
        existed_post: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post doesn't exist")
        if existed_post.creator.id == user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't dislike own posts")
        if existed_dislike:
            pass
        else:
            like_count: int = await check_and_delete_existed_like_or_dislike(post_id, user, "like")
            if like_count:
                existed_post.likes -= 1
            existed_post.dislikes += 1
            await existed_post.update()
            dislike_in_db: DisLike = await DisLike.objects.create(user=user.id, post=post_id,
                                                                  created_at=await moscow_time_now())
            dislike_in_db.user = user.dict()
            await set_redis_cache(post_id, user, dislike_in_db, "dislike")
        return DisLikeCreateOut(status=200, detail="Dislike created successfully")


async def remove_dislike_db(post_id: int, user: User) -> DisLikeRemoveOut:
    async with database.transaction():
        existed_dislike: DisLike = await get_or_none_dislike_from_db_by_post_user_id(post_id=post_id, user_id=user.id)
        existed_post: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post with current id doesn't exist")
        if existed_dislike:
            existed_post.dislikes -= 1
            await existed_post.update()
            await existed_dislike.delete()
            await remove_key_from_redis(post_id, user.id, "dislike")
        else:
            pass
        return DisLikeRemoveOut(status=200, detail="DisLike removed successfully")
