from fastapi import APIRouter

from routes.auth.api import auth_router
from routes.posts.api import post_router

routes = APIRouter()

routes.include_router(auth_router)
routes.include_router(post_router)
