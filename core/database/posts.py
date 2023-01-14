import datetime
import uuid

import aiofiles
import ormar
from fastapi import HTTPException, UploadFile
from starlette import status

from config.config import main_settings
from config.db_config import database
from core.database.cache import remove_key_from_redis, get_all_likes_or_dislikes_for_current_post
from core.schemas.posts.common import PostCreateOut, PostUpdate, PostUpdateOut, PostDeleteOut, AllPostsOut, \
    CurrenPostOut
from core.utils import moscow_time_now
from resources.posts.models import Post, Photo, Like, DisLike
from resources.users.models import User

settings = main_settings()


async def get_current_post_db(post_id: int, user: User) -> CurrenPostOut:
    existed_post: Post = await Post.objects.select_related(
        ['creator', "post_photo"]).get_or_none(id=post_id)

    existed_post.post_like = await get_all_likes_or_dislikes_for_current_post(post_id, "like")
    existed_post.post_dislike = await get_all_likes_or_dislikes_for_current_post(post_id, "dislike")
    if not existed_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post doesn't exist")
    return CurrenPostOut(**existed_post.dict())


async def get_all_posts_db(with_user_posts: bool, user: User) -> list[AllPostsOut]:
    if with_user_posts:
        return await Post.objects.select_related(["post_photo", "creator"]).all()
    else:
        return await Post.objects.exclude(creator__id=user.id).select_related(["post_photo", "creator"]).all()


async def create_post(post_data: Post) -> Post:
    return await Post.objects.create(**post_data.dict(exclude_unset=True), created_at=await moscow_time_now(),
                                     updated_at=await moscow_time_now())


async def create_photo(photo_data: Photo) -> Photo:
    return await Photo.objects.create(**photo_data.dict(exclude_unset=True), uploaded_at=await moscow_time_now())


async def get_or_none_post_from_db_by_id(post_id) -> Post:
    return await Post.objects.get_or_none(id=post_id)


async def save_post_photos(user: User, created_post: Post, post_photo: list[UploadFile]):
    for file in post_photo:
        new_photo_name: str = f"{datetime.date.today()}_{uuid.uuid4()}"
        created_photo: Photo = await create_photo(Photo(name=str(new_photo_name), uploader=user.id,
                                                        post=created_post.id))
        async with aiofiles.open(
                f'static/posts_photos/{created_photo.name}.png',
                'wb+') as out_file:
            content = await file.read()
            await out_file.write(content)


async def create_post_db(user: User, head: str, main_text: str,
                         post_photo: list[UploadFile] | None = None) -> PostCreateOut:
    async with database.transaction():
        created_post: Post = await create_post(
            Post(head=head, main_text=main_text, creator=user.id))
        if post_photo:
            await save_post_photos(user, created_post, post_photo)
        return PostCreateOut(status=200, detail=f"{created_post.head} created successfully")


async def update_post_db(post_id, update_data: PostUpdate, user) -> PostUpdateOut:
    async with database.transaction():
        existed_post_from_db: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post_from_db or existed_post_from_db.creator.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission denied")
        await existed_post_from_db.update(**update_data.dict(exclude_unset=True), updated_at=await moscow_time_now())
        return PostUpdateOut(status=200, detail="Updated successfully")


async def delete_post_db(post_id: int, user: User) -> PostDeleteOut:
    async with database.transaction():
        post_from_db: Post = await get_or_none_post_from_db_by_id(post_id)
        if not post_from_db or post_from_db.creator.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission denied")
        await post_from_db.delete()
        return PostDeleteOut(status=200, detail="Deleted successfully")


async def check_and_delete_existed_like_or_dislike(post_id: int, user: User, check_param: str) -> int:
    async with database.transaction():
        existed_post: Post = await Post.objects.get_or_none(id=post_id)
        if not existed_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post doesn't exist")
        if check_param == "like":
            existed_like: Like = await Like.objects.filter(ormar.and_(post=post_id, user=user.id)).get_or_none()
            if existed_like:
                await remove_key_from_redis(post_id, user.id, "like")
                likes_count: int = existed_post.likes
                await existed_like.delete()
                return likes_count
        if check_param == "dislike":
            existed_dislike: DisLike = await DisLike.objects.filter(
                ormar.and_(post=post_id, user=user.id)).get_or_none()
            if existed_dislike:
                await remove_key_from_redis(post_id, user.id, "dislike")
                dislikes_count: int = existed_post.dislikes
                await existed_dislike.delete()
                return dislikes_count
