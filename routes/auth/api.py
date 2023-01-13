from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from config.config import main_settings
from core.auth.auth_logic import check_user, get_current_user
from core.database.users import create_user
from core.schemas.auth.common import Token, RegisterSchema, RegisterOutSchema
from resources.users.models import User

settings = main_settings()

auth_router = APIRouter(prefix=settings.API_PATH_V1 + "authorization",
                        tags=["Auth"])


@auth_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return await check_user(phone_or_email=form_data.username, password=form_data.password, scopes=['common:common'])


@auth_router.post('/registration')
async def user_registration(user: RegisterSchema) -> RegisterOutSchema:
    created_user: User = await create_user(user)
    return RegisterOutSchema(status=200, value=created_user.email)
