from fastapi import APIRouter

from routes.auth.api import auth_router
from routes.dislikes.api import dislike_router
from routes.likes.api import like_router
from routes.posts.api import post_router

routes = APIRouter()

routes.include_router(auth_router)
routes.include_router(post_router)
routes.include_router(like_router)
routes.include_router(dislike_router)
