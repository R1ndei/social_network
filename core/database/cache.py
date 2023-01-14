import aioredis
import orjson

from config.config import main_settings
from resources.posts.models import Like, DisLike
from resources.users.models import User

settings = main_settings()

redis = aioredis.from_url(settings.REDIS_URL)


async def set_redis_cache(post_id: int, user: User, like_in_db: Like | DisLike, param: str) -> None:
    value = await redis.get(f"{post_id}_{user.id}_{param}")
    if value:
        pass
    else:
        await redis.set(f"{post_id}_{user.id}_{param}", orjson.dumps(like_in_db.dict()))


async def remove_key_from_redis(post_id: int, user_id: int, param: str) -> None:
    await redis.delete(f"{post_id}_{user_id}_{param}")


async def get_all_likes_or_dislikes_for_current_post(post_id: int, param: str) -> list:
    result_list: list = []
    all_keys_names: list = await redis.keys(f"{post_id}_*_{param}")
    for key_value in all_keys_names:
        binary_data = await redis.get(key_value)
        json_data = orjson.loads(binary_data)
        result_list.append(json_data)
    return result_list
