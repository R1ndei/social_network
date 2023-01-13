from fastapi import APIRouter, Depends, File, UploadFile, Body

from config.config import main_settings
from core.auth.auth_logic import get_current_user
from core.database.posts import get_all_posts_db, create_post_db, update_post_db, delete_post_db
from core.schemas.posts.common import PostCreateSchema, PostCreateOut, PostUpdate, PostUpdateOut
from resources.users.models import User

settings = main_settings()

post_router = APIRouter(prefix=settings.API_PATH_V1 + "authorization",
                        tags=["Posts"])


@post_router.get("/post")
async def all_posts(with_user_posts: bool, user: User = Depends(get_current_user)):
    return await get_all_posts_db()


@post_router.post("/post")
async def create_post(user: User = Depends(get_current_user), head: str = Body(), main_text: str = Body(),
                      post_photo: list[UploadFile] | None = None) -> PostCreateOut:
    return await create_post_db(user, head, main_text, post_photo)


@post_router.put("/post/{id}")
async def update_post(post_id: int, update_data: PostUpdate, user: User = Depends(get_current_user)) -> PostUpdateOut:
    return await update_post_db(post_id, update_data, user)


@post_router.delete("/post/{id}")
async def delete_post(post_id: int, user: User = Depends(get_current_user)):
    return await delete_post_db(post_id, user)
