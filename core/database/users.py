from fastapi import HTTPException
from starlette import status

from config.config import main_settings
from config.db_config import database
from core import validators
from core.auth.auth_logic import HashPassword, format_phone_for_db
from core.external_services.hunter_email.api import verifying_email
from core.schemas.auth.common import RegisterSchema
from core.schemas.external_services.common import HunterResponse
from core.utils import moscow_time_now
from resources.users.models import User

settings = main_settings()


async def check_user_exist_by_phone_and_email(email: str, phone: str) -> User:
    return await User.objects.get_or_none(email=email, phone=phone)


async def get_user(username: str) -> User:
    if validators.is_email(username):
        return await User.objects.get_or_none(email=username)
    username = await format_phone_for_db(username)
    if validators.is_phone(username):
        return await User.objects.get_or_none(phone=username)


async def get_superuser(username: str) -> User:
    if validators.is_email(username):
        return await User.objects.get_or_none(email=username, is_super_user=True)

    return await User.objects.get_or_none(phone=username, is_super_user=True)


async def create_user(user_data: RegisterSchema) -> User:
    async with database.transaction():
        if await check_user_exist_by_phone_and_email(user_data.email, user_data.phone):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or phone already in use")
        user_data.password = HashPassword.bcrypt(user_data.password)
        user_data.phone = await format_phone_for_db(user_data.phone)
        email_verifier: bool = False
        verification_result: HunterResponse = await verifying_email(user_data.email)
        if verification_result.status_code == 200:
            if verification_result.response["data"]["status"] in ["valid"]:
                email_verifier = True
        user = await User.objects.create(**user_data.dict(), created_at=await moscow_time_now(),
                                         is_verified_email=email_verifier)
        return user
