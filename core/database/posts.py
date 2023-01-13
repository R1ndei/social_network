import datetime
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile
from starlette import status

from config.config import main_settings
from config.db_config import database
from core.schemas.posts.common import PostCreateOut, PostUpdate, PostUpdateOut, PostDeleteOut
from core.utils import moscow_time_now
from resources.posts.models import Post, Photo
from resources.users.models import User

settings = main_settings()


async def get_all_posts_db(with_user_posts: bool, user: User) -> any:
    if with_user_posts:
        return await Post.objects.all()
    else:
        return await Post.objects.exclude(creator__id=user.id).all()


async def create_post(post_data: Post) -> Post:
    return await Post.objects.create(**post_data.dict(exclude_unset=True), created_at=await moscow_time_now(),
                                     updated_at=await moscow_time_now())


async def create_photo(photo_data: Photo) -> Photo:
    return await Photo.objects.create(**photo_data.dict(), uploaded_at=await moscow_time_now())


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
            content = await file.read()  # async read
            await out_file.write(content)  # async write


async def create_post_db(user: User, head: str, main_text: str, post_photo: list[UploadFile] | None = None) -> any:
    async with database.transaction():
        created_post: Post = await create_post(
            Post(head=head, main_text=main_text, creator=user.id))
        if post_photo:
            await save_post_photos(user, created_post, post_photo)
        return PostCreateOut(status=200, detail=f"{created_post.head} created successfully")


async def update_post_db(post_id, update_data: PostUpdate, user) -> any:
    async with database.transaction():
        existed_post_from_db: Post = await get_or_none_post_from_db_by_id(post_id)
        if not existed_post_from_db or existed_post_from_db.creator.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission denied")
        await existed_post_from_db.update(**update_data.dict(exclude_unset=True), updated_at=await moscow_time_now())
        return PostUpdateOut(status=200, detail="Updated successfully")


async def delete_post_db(post_id: int, user: User) -> any:
    async with database.transaction():
        post_from_db: Post = await get_or_none_post_from_db_by_id(post_id)
        if not post_from_db or post_from_db.creator.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission denied")
        await post_from_db.delete()
        return PostDeleteOut(status=200, detail="Deleted successfully")
