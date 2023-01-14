from fastapi import HTTPException, status

from config.config import main_settings
from config.db_config import database
from core.database.cache import set_redis_cache, remove_key_from_redis
from core.database.posts import get_or_none_post_from_db_by_id, check_and_delete_existed_like_or_dislike
from core.schemas.cache.common import SaveLikeOrDislikeInCache
from core.schemas.likes.common import LikeCreateOut, ListLikedPosts, LikeRemoveOut
from core.utils import moscow_time_now
from resources.posts.models import Like, Post
from resources.users.models import User

settings = main_settings()


async def get_all_own_likes_db(user: User) -> list[ListLikedPosts]:
    return await Like.objects.filter(user=user.id).select_related(
        ["post__post_photo", "post__creator"]).all()


async def get_or_none_like_from_db_by_post_user_id(post_id: int, user_id: int) -> Like:
    return await Like.objects.get_or_none(post=post_id, user=user_id)


async def like_post_db(post_id: int, user: User) -> LikeCreateOut:
    async with database.transaction():
        existed_like: Like = await get_or_none_like_from_db_by_post_user_id(post_id=post_id, user_id=user.id)
        existed_post: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post with current id doesn't exist")
        if existed_post.creator.id == user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't like own posts")
        if existed_like:
            pass
        else:
            dislikes_count: int = await check_and_delete_existed_like_or_dislike(post_id, user, "dislike")
            if dislikes_count:
                existed_post.dislikes -= 1
            existed_post.likes += 1
            await existed_post.update()
            like_in_db: Like = await Like.objects.create(user=user.id, post=post_id, created_at=await moscow_time_now())
            like_in_db.user = user.dict()
            print(SaveLikeOrDislikeInCache(**like_in_db.dict()))
            await set_redis_cache(post_id, user, like_in_db, "like")
        return LikeCreateOut(status=200, detail="Liked successfully")


async def remove_like_db(post_id, user) -> LikeRemoveOut:
    async with database.transaction():
        existed_like: Like = await get_or_none_like_from_db_by_post_user_id(post_id=post_id, user_id=user.id)
        existed_post: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post with current id doesn't exist")
        if existed_like:
            existed_post.likes -= 1
            await existed_post.update()
            await existed_like.delete()
            await remove_key_from_redis(post_id, user.id, "like")
        else:
            pass
        return LikeRemoveOut(status=200, detail="Like removed successfully")
